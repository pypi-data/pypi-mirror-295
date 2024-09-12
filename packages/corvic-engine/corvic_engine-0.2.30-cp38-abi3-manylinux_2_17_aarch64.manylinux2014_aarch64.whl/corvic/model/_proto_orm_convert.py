import dataclasses

from typing_extensions import overload

from corvic import orm
from corvic.result import BadArgumentError, Ok
from corvic_generated.model.v1alpha import models_pb2

_Proto = (
    models_pb2.Resource
    | models_pb2.Source
    | models_pb2.FeatureView
    | models_pb2.Space
    | models_pb2.FeatureViewSource
    | models_pb2.Agent
)
_Orm = (
    orm.Resource
    | orm.Source
    | orm.FeatureView
    | orm.Space
    | orm.FeatureViewSource
    | orm.Agent
)
_ID = (
    orm.ResourceID
    | orm.SourceID
    | orm.FeatureViewID
    | orm.SpaceID
    | orm.FeatureViewSourceID
    | orm.AgentID
)


@dataclasses.dataclass
class _OrmIDs:
    obj_id: int | None
    room_id: int | None


def _translate_orm_ids(
    proto_obj: _Proto, obj_id_class: type[_ID]
) -> Ok[_OrmIDs] | orm.InvalidORMIdentifierError:
    if not proto_obj.id:
        obj_id = None
    else:
        match obj_id_class(proto_obj.id).to_orm():
            case orm.InvalidORMIdentifierError() as err:
                return err
            case Ok(obj_id):
                pass

    match proto_obj:
        case (
            models_pb2.Resource()
            | models_pb2.Source()
            | models_pb2.FeatureView()
            | models_pb2.Space()
            | models_pb2.Agent()
        ):
            match orm.RoomID(proto_obj.room_id).to_orm():
                case orm.InvalidORMIdentifierError() as err:
                    return err
                case Ok(room_id):
                    pass
        case models_pb2.FeatureViewSource():
            room_id = None

    return Ok(_OrmIDs(obj_id, room_id))


@overload
def orm_to_proto(orm_obj: orm.Resource) -> models_pb2.Resource: ...


@overload
def orm_to_proto(orm_obj: orm.Source) -> models_pb2.Source: ...


@overload
def orm_to_proto(orm_obj: orm.FeatureView) -> models_pb2.FeatureView: ...


@overload
def orm_to_proto(orm_obj: orm.Space) -> models_pb2.Space: ...


@overload
def orm_to_proto(orm_obj: orm.FeatureViewSource) -> models_pb2.FeatureViewSource: ...


@overload
def orm_to_proto(orm_obj: orm.Agent) -> models_pb2.Agent: ...


def orm_to_proto(orm_obj: _Orm) -> _Proto:
    match orm_obj:
        case orm.Resource():
            return models_pb2.Resource(
                id=str(orm.ResourceID.from_orm(orm_obj.id)),
                name=orm_obj.name,
                description=orm_obj.description,
                mime_type=orm_obj.mime_type,
                url=orm_obj.url,
                md5=orm_obj.md5,
                size=orm_obj.size,
                original_path=orm_obj.original_path,
                room_id=str(orm.RoomID.from_orm(orm_obj.room_id)),
                source_ids=[
                    str(orm.SourceID.from_orm(val.source_id))
                    for val in orm_obj.source_associations
                ],
                org_id=orm_obj.org_id,
            )
        case orm.Source():
            return models_pb2.Source(
                id=str(orm.SourceID.from_orm(orm_obj.id)),
                name=orm_obj.name,
                table_op_graph=orm_obj.table_op_graph,
                room_id=str(orm.RoomID.from_orm(orm_obj.room_id)),
                resource_id=str(
                    orm.ResourceID.from_orm(
                        orm_obj.resource_associations[0].resource_id
                    )
                )
                if orm_obj.resource_associations
                else "",
            )
        case orm.FeatureView():
            raise NotImplementedError()
        case orm.Space():
            raise NotImplementedError()
        case orm.FeatureViewSource():
            raise NotImplementedError()
        case orm.Agent():
            return models_pb2.Agent(
                id=str(orm.AgentID.from_orm(orm_obj.id)),
                name=orm_obj.name,
                room_id=str(orm.RoomID.from_orm(orm_obj.room_id)),
                agent_parameters=orm_obj.parameters,
                org_id=orm_obj.org_id,
            )


@overload
def proto_to_orm(
    proto_obj: models_pb2.Resource,
) -> Ok[orm.Resource] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.Source,
) -> Ok[orm.Source] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.FeatureView,
) -> Ok[orm.FeatureView] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.Space,
) -> Ok[orm.Space] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.FeatureViewSource,
) -> Ok[orm.FeatureViewSource] | orm.InvalidORMIdentifierError: ...


@overload
def proto_to_orm(
    proto_obj: models_pb2.Agent,
) -> Ok[orm.Agent] | orm.InvalidORMIdentifierError: ...


def _resource_proto_to_orm(
    proto_obj: models_pb2.Resource,
) -> Ok[orm.Resource] | orm.InvalidORMIdentifierError | BadArgumentError:
    match _translate_orm_ids(proto_obj, orm.ResourceID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return BadArgumentError("room id required to commit resource")

    source_ids = list[int]()
    for source_id in proto_obj.source_ids:
        match orm.SourceID(source_id).to_orm():
            case orm.InvalidORMIdentifierError() as err:
                return err
            case Ok(orm_id):
                source_ids.append(orm_id)
    orm_obj = orm.Resource(
        id=ids.obj_id,
        name=proto_obj.name,
        description=proto_obj.description,
        mime_type=proto_obj.mime_type,
        md5=proto_obj.md5,
        url=proto_obj.url,
        size=proto_obj.size,
        original_path=proto_obj.original_path,
        room_id=ids.room_id,
        source_associations=[
            orm.SourceResourceAssociation(source_id=src_id, resource_id=ids.obj_id)
            for src_id in source_ids
        ],
    )
    if proto_obj.org_id:
        orm_obj.org_id = proto_obj.org_id
    return Ok(orm_obj)


def _source_proto_to_orm(
    proto_obj: models_pb2.Source,
) -> Ok[orm.Source] | orm.InvalidORMIdentifierError | BadArgumentError:
    match _translate_orm_ids(proto_obj, orm.SourceID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return BadArgumentError("room id required to commit resource")
    match orm.ResourceID(proto_obj.resource_id).to_orm():
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(resource_id):
            pass

    orm_obj = orm.Source(
        id=ids.obj_id,
        name=proto_obj.name,
        table_op_graph=proto_obj.table_op_graph,
        room_id=ids.room_id,
        resource_associations=[
            orm.SourceResourceAssociation(source_id=ids.obj_id, resource_id=resource_id)
        ],
    )
    if proto_obj.org_id:
        orm_obj.org_id = proto_obj.org_id
    return Ok(orm_obj)


def _agent_proto_to_orm(
    proto_obj: models_pb2.Agent,
) -> Ok[orm.Agent] | orm.InvalidORMIdentifierError | BadArgumentError:
    match _translate_orm_ids(proto_obj, orm.AgentID):
        case orm.InvalidORMIdentifierError() as err:
            return err
        case Ok(ids):
            pass
    if not ids.room_id:
        return BadArgumentError("room id required to commit resource")

    orm_obj = orm.Agent(
        id=ids.obj_id,
        name=proto_obj.name,
        parameters=proto_obj.agent_parameters,
        room_id=ids.room_id,
    )
    if proto_obj.org_id:
        orm_obj.org_id = proto_obj.org_id
    return Ok(orm_obj)


def proto_to_orm(
    proto_obj: _Proto,
) -> Ok[_Orm] | orm.InvalidORMIdentifierError | BadArgumentError:
    match proto_obj:
        case models_pb2.Resource():
            return _resource_proto_to_orm(proto_obj)
        case models_pb2.Source():
            return _source_proto_to_orm(proto_obj)
        case models_pb2.FeatureView():
            raise NotImplementedError()
        case models_pb2.Space():
            raise NotImplementedError()
        case models_pb2.FeatureViewSource():
            raise NotImplementedError()
        case models_pb2.Agent():
            return _agent_proto_to_orm(proto_obj)
