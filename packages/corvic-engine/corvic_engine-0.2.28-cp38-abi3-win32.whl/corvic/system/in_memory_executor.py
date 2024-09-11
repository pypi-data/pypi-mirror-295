"""Staging-agnostic in-memory executor."""

from __future__ import annotations

import dataclasses
import datetime
import functools
from collections.abc import MutableMapping
from typing import Any, Final, cast

import numpy as np
import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
import structlog
from google.protobuf import json_format, struct_pb2

from corvic import embed, embedding_metric, op_graph, sql
from corvic.result import BadArgumentError, InternalError, Ok
from corvic.system._dimension_reduction import DimensionReducer, UmapDimensionReducer
from corvic.system._embedder import EmbedTextContext, TextEmbedder
from corvic.system.op_graph_executor import (
    ExecutionContext,
    ExecutionResult,
    OpGraphExecutor,
    TableComputeContext,
    TableComputeResult,
    TableSliceArgs,
)
from corvic.system.staging import StagingDB
from corvic.system.storage import StorageManager
from corvic_generated.orm.v1 import table_pb2

_logger = structlog.get_logger()


_MIN_EMBEDDINGS_FOR_EMBEDDINGS_SUMMARY: Final = 3


def get_polars_embedding_length(
    embedding_df: pl.DataFrame, embedding_column_name: str
) -> Ok[int] | BadArgumentError:
    outer_type = embedding_df.schema[embedding_column_name]
    if isinstance(outer_type, pl.Array):
        return Ok(outer_type.shape[0])
    if not isinstance(outer_type, pl.List):
        return BadArgumentError("invalid embedding datatype", dtype=str(outer_type))
    if len(embedding_df[embedding_column_name]) == 0:
        return BadArgumentError("cannot infer embedding length for empty embedding set")
    embedding_length = len(embedding_df[embedding_column_name][0])
    if embedding_length < 1:
        return BadArgumentError("invalid embedding length", length=embedding_length)
    return Ok(embedding_length)


def get_polars_embedding(
    embedding_df: pl.DataFrame, embedding_column_name: str
) -> Ok[np.ndarray[Any, Any]] | BadArgumentError:
    outer_type = embedding_df.schema[embedding_column_name]
    if isinstance(outer_type, pl.Array):
        return Ok(embedding_df[embedding_column_name].to_numpy())
    if not isinstance(outer_type, pl.List):
        return BadArgumentError("invalid embedding datatype", dtype=str(outer_type))
    match get_polars_embedding_length(embedding_df, embedding_column_name):
        case Ok(embedding_length):
            pass
        case BadArgumentError() as err:
            return err
    return Ok(
        embedding_df[embedding_column_name]
        .cast(pl.Array(inner=outer_type.inner, shape=embedding_length))
        .to_numpy()
    )


def batch_to_proto_struct(batch: pa.RecordBatch) -> list[struct_pb2.Struct]:
    """Converts a RecordBatch to protobuf Structs safely."""
    data = batch.to_pylist()
    structs = [struct_pb2.Struct() for _ in range(len(data))]
    for idx, datum in enumerate(data):
        make_dict_bytes_human_readable(datum)
        json_format.ParseDict(datum, structs[idx])
    return structs


def cast_batch_for_storage(
    batch: pa.RecordBatch, new_schema: pa.Schema
) -> pa.RecordBatch:
    """Prepare table for storage by fixing up columns to be more widely readable.

    1. During computation a null typed column may be interpreted as non-null,
    i.e. int64, but a non-null typed column cannot be cast to a null column.

    2. Even though the parquet representation is the same for an arrow FixedSizeList
    and a List, some parquet readers (ClickHouse) do not support FixedSizeList
    but do support List.

    This function widens column types to always be nullable X instead of null and
    List instead of FixedSizeList.
    """
    select = batch.select(new_schema.names)
    storage_schema = _patch_schema_for_storage(new_schema, select.schema)
    return select.cast(storage_schema, safe=True)


def make_list_bytes_human_readable(data: list[Any]) -> None:
    """Utility function to cleanup list data types.

    This function ensures that the list can be converted to
    a protobuf Value safely.
    """
    for i in range(len(data)):
        match data[i]:
            case bytes():
                data[i] = data[i].decode("utf-8", errors="replace")
            case pl.Time() | pl.Date() | datetime.datetime() | datetime.date():
                data[i] = str(data[i])
            case dict():
                make_dict_bytes_human_readable(data[i])
            case list():
                make_list_bytes_human_readable(data[i])
            case _:
                pass


def make_dict_bytes_human_readable(data: MutableMapping[str, Any]) -> None:
    """Utility function to cleanup mapping data types.

    This function ensures that the mapping can be converted to
    a protobuf Value safely.
    """
    for k, v in data.items():
        match v:
            case bytes():
                data[k] = v.decode("utf-8", errors="replace")
            case pl.Time() | pl.Date() | datetime.datetime() | datetime.date():
                data[k] = str(v)
            case dict():
                make_dict_bytes_human_readable(data[k])
            case list():
                make_list_bytes_human_readable(data[k])
            case _:
                pass


def _patch_schema_for_storage(
    new_schema: pa.Schema, old_schema: pa.Schema
) -> pa.Schema:
    """Merge new arrow Schema with an old schema to cast data before storage.

    This merge explicitly avoids casting a non-null column to null,
    which is never a valid cast.
    """
    # TODO(Patrick): handle maps, etc
    patched_schema: list[pa.Field] = []
    for field in new_schema:
        old_field = old_schema.field(field.name)
        if pa.types.is_struct(field.type):
            patched_schema.append(_patch_struct_field(field, old_field))
        elif (
            pa.types.is_list(field.type)
            or pa.types.is_large_list(field.type)
            or pa.types.is_fixed_size_list(field.type)
        ):
            patched_schema.append(_patch_list_field(field, old_field))
        elif not pa.types.is_null(field.type):
            patched_schema.append(field)
        elif old_field and not pa.types.is_null(old_field.type):
            patched_schema.append(field.with_type(old_field.type))
        else:
            patched_schema.append(field)
    return pa.schema(patched_schema, new_schema.metadata)


def _wrap_list_type(
    list_type: pa.ListType | pa.LargeListType | pa.FixedSizeListType,
    list_value_field: pa.Field,
) -> pa.DataType:
    if isinstance(list_type, pa.ListType):
        return pa.list_(value_type=list_value_field)
    if isinstance(list_type, pa.FixedSizeListType):
        return pa.list_(value_type=list_value_field, list_size=list_type.list_size)
    return pa.large_list(value_type=list_value_field)


def _patch_list_field(
    new_field: pa.Field,
    old_field: pa.Field,
) -> pa.Field:
    new_field_type = new_field.type
    old_field_type = old_field.type
    if (
        not old_field
        or not isinstance(
            new_field_type, pa.ListType | pa.LargeListType | pa.FixedSizeListType
        )
        or not isinstance(
            old_field_type, pa.ListType | pa.LargeListType | pa.FixedSizeListType
        )
    ):
        return new_field
    new_list_field = new_field_type.value_field
    old_list_type = old_field_type.value_field.type

    if pa.types.is_struct(new_list_field.type):
        return new_field.with_type(
            _wrap_list_type(
                new_field_type,
                new_field_type.value_field.with_type(
                    _patch_struct_field(
                        new_list_field, new_list_field.with_type(old_list_type)
                    ).type
                ),
            )
        )
    if (
        pa.types.is_list(new_list_field.type)
        or pa.types.is_large_list(new_list_field.type)
        or pa.types.is_fixed_size_list(new_list_field.type)
    ):
        return new_field.with_type(
            _wrap_list_type(
                new_field_type,
                new_field_type.value_field.with_type(
                    _patch_list_field(
                        new_list_field, new_list_field.with_type(old_list_type)
                    ).type
                ),
            )
        )
    if not pa.types.is_null(new_list_field.type):
        return new_field
    return new_field.with_type(
        _wrap_list_type(new_field_type, old_field_type.value_field)
    )


def _patch_struct_field(
    new_field: pa.Field,
    old_field: pa.Field,
) -> pa.Field:
    new_field_type = new_field.type
    if not old_field or not isinstance(new_field_type, pa.StructType):
        return new_field
    old_struct = old_field.type
    if not isinstance(old_struct, pa.StructType):
        return new_field

    patched_nested_fields: list[pa.Field] = []
    for field_index in range(old_struct.num_fields):
        old_nested_field = old_struct.field(field_index)
        field = new_field_type.field(
            new_field_type.get_field_index(old_nested_field.name)
        )
        if pa.types.is_struct(field.type):
            patched_nested_fields.append(
                _patch_struct_field(field, field.with_type(old_nested_field.type))
            )
        elif (
            pa.types.is_list(field.type)
            or pa.types.is_large_list(field.type)
            or pa.types.is_fixed_size_list(field.type)
        ):
            patched_nested_fields.append(
                _patch_list_field(field, field.with_type(old_nested_field.type))
            )
        elif not pa.types.is_null(field.type):
            patched_nested_fields.append(field)
        elif old_nested_field.type and not pa.types.is_null(old_nested_field.type):
            patched_nested_fields.append(field.with_type(old_nested_field.type))
        else:
            patched_nested_fields.append(field)
    return new_field.with_type(pa.struct(patched_nested_fields))


def _as_df(
    batch_or_batch_container: pa.RecordBatchReader | pa.RecordBatch | _SchemaAndBatches,
    expected_schema: pa.Schema | None = None,
):
    expected_schema = expected_schema or batch_or_batch_container.schema
    schema_dataframe = cast(pl.DataFrame, pl.from_arrow(expected_schema.empty_table()))

    match batch_or_batch_container:
        case pa.RecordBatchReader():
            batches = list(batch_or_batch_container)
        case _SchemaAndBatches():
            batches = batch_or_batch_container.batches
        case pa.RecordBatch():
            batches = [batch_or_batch_container]

    if not batches:
        return schema_dataframe

    schema_dataframe = cast(pl.DataFrame, pl.from_arrow(batches[0]))

    return cast(
        pl.DataFrame,
        pl.from_arrow(batches, rechunk=False, schema=schema_dataframe.schema),
    )


@dataclasses.dataclass(frozen=True)
class _SchemaAndBatches:
    schema: pa.Schema
    batches: list[pa.RecordBatch]
    metrics: dict[str, Any]

    def to_batch_reader(self):
        return pa.RecordBatchReader.from_batches(
            schema=self.schema, batches=self.batches
        )

    def cast_for_storage(self, op: op_graph.Op) -> _SchemaAndBatches:
        if not self.batches:
            return _SchemaAndBatches(
                schema=self.schema, batches=self.batches, metrics=self.metrics
            )
        new_schema = op.schema.to_arrow()
        old_schema = self.batches[0].select(new_schema.names).schema
        storage_schema = _patch_schema_for_storage(
            new_schema=new_schema, old_schema=old_schema
        )
        cast_batches = [
            batch.select(storage_schema.names).cast(storage_schema, safe=True)
            for batch in self.batches
        ]
        return _SchemaAndBatches(
            schema=storage_schema, batches=cast_batches, metrics=self.metrics
        )

    @classmethod
    def from_dataframe(cls, dataframe: pl.DataFrame, metrics: dict[str, Any]):
        table = dataframe.to_arrow()
        schema = table.schema
        return cls(schema, table.to_batches(), metrics)


@dataclasses.dataclass(frozen=True)
class _SlicedTable:
    op_graph: op_graph.Op
    slice_args: TableSliceArgs | None


@dataclasses.dataclass
class _InMemoryExecutionContext:
    exec_context: ExecutionContext
    current_output_context: TableComputeContext | None = None

    # Using _SchemaAndBatches rather than a RecordBatchReader since the latter's
    # contract only guarantees one iteration and these might be accessed more than
    # once
    computed_batches_for_op_graph: dict[_SlicedTable, _SchemaAndBatches] = (
        dataclasses.field(default_factory=dict)
    )

    @classmethod
    def count_source_op_uses(
        cls,
        op: op_graph.Op,
        use_counts: dict[_SlicedTable, int],
        slice_args: TableSliceArgs | None,
    ):
        for source in op.sources():
            sliced_table = _SlicedTable(source, slice_args)
            use_counts[sliced_table] = use_counts.get(sliced_table, 0) + 1
            cls.count_source_op_uses(source, use_counts, slice_args)

    @property
    def current_slice_args(self) -> TableSliceArgs | None:
        if self.current_output_context:
            return self.current_output_context.sql_output_slice_args
        return None

    @functools.cached_property
    def reused_tables(self) -> set[_SlicedTable]:
        use_counts = dict[_SlicedTable, int]()
        for output_table in self.output_tables:
            self.count_source_op_uses(
                output_table.op_graph, use_counts, output_table.slice_args
            )

        return {op for op, count in use_counts.items() if count > 1}

    @functools.cached_property
    def output_tables(self) -> set[_SlicedTable]:
        return {
            _SlicedTable(ctx.table_op_graph, ctx.sql_output_slice_args)
            for ctx in self.exec_context.tables_to_compute
        }


class InMemoryTableComputeResult(TableComputeResult):
    """The in-memory result of computing a particular op graph."""

    def __init__(
        self,
        storage_manager: StorageManager,
        batches: _SchemaAndBatches,
        context: TableComputeContext,
    ):
        self._storage_manager = storage_manager
        self._batches = batches
        self._context = context

    @property
    def metrics(self):
        return self._batches.metrics

    def to_batch_reader(self) -> pa.RecordBatchReader:
        return self._batches.to_batch_reader()

    def to_urls(self) -> list[str]:
        # one file for now; we may produce more in the future
        file_idx = 0
        file_name = f"{self._context.output_url_prefix}.{file_idx:>06}"
        with (
            self._storage_manager.blob_from_url(file_name).open("wb") as stream,
            pq.ParquetWriter(stream, self._batches.schema) as writer,
        ):
            for batch in self._batches.batches:
                writer.write_batch(batch)

        return [file_name]

    @property
    def context(self) -> TableComputeContext:
        return self._context


class InMemoryExecutionResult(ExecutionResult):
    """A container for in-memory results.

    This container is optimized to avoid writes to disk, i.e., `to_batch_reader` will
    be fast `to_urls` will be slow.
    """

    def __init__(
        self,
        tables: list[InMemoryTableComputeResult],
        context: ExecutionContext,
    ):
        self._tables = tables
        self._context = context

    @classmethod
    def make(
        cls,
        storage_manager: StorageManager,
        in_memory_context: _InMemoryExecutionContext,
        context: ExecutionContext,
    ) -> InMemoryExecutionResult:
        tables = [
            InMemoryTableComputeResult(
                storage_manager,
                in_memory_context.computed_batches_for_op_graph[
                    _SlicedTable(
                        table_context.table_op_graph,
                        table_context.sql_output_slice_args,
                    )
                ],
                table_context,
            )
            for table_context in context.tables_to_compute
        ]
        return InMemoryExecutionResult(
            tables,
            context,
        )

    @property
    def tables(self) -> list[InMemoryTableComputeResult]:
        return self._tables

    @property
    def context(self) -> ExecutionContext:
        return self._context


class InMemoryExecutor(OpGraphExecutor):
    """Executes op_graphs in memory (after staging queries)."""

    def __init__(
        self,
        staging_db: StagingDB,
        storage_manager: StorageManager,
        text_embedder: TextEmbedder,
        dimension_reducer: DimensionReducer | None = None,
    ):
        self._staging_db = staging_db
        self._storage_manager = storage_manager
        self._text_embedder = text_embedder
        self._dimension_reducer = dimension_reducer or UmapDimensionReducer()

    @classmethod
    def _is_sql_compatible(cls, op: op_graph.Op) -> bool:
        return isinstance(op, sql.SqlComputableOp) and all(
            cls._is_sql_compatible(sub_op) for sub_op in op.sources()
        )

    def _execute_read_from_parquet(
        self, op: op_graph.op.ReadFromParquet, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches]:
        batches: list[pa.RecordBatch] = []
        for blob_name in op.blob_names:
            with (
                self._storage_manager.blob_from_url(blob_name).open("rb") as stream,
            ):
                batches.extend(
                    # reading files with pyarrow, then converting them to polars
                    # can cause "ShapeError" bugs. That's why we're not reading this
                    # using pyarrow.
                    pl.read_parquet(
                        source=stream,
                        columns=op.arrow_schema.names,
                        use_pyarrow=False,
                    )
                    .to_arrow()
                    .to_batches()
                )
        return Ok(_SchemaAndBatches(op.arrow_schema, batches=batches, metrics={}))

    def _execute_rollup_by_aggregation(
        self, op: op_graph.op.RollupByAggregation, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches]:
        raise NotImplementedError(
            "rollup by aggregation outside of sql not implemented"
        )

    def _execute_rename_columns(
        self, op: op_graph.op.RenameColumns, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches] | InternalError:
        return self._execute(op.source, context).map(
            lambda source_batches: _SchemaAndBatches.from_dataframe(
                _as_df(source_batches).rename(dict(op.old_name_to_new)),
                source_batches.metrics,
            )
        )

    def _execute_select_columns(
        self, op: op_graph.op.SelectColumns, context: _InMemoryExecutionContext
    ):
        return self._execute(op.source, context).map(
            lambda source_batches: _SchemaAndBatches.from_dataframe(
                _as_df(source_batches).select(op.columns), source_batches.metrics
            )
        )

    def _execute_limit_rows(
        self, op: op_graph.op.LimitRows, context: _InMemoryExecutionContext
    ):
        return self._execute(op.source, context).map(
            lambda source_batches: _SchemaAndBatches.from_dataframe(
                _as_df(source_batches).limit(op.num_rows),
                source_batches.metrics,
            )
        )

    def _execute_order_by(
        self, op: op_graph.op.OrderBy, context: _InMemoryExecutionContext
    ):
        return self._execute(op.source, context).map(
            lambda source_batches: _SchemaAndBatches.from_dataframe(
                _as_df(source_batches).sort(op.columns, descending=op.desc),
                source_batches.metrics,
            )
        )

    def _row_filter_literal_comparison_to_condition(
        self, row_filter: op_graph.row_filter.CompareColumnToLiteral
    ) -> Ok[pl.Expr] | op_graph.OpParseError:
        match row_filter.comparison_type:
            case table_pb2.COMPARISON_TYPE_EQ:
                comp = pl.col(row_filter.column_name) == row_filter.literal
            case table_pb2.COMPARISON_TYPE_NE:
                comp = pl.col(row_filter.column_name) != row_filter.literal
            case table_pb2.COMPARISON_TYPE_LT:
                comp = pl.col(row_filter.column_name) < row_filter.literal
            case table_pb2.COMPARISON_TYPE_GT:
                comp = pl.col(row_filter.column_name) > row_filter.literal
            case table_pb2.COMPARISON_TYPE_LE:
                comp = pl.col(row_filter.column_name) <= row_filter.literal
            case table_pb2.COMPARISON_TYPE_GE:
                comp = pl.col(row_filter.column_name) >= row_filter.literal
            case _:
                return op_graph.OpParseError(
                    "unknown comparison type value in row filter",
                    value=row_filter.comparison_type,
                )
        return Ok(comp)

    def _row_filter_combination_to_condition(
        self, row_filter: op_graph.row_filter.CombineFilters
    ) -> Ok[pl.Expr] | op_graph.OpParseError:
        sub_filters = list[pl.Expr]()
        for sub_filter in row_filter.row_filters:
            match self._row_filter_to_condition(sub_filter):
                case Ok(new_sub_filter):
                    sub_filters.append(new_sub_filter)
                case op_graph.OpParseError() as err:
                    return err
        match row_filter.combination_op:
            case table_pb2.LOGICAL_COMBINATION_ANY:
                return Ok(
                    functools.reduce(lambda left, right: left | right, sub_filters)
                )
            case table_pb2.LOGICAL_COMBINATION_ALL:
                return Ok(
                    functools.reduce(lambda left, right: left & right, sub_filters)
                )
            case _:
                return op_graph.OpParseError(
                    "unknown logical combination op value in row filter",
                    value=row_filter.combination_op,
                )

    def _row_filter_to_condition(
        self, row_filter: op_graph.RowFilter
    ) -> Ok[pl.Expr] | op_graph.OpParseError:
        match row_filter:
            case op_graph.row_filter.CompareColumnToLiteral():
                return self._row_filter_literal_comparison_to_condition(row_filter)
            case op_graph.row_filter.CombineFilters():
                return self._row_filter_combination_to_condition(row_filter)

    def _execute_filter_rows(
        self, op: op_graph.op.FilterRows, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches] | InternalError:
        match self._execute(op.source, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                return self._row_filter_to_condition(op.row_filter).map_or_else(
                    lambda err: InternalError.from_(err),
                    lambda row_filter: Ok(
                        _SchemaAndBatches.from_dataframe(
                            _as_df(source_batches).filter(row_filter),
                            source_batches.metrics,
                        )
                    ),
                )

    def _execute_embedding_metrics(
        self, op: op_graph.op.EmbeddingMetrics, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches] | InternalError:
        match self._execute(op.table, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                pass
        embedding_df = _as_df(source_batches)

        if len(embedding_df) < _MIN_EMBEDDINGS_FOR_EMBEDDINGS_SUMMARY:
            # downstream consumers handle empty metadata by substituting their
            # own values
            return Ok(source_batches)

        # before it was configurable, this op assumed that the column's name was
        # this hardcoded name
        embedding_column_name = op.embedding_column_name or "embedding"
        match get_polars_embedding(embedding_df, embedding_column_name):
            case Ok(embedding):
                pass
            case BadArgumentError() as err:
                raise err

        metrics = source_batches.metrics.copy()
        metrics["ne_sum"] = embedding_metric.ne_sum(embedding, normalize=True)
        metrics["condition_number"] = embedding_metric.condition_number(
            embedding, normalize=True
        )
        metrics["rcondition_number"] = embedding_metric.rcondition_number(
            embedding, normalize=True
        )
        metrics["stable_rank"] = embedding_metric.stable_rank(embedding, normalize=True)
        return Ok(_SchemaAndBatches.from_dataframe(embedding_df, metrics=metrics))

    def _execute_embedding_coordinates(
        self, op: op_graph.op.EmbeddingCoordinates, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches] | InternalError:
        match self._execute(op.table, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                pass
        embedding_df = _as_df(source_batches)

        # before it was configurable, this op assumed that the column's name was
        # this hardcoded name
        embedding_column_name = op.embedding_column_name or "embedding"

        # the neighbors of a point includes itself. That does mean, that an n_neighbors
        # value of less than 3 simply does not work
        if len(embedding_df) < _MIN_EMBEDDINGS_FOR_EMBEDDINGS_SUMMARY:
            coordinates_df = embedding_df.with_columns(
                pl.Series(
                    name=embedding_column_name,
                    values=[[0.0] * op.n_components] * len(embedding_df),
                    dtype=pl.Array(pl.Float32, op.n_components),
                )
            )
            return Ok(
                _SchemaAndBatches.from_dataframe(coordinates_df, source_batches.metrics)
            )

        match get_polars_embedding(embedding_df, embedding_column_name):
            case Ok(embedding):
                pass
            case BadArgumentError() as err:
                raise err

        coordinates = self._dimension_reducer.reduce_dimensions(
            embedding, op.n_components, op.metric
        )
        coordinates_df = embedding_df.with_columns(
            pl.Series(
                name=embedding_column_name,
                values=coordinates,
                dtype=pl.Array(pl.Float32, coordinates.shape[1]),
            )
        )
        return Ok(
            _SchemaAndBatches.from_dataframe(coordinates_df, source_batches.metrics)
        )

    def _execute_distinct_rows(
        self, op: op_graph.op.DistinctRows, context: _InMemoryExecutionContext
    ):
        return self._execute(op.source, context).map(
            lambda source_batches: _SchemaAndBatches.from_dataframe(
                _as_df(source_batches).unique(), source_batches.metrics
            )
        )

    def _execute_join(
        self, op: op_graph.op.Join, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches] | InternalError:
        match self._execute(op.left_source, context):
            case InternalError() as err:
                return err
            case Ok(left_batches):
                pass
        match self._execute(op.right_source, context):
            case InternalError() as err:
                return err
            case Ok(right_batches):
                pass
        left_df = _as_df(left_batches)
        right_df = _as_df(right_batches)

        match op.how:
            case table_pb2.JOIN_TYPE_INNER:
                join_type = "inner"
            case table_pb2.JOIN_TYPE_LEFT_OUTER:
                join_type = "left"
            case _:
                join_type = "inner"

        # in our join semantics we drop columns from the right source on conflict
        right_df = right_df.select(
            [
                col
                for col in right_df.columns
                if col in op.right_join_columns or col not in left_df.columns
            ]
        )
        metrics = right_batches.metrics.copy()
        metrics.update(left_batches.metrics)

        # polars doesn't behave so well when one side is empty, just
        # compute the trivial empty join when the result is guaranteed
        # to be empty instead.
        if len(left_df) == 0 or len(right_df) == 0 and join_type == "inner":
            return Ok(
                _SchemaAndBatches(
                    schema=op.schema.to_arrow(),
                    batches=op.schema.to_arrow().empty_table().to_batches(),
                    metrics=metrics,
                )
            )

        return Ok(
            _SchemaAndBatches.from_dataframe(
                left_df.join(
                    right_df,
                    left_on=op.left_join_columns,
                    right_on=op.right_join_columns,
                    how=join_type,
                ),
                metrics,
            )
        )

    def _execute_empty(self, op: op_graph.op.Empty, context: _InMemoryExecutionContext):
        empty_table = pa.schema([]).empty_table()
        return Ok(
            _SchemaAndBatches(empty_table.schema, empty_table.to_batches(), metrics={})
        )

    def _execute_concat(
        self, op: op_graph.op.Concat, context: _InMemoryExecutionContext
    ):
        source_batches = list[_SchemaAndBatches]()
        for table in op.tables:
            match self._execute(table, context):
                case InternalError() as err:
                    return err
                case Ok(batches):
                    source_batches.append(batches)
        dataframes = [_as_df(batches) for batches in source_batches]
        metrics = dict[str, Any]()
        for batches in source_batches:
            metrics.update(batches.metrics)
        return Ok(
            _SchemaAndBatches.from_dataframe(
                pl.concat(dataframes, how=op.how), metrics=metrics
            )
        )

    def _execute_unnest_struct(
        self, op: op_graph.op.UnnestStruct, context: _InMemoryExecutionContext
    ):
        return self._execute(op.source, context).map(
            lambda source_batches: _SchemaAndBatches.from_dataframe(
                _as_df(source_batches).unnest(op.struct_column_name),
                source_batches.metrics,
            )
        )

    def _execute_nest_into_struct(
        self, op: op_graph.op.NestIntoStruct, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                pass
        non_struct_columns = [
            name
            for name in source_batches.schema.names
            if name not in op.column_names_to_nest
        ]
        return Ok(
            _SchemaAndBatches.from_dataframe(
                _as_df(source_batches).select(
                    *non_struct_columns,
                    pl.struct(op.column_names_to_nest).alias(op.struct_column_name),
                ),
                source_batches.metrics,
            )
        )

    def _execute_add_literal_column(
        self, op: op_graph.op.AddLiteralColumn, context: _InMemoryExecutionContext
    ):
        pl_schema = cast(
            pl.DataFrame, pl.from_arrow(op.column_arrow_schema.empty_table())
        ).schema
        name, dtype = next(iter(pl_schema.items()))

        column = pl.Series(name, op.literals).cast(dtype)
        return self._execute(op.source, context).map(
            lambda source_batches: _SchemaAndBatches.from_dataframe(
                _as_df(source_batches).with_columns(column),
                source_batches.metrics,
            )
        )

    def _execute_combine_columns(
        self, op: op_graph.op.CombineColumns, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                pass
        source_df = _as_df(source_batches)
        match op.reduction:
            case op_graph.ConcatString():
                # if we do not ignore nulls then all concatenated rows that
                # have a single column that contain a null value will be output
                # as null.
                result_df = source_df.with_columns(
                    pl.concat_str(
                        [pl.col(col) for col in op.column_names],
                        separator=op.reduction.separator,
                        ignore_nulls=True,
                    ).alias(op.combined_column_name)
                )

            case op_graph.ConcatList():
                result_df = source_df.with_columns(
                    pl.concat_list(*op.column_names).alias(op.combined_column_name)
                )

        return Ok(_SchemaAndBatches.from_dataframe(result_df, source_batches.metrics))

    def _execute_embed_column(
        self, op: op_graph.op.EmbedColumn, context: _InMemoryExecutionContext
    ):
        match self._execute(op.source, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                pass
        source_df = _as_df(source_batches)
        to_embed = source_df[op.column_name].cast(pl.String())

        embed_context = EmbedTextContext(
            inputs=to_embed,
            model_name=op.model_name,
            tokenizer_name=op.tokenizer_name,
            expected_vector_length=op.expected_vector_length,
            expected_coordinate_bitwidth=op.expected_coordinate_bitwidth,
        )
        match self._text_embedder.embed(embed_context):
            case Ok(result):
                pass
            case BadArgumentError() | InternalError() as err:
                raise InternalError("Failed to embed column") from err

        result_df = source_df.with_columns(
            result.embeddings.alias(op.embedding_column_name)
        ).drop_nulls(op.embedding_column_name)

        return Ok(
            _SchemaAndBatches.from_dataframe(
                result_df,
                source_batches.metrics,
            )
        )

    def _execute_encode_column(  # noqa: C901
        self, op: op_graph.op.EncodeColumn, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches] | InternalError:
        match self._execute(op.source, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                pass
        source_df = _as_df(source_batches)
        to_encode = source_df[op.column_name].cast(pl.String())
        match op.encoder:
            case op_graph.encoder.OneHotEncoder():
                encoded = to_encode.to_dummies()
                return Ok(
                    _SchemaAndBatches.from_dataframe(
                        source_df.with_columns(
                            encoded.select(
                                pl.concat_list(pl.all()).alias(op.encoded_column_name)
                            )
                        ),
                        source_batches.metrics,
                    )
                )
            case op_graph.encoder.MinMaxScaler():
                from sklearn.preprocessing import MinMaxScaler

                encoder = MinMaxScaler(
                    feature_range=(
                        op.encoder.feature_range_min,
                        op.encoder.feature_range_max,
                    )
                )
                encoded = encoder.fit_transform(
                    to_encode.to_numpy().reshape(-1, 1)
                ).flatten()

            case op_graph.encoder.LabelBinarizer():
                from sklearn.preprocessing import LabelBinarizer

                encoder = LabelBinarizer(
                    neg_label=op.encoder.neg_label, pos_label=op.encoder.pos_label
                )
                encoded = encoder.fit_transform(to_encode.to_numpy().reshape(-1))

            case op_graph.encoder.LabelEncoder():
                from sklearn.preprocessing import LabelEncoder

                encoder = LabelEncoder()
                encoded = encoder.fit_transform(
                    to_encode.to_numpy().reshape(-1)
                ).flatten()

            case op_graph.encoder.KBinsDiscretizer():
                from sklearn.preprocessing import KBinsDiscretizer

                encoder = KBinsDiscretizer(
                    n_bins=op.encoder.n_bins,
                    encode=op.encoder.encode_method,
                    strategy=op.encoder.strategy,
                    dtype=np.float32,
                )
                encoded = encoder.fit_transform(
                    to_encode.to_numpy().reshape(-1, 1)
                ).flatten()

            case op_graph.encoder.Binarizer():
                from sklearn.preprocessing import Binarizer

                encoder = Binarizer(
                    threshold=op.encoder.threshold,
                )
                encoded = encoder.fit_transform(
                    to_encode.to_numpy().reshape(-1, 1)
                ).flatten()

            case op_graph.encoder.MaxAbsScaler():
                from sklearn.preprocessing import MaxAbsScaler

                encoder = MaxAbsScaler()
                encoded = encoder.fit_transform(
                    to_encode.to_numpy().reshape(-1, 1)
                ).flatten()

            case op_graph.encoder.StandardScaler():
                from sklearn.preprocessing import StandardScaler

                encoder = StandardScaler(
                    with_mean=op.encoder.with_mean,
                    with_std=op.encoder.with_std,
                )
                encoded = encoder.fit_transform(
                    to_encode.to_numpy().reshape(-1, 1)
                ).flatten()

        return Ok(
            _SchemaAndBatches.from_dataframe(
                source_df.with_columns(
                    pl.Series(
                        name=op.encoded_column_name,
                        values=encoded,
                        dtype=op.encoder.output_dtype,
                    )
                ),
                source_batches.metrics,
            )
        )

    def _execute_embed_node2vec_from_edge_lists(
        self,
        op: op_graph.op.EmbedNode2vecFromEdgeLists,
        context: _InMemoryExecutionContext,
    ):
        dtypes: set[pa.DataType] = set()
        entities_dtypes: dict[str, pa.DataType] = {}
        for edge_list in op.edge_list_tables:
            schema = edge_list.table.schema.to_arrow()
            start_dtype = schema.field(edge_list.start_column_name).type
            end_dtype = schema.field(edge_list.end_column_name).type
            dtypes.add(start_dtype)
            dtypes.add(end_dtype)
            entities_dtypes[edge_list.start_column_name] = start_dtype
            entities_dtypes[edge_list.end_column_name] = end_dtype

        start_fields = [pa.field(f"start_id_{dtype}", dtype) for dtype in dtypes]
        start_fields.append(pa.field("start_source", pa.large_string()))
        start_id_column_names = [field.name for field in start_fields]

        end_fields = [pa.field(f"end_id_{dtype}", dtype) for dtype in dtypes]
        end_fields.append(pa.field("end_source", pa.large_string()))
        end_id_column_names = [field.name for field in end_fields]

        fields = start_fields + end_fields
        empty_edges_table = pl.from_arrow(pa.schema(fields).empty_table())

        if isinstance(empty_edges_table, pl.Series):
            empty_edges_table = empty_edges_table.to_frame()

        metrics = dict[str, Any]()

        edge_list_batches = list[_SchemaAndBatches]()
        for edge_list in op.edge_list_tables:
            match self._execute(edge_list.table, context):
                case InternalError() as err:
                    return err
                case Ok(source_batches):
                    edge_list_batches.append(source_batches)

        def edge_generator():
            for edge_list, batches in zip(
                op.edge_list_tables, edge_list_batches, strict=True
            ):
                start_column_name = edge_list.start_column_name
                end_column_name = edge_list.end_column_name
                start_column_type_name = entities_dtypes[start_column_name]
                end_column_type_name = entities_dtypes[end_column_name]
                metrics.update(batches.metrics)
                for batch in batches.batches:
                    yield (
                        _as_df(batch)
                        .with_columns(
                            pl.col(edge_list.start_column_name).alias(
                                f"start_id_{start_column_type_name}"
                            ),
                            pl.lit(edge_list.start_entity_name).alias("start_source"),
                            pl.col(edge_list.end_column_name).alias(
                                f"end_id_{end_column_type_name}"
                            ),
                            pl.lit(edge_list.end_entity_name).alias("end_source"),
                        )
                        .select(
                            f"start_id_{start_column_type_name}",
                            "start_source",
                            f"end_id_{end_column_type_name}",
                            "end_source",
                        )
                    )

        edges = pl.concat(
            [
                empty_edges_table,
                *(edge_list for edge_list in edge_generator()),
            ],
            rechunk=False,
            how="diagonal",
        )

        n2v_space = embed.Space(
            edges=edges,
            start_id_column_names=start_id_column_names,
            end_id_column_names=end_id_column_names,
            directed=True,
        )
        n2v_runner = embed.Node2Vec(
            space=n2v_space,
            dim=op.ndim,
            walk_length=op.walk_length,
            window=op.window,
            p=op.p,
            q=op.q,
            alpha=op.alpha,
            min_alpha=op.min_alpha,
            negative=op.negative,
        )
        n2v_runner.train(epochs=op.epochs)
        return Ok(_SchemaAndBatches.from_dataframe(n2v_runner.wv.to_polars(), metrics))

    def _execute_aggregate_columns(
        self, op: op_graph.op.AggregateColumns, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches] | InternalError:
        match self._execute(op.source, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                pass
        source_df = _as_df(source_batches)
        to_aggregate = source_df[op.column_names]

        match op.aggregation:
            case op_graph.aggregation.Min():
                aggregate = to_aggregate.min()
            case op_graph.aggregation.Max():
                aggregate = to_aggregate.max()
            case op_graph.aggregation.Mean():
                aggregate = to_aggregate.mean()
            case op_graph.aggregation.Std():
                aggregate = to_aggregate.std()
            case op_graph.aggregation.Quantile():
                aggregate = to_aggregate.quantile(op.aggregation.quantile)
            case op_graph.aggregation.Count():
                aggregate = to_aggregate.count()
            case op_graph.aggregation.NullCount():
                aggregate = to_aggregate.null_count()

        return Ok(_SchemaAndBatches.from_dataframe(aggregate, metrics={}))

    def _execute_correlate_columns(
        self, op: op_graph.op.CorrelateColumns, context: _InMemoryExecutionContext
    ):
        return self._execute(op.source, context).map(
            lambda source_batches: _SchemaAndBatches.from_dataframe(
                _as_df(source_batches)[op.column_names].corr(dtype="float32"),
                metrics={},
            )
        )

    def _execute_histogram_column(
        self, op: op_graph.op.HistogramColumn, context: _InMemoryExecutionContext
    ):
        return self._execute(op.source, context).map(
            lambda source_batches: _SchemaAndBatches.from_dataframe(
                _as_df(source_batches)[op.column_name]
                .hist(include_category=False)
                .rename(
                    {
                        "breakpoint": op.breakpoint_column_name,
                        "count": op.count_column_name,
                    }
                ),
                metrics={},
            )
        )

    def _execute_convert_columns_to_string(
        self, op: op_graph.op.ConvertColumnToString, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches] | InternalError:
        match self._execute(op.source, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                pass
        source_df = _as_df(source_batches)
        column = source_df[op.column_name]
        if not column.dtype.is_nested():
            source_df = source_df.with_columns(column.cast(pl.String(), strict=False))
        elif isinstance(column.dtype, pl.Array | pl.List):
            source_df = source_df.with_columns(
                column.cast(pl.List(pl.String())).list.join(",")
            )
        else:
            raise NotImplementedError(
                "converting struct columns to strings is not implemented"
            )
        return Ok(
            _SchemaAndBatches.from_dataframe(source_df, metrics=source_batches.metrics)
        )

    def _execute_add_row_index(
        self, op: op_graph.op.AddRowIndex, context: _InMemoryExecutionContext
    ):
        return self._execute(op.source, context).map(
            lambda source_batches: _SchemaAndBatches.from_dataframe(
                _as_df(source_batches)
                .with_row_index(name=op.row_index_column_name, offset=op.offset)
                .with_columns(pl.col(op.row_index_column_name).cast(pl.UInt64())),
                metrics=source_batches.metrics,
            )
        )

    def _execute_output_csv(
        self, op: op_graph.op.OutputCsv, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches] | InternalError:
        match self._execute(op.source, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                pass
        source_df = _as_df(source_batches)
        source_df.write_csv(
            op.csv_url,
            quote_style="never",
            include_header=op.include_header,
        )
        return Ok(source_batches)

    def _execute_truncate_list(
        self, op: op_graph.op.TruncateList, context: _InMemoryExecutionContext
    ) -> Ok[_SchemaAndBatches] | InternalError:
        # TODO(Patrick): verify this approach works for arrays
        match self._execute(op.source, context):
            case InternalError() as err:
                return err
            case Ok(source_batches):
                pass
        source_df = _as_df(source_batches)
        existing_length = get_polars_embedding_length(
            source_df, op.column_name
        ).unwrap_or_raise()
        head_length = (
            op.target_column_length
            if existing_length >= op.target_column_length
            else existing_length
        )
        source_df = source_df.with_columns(
            pl.col(op.column_name).list.head(head_length)
        )
        if head_length < op.target_column_length:
            padding_length = op.target_column_length - head_length
            padding: list[Any] = [op.padding_value] * padding_length
            source_df = source_df.with_columns(
                pl.col(op.column_name).list.concat(padding)
            )
        source_df = source_df.with_columns(
            pl.col(op.column_name).list.to_array(width=op.target_column_length)
        )
        return Ok(
            _SchemaAndBatches.from_dataframe(source_df, metrics=source_batches.metrics)
        )

    def _do_execute(  # noqa: PLR0911, PLR0912, C901
        self,
        op: op_graph.Op,
        context: _InMemoryExecutionContext,
    ) -> Ok[_SchemaAndBatches] | InternalError:
        if self._is_sql_compatible(op) and self._staging_db:
            query = sql.parse_op_graph(
                op,
                self._staging_db.query_for_blobs,
                self._staging_db.query_for_vector_search,
            )
            expected_schema = op.schema.to_arrow()
            return self._staging_db.run_select_query(
                query, expected_schema, context.current_slice_args
            ).map(
                lambda rbr: _SchemaAndBatches.from_dataframe(
                    _as_df(rbr, expected_schema), metrics={}
                )
            )

        match op:
            case op_graph.op.SelectFromStaging():
                raise InternalError("SelectFromStaging should always be lowered to sql")
            case op_graph.op.SelectFromVectorStaging():
                raise InternalError(
                    "SelectFromVectorStaging should always be lowered to sql"
                )
            case op_graph.op.ReadFromParquet():
                return self._execute_read_from_parquet(op, context)
            case op_graph.op.RenameColumns():
                return self._execute_rename_columns(op, context)
            case op_graph.op.Join():
                return self._execute_join(op, context)
            case op_graph.op.SelectColumns():
                return self._execute_select_columns(op, context)
            case op_graph.op.LimitRows():
                return self._execute_limit_rows(op, context)
            case op_graph.op.OrderBy():
                return self._execute_order_by(op, context)
            case op_graph.op.FilterRows():
                return self._execute_filter_rows(op, context)
            case op_graph.op.DistinctRows():
                return self._execute_distinct_rows(op, context)
            case (
                op_graph.op.SetMetadata()
                | op_graph.op.UpdateMetadata()
                | op_graph.op.RemoveFromMetadata()
                | op_graph.op.UpdateFeatureTypes()
            ):
                return self._execute(op.source, context)
            case op_graph.op.EmbeddingMetrics() as op:
                return self._execute_embedding_metrics(op, context)
            case op_graph.op.EmbeddingCoordinates():
                return self._execute_embedding_coordinates(op, context)
            case op_graph.op.RollupByAggregation() as op:
                return self._execute_rollup_by_aggregation(op, context)
            case op_graph.op.Empty():
                return self._execute_empty(op, context)
            case op_graph.op.EmbedNode2vecFromEdgeLists():
                return self._execute_embed_node2vec_from_edge_lists(op, context)
            case op_graph.op.Concat():
                return self._execute_concat(op, context)
            case op_graph.op.UnnestStruct():
                return self._execute_unnest_struct(op, context)
            case op_graph.op.NestIntoStruct():
                return self._execute_nest_into_struct(op, context)
            case op_graph.op.AddLiteralColumn():
                return self._execute_add_literal_column(op, context)
            case op_graph.op.CombineColumns():
                return self._execute_combine_columns(op, context)
            case op_graph.op.EmbedColumn():
                return self._execute_embed_column(op, context)
            case op_graph.op.EncodeColumn():
                return self._execute_encode_column(op, context)
            case op_graph.op.AggregateColumns():
                return self._execute_aggregate_columns(op, context)
            case op_graph.op.CorrelateColumns():
                return self._execute_correlate_columns(op, context)
            case op_graph.op.HistogramColumn():
                return self._execute_histogram_column(op, context)
            case op_graph.op.ConvertColumnToString():
                return self._execute_convert_columns_to_string(op, context)
            case op_graph.op.AddRowIndex():
                return self._execute_add_row_index(op, context)
            case op_graph.op.OutputCsv():
                return self._execute_output_csv(op, context)
            case op_graph.op.TruncateList():
                return self._execute_truncate_list(op, context)

    def _execute(
        self,
        op: op_graph.Op,
        context: _InMemoryExecutionContext,
        *,
        cast_for_storage: bool = False,
    ) -> Ok[_SchemaAndBatches] | InternalError:
        with structlog.contextvars.bound_contextvars(
            executing_op=op.expected_oneof_field()
        ):
            sliced_table = _SlicedTable(op, context.current_slice_args)
            if sliced_table in context.computed_batches_for_op_graph:
                _logger.info("using previously computed table for op")
                return Ok(context.computed_batches_for_op_graph[sliced_table])

            try:
                _logger.info("starting op execution")
                maybe_batches = self._do_execute(op=op, context=context)
            finally:
                _logger.info("op execution complete")
            match maybe_batches:
                case InternalError() as err:
                    return err
                case Ok(batches):
                    if cast_for_storage:
                        batches = batches.cast_for_storage(op)

            if (
                sliced_table in context.output_tables
                or sliced_table in context.reused_tables
            ):
                context.computed_batches_for_op_graph[sliced_table] = batches
            return Ok(batches)

    def execute(
        self, context: ExecutionContext
    ) -> Ok[ExecutionResult] | BadArgumentError | InternalError:
        in_memory_context = _InMemoryExecutionContext(context)

        for table_context in context.tables_to_compute:
            in_memory_context.current_output_context = table_context
            sliced_table = _SlicedTable(
                table_context.table_op_graph, table_context.sql_output_slice_args
            )
            if sliced_table not in in_memory_context.computed_batches_for_op_graph:
                match self._execute(
                    sliced_table.op_graph, in_memory_context, cast_for_storage=True
                ):
                    case InternalError() as err:
                        return err
                    case Ok():
                        pass

        return Ok(
            InMemoryExecutionResult.make(
                self._storage_manager, in_memory_context, context
            )
        )
