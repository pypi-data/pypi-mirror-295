"""Filter definitions for the FilterRows op."""

from __future__ import annotations

import functools
from collections.abc import Mapping, Sequence
from typing import Any, Final, overload

from google.protobuf import json_format

from corvic.op_graph.errors import OpParseError
from corvic.proto_wrapper import OneofProtoWrapper, ProtoParseError
from corvic.result import BadArgumentError, Ok
from corvic_generated.orm.v1 import table_pb2


@overload
def from_proto(proto: table_pb2.RowFilter) -> RowFilter: ...


@overload
def from_proto(
    proto: table_pb2.CompareColumnToLiteralRowFilter,
) -> CompareColumnToLiteral: ...


@overload
def from_proto(proto: table_pb2.CombineFiltersRowFilter) -> CombineFilters: ...


def from_proto(
    proto: (
        table_pb2.RowFilter
        | table_pb2.CompareColumnToLiteralRowFilter
        | table_pb2.CombineFiltersRowFilter
    ),
) -> RowFilter:
    """Create an Op wrapper around an Op protobuf message."""
    match proto:
        case table_pb2.RowFilter():
            return _from_row_filter(proto)
        case table_pb2.CompareColumnToLiteralRowFilter():
            return CompareColumnToLiteral(
                table_pb2.RowFilter(compare_column_to_literal=proto)
            )
        case table_pb2.CombineFiltersRowFilter():
            return CombineFilters(table_pb2.RowFilter(combine_filters=proto))


def _from_row_filter(proto: table_pb2.RowFilter) -> RowFilter:
    field_name = proto.WhichOneof(_Base.oneof_name())
    new_filter_type = _FILTER_FIELD_NAME_TO_ROW_FILTER.get(field_name)
    if new_filter_type is None:
        raise BadArgumentError("unsupported filter type", operation_type=field_name)
    return new_filter_type(proto)


class _Base(OneofProtoWrapper[table_pb2.RowFilter]):
    """Base type for all row filters."""

    @classmethod
    def oneof_name(cls) -> str:
        return "filter"

    @classmethod
    def expected_oneof_field(cls) -> str:
        """Returns the name of field for this type in the root proto op type."""
        if cls not in _ROW_FILTER_TO_FILTER_FIELD_NAME:
            raise ProtoParseError(
                "filter field name must registered in _FILTER_FIELD_NAME_TO_ROW_FILTER"
            )
        return _ROW_FILTER_TO_FILTER_FIELD_NAME[cls]

    def and_(self, other: RowFilter):
        return from_proto(
            table_pb2.CombineFiltersRowFilter(
                row_filters=[self._proto, other.to_proto()],
                logical_combination=table_pb2.LOGICAL_COMBINATION_ALL,
            )
        )

    def or_(self, other: RowFilter):
        return from_proto(
            table_pb2.CombineFiltersRowFilter(
                row_filters=[self._proto, other.to_proto()],
                logical_combination=table_pb2.LOGICAL_COMBINATION_ANY,
            )
        )


def _make_compare_to_literal_proto(
    column_name: str, literal: Any, comparison_type: table_pb2.ComparisonType
):
    proto_filter = table_pb2.CompareColumnToLiteralRowFilter()
    try:
        json_format.ParseDict({"literal": literal}, proto_filter)
    except json_format.ParseError as json_parse_error:
        raise OpParseError(
            "provided literal not valid for comparison"
        ) from json_parse_error

    proto_filter.column_name = column_name
    proto_filter.comparison_type = comparison_type
    return proto_filter


def _make_compare_to_literal(
    column_name: str, literal: Any, comparison_type: table_pb2.ComparisonType
):
    return from_proto(
        _make_compare_to_literal_proto(column_name, literal, comparison_type)
    )


def eq(column_name: str, literal: Any):
    """Include rows where column is equal to a literal."""
    return _make_compare_to_literal(column_name, literal, table_pb2.COMPARISON_TYPE_EQ)


def ne(column_name: str, literal: Any):
    """Include rows where column is not equal to a literal."""
    return _make_compare_to_literal(column_name, literal, table_pb2.COMPARISON_TYPE_NE)


def lt(column_name: str, literal: Any):
    """Include rows where column is less than to a literal."""
    return _make_compare_to_literal(column_name, literal, table_pb2.COMPARISON_TYPE_LT)


def gt(column_name: str, literal: Any):
    """Include rows where column is greater than to a literal."""
    return _make_compare_to_literal(column_name, literal, table_pb2.COMPARISON_TYPE_GT)


def le(column_name: str, literal: Any):
    """Include rows where column is less than or equal to than a literal."""
    return _make_compare_to_literal(column_name, literal, table_pb2.COMPARISON_TYPE_LE)


def ge(column_name: str, literal: Any):
    """Include rows where column is greater than or equal to to a literal."""
    return _make_compare_to_literal(column_name, literal, table_pb2.COMPARISON_TYPE_GE)


def in_(column_name: str, literals: list[Any]):
    """Include rows where column matches any value in the list of literals."""
    return from_proto(
        table_pb2.CombineFiltersRowFilter(
            row_filters=[
                table_pb2.RowFilter(
                    compare_column_to_literal=_make_compare_to_literal_proto(
                        column_name, literal, table_pb2.COMPARISON_TYPE_EQ
                    )
                )
                for literal in literals
            ],
            logical_combination=table_pb2.LOGICAL_COMBINATION_ANY,
        )
    )


def not_in(column_name: str, literals: list[Any]):
    """Include rows where column does not match any value in the list of literals."""
    return from_proto(
        table_pb2.CombineFiltersRowFilter(
            row_filters=[
                table_pb2.RowFilter(
                    compare_column_to_literal=_make_compare_to_literal_proto(
                        column_name, literal, table_pb2.COMPARISON_TYPE_NE
                    )
                )
                for literal in literals
            ],
            logical_combination=table_pb2.LOGICAL_COMBINATION_ALL,
        )
    )


def _parse_raw_literal_expression(
    operands: list[Any],
) -> Ok[tuple[str, Any]] | BadArgumentError:
    expected_literal_operands = 2
    if len(operands) != expected_literal_operands:
        return BadArgumentError("unsupported literal expression passed")
    column_value = ""
    literal_value: Any = None
    for operand in operands:
        if isinstance(operand, dict) and "var" in operand:
            operand_value: Any = operand["var"]
            if not isinstance(operand_value, str):
                return BadArgumentError("invalid column name in literal expression")
            column_value = operand_value
        else:
            literal_value = operand
    if not column_value or literal_value is None:
        return BadArgumentError(
            "could not parse column name and/or literal from expression"
        )
    return Ok((column_value, literal_value))


def _create_literal_expression(  # noqa: PLR0911
    op: str, column_name: str, literal: Any
) -> Ok[RowFilter] | BadArgumentError:
    match op:
        case "==":
            return Ok(eq(column_name, literal))
        case "!=":
            return Ok(ne(column_name, literal))
        case "<=":
            return Ok(le(column_name, literal))
        case ">=":
            return Ok(ge(column_name, literal))
        case "<":
            return Ok(lt(column_name, literal))
        case ">":
            return Ok(gt(column_name, literal))
        case _:
            return BadArgumentError("unsupported literal row filter operation", op=op)


def _create_compound_expression(
    op: str, sub_ops: list[RowFilter]
) -> Ok[RowFilter] | BadArgumentError:
    if len(sub_ops) <= 1:
        return BadArgumentError(
            "invalid compound operation, not enough sub operations",
            op=op,
            num_sub_ops=len(sub_ops),
        )
    compound_op = sub_ops[0]
    for sub_op in sub_ops[1:]:
        match op.upper():
            case "AND":
                compound_op = compound_op.and_(sub_op)
            case "OR":
                compound_op = compound_op.or_(sub_op)
            case _:
                return BadArgumentError(
                    "unsupported compound row filter operation", op=op
                )
    return Ok(compound_op)


def parse_jsonlogic(expression: Mapping[str, Any]) -> Ok[RowFilter] | BadArgumentError:  # noqa: PLR0911
    """Parses an expression in JsonLogic into a RowFilter.

    More information on the JsonLogic format can be found at https://jsonlogic.com
    """
    if not expression or len(expression) != 1 or not isinstance(expression, dict):
        return BadArgumentError("row filter expression tree is not a binary tree")
    op, raw_operands = next(iter(expression.items()), (None, None))
    if not isinstance(op, str) or not isinstance(raw_operands, list):
        return BadArgumentError("row filter expression tree missing op or operands")
    operands: list[Any] = raw_operands
    match op.upper():
        case "AND" | "OR":
            sub_ops: list[RowFilter] = []
            for sub_op in operands:
                match parse_jsonlogic(sub_op):
                    case Ok(sub_filter):
                        sub_ops.append(sub_filter)
                    case BadArgumentError() as err:
                        return err
            return _create_compound_expression(op, sub_ops)
        case "==" | "!=" | "<=" | ">=" | "<" | ">":
            match _parse_raw_literal_expression(operands):
                case Ok(parsed_expression):
                    column_name, literal = parsed_expression
                    return _create_literal_expression(op, column_name, literal)
                case BadArgumentError() as err:
                    return err
        case _:
            return BadArgumentError("unsupported row filter operation", op=op)


class CompareColumnToLiteral(_Base):
    """A row filter that compares row values to literals."""

    @property
    def column_name(self) -> str:
        return self._proto.compare_column_to_literal.column_name

    @property
    def comparison_type(self) -> table_pb2.ComparisonType:
        return self._proto.compare_column_to_literal.comparison_type

    @functools.cached_property
    def literal(self):
        return json_format.MessageToDict(self._proto.compare_column_to_literal)[
            "literal"
        ]


class CombineFilters(_Base):
    """A row filter that combines the results of other filters."""

    @functools.cached_property
    def row_filters(self) -> Sequence[RowFilter]:
        return [
            from_proto(row_filter)
            for row_filter in self._proto.combine_filters.row_filters
        ]

    @property
    def combination_op(self) -> table_pb2.LogicalCombination:
        return self._proto.combine_filters.logical_combination


RowFilter = CompareColumnToLiteral | CombineFilters

_FILTER_FIELD_NAME_TO_ROW_FILTER: Final = {
    "compare_column_to_literal": CompareColumnToLiteral,
    "combine_filters": CombineFilters,
}

_ROW_FILTER_TO_FILTER_FIELD_NAME: Final[dict[type[Any], str]] = {
    op: name for name, op in _FILTER_FIELD_NAME_TO_ROW_FILTER.items()
}
