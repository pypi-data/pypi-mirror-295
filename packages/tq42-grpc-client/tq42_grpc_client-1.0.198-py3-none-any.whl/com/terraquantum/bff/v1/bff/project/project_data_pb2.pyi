from com.terraquantum.project.v1.project import project_pb2 as _project_pb2
from com.terraquantum.user.v1.user import user_pb2 as _user_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectDataProto(_message.Message):
    __slots__ = ("project", "user", "dataset_count", "models_count", "experiment_count")
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    DATASET_COUNT_FIELD_NUMBER: _ClassVar[int]
    MODELS_COUNT_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_COUNT_FIELD_NUMBER: _ClassVar[int]
    project: _project_pb2.ProjectProto
    user: _user_pb2.UserProto
    dataset_count: int
    models_count: int
    experiment_count: int
    def __init__(self, project: _Optional[_Union[_project_pb2.ProjectProto, _Mapping]] = ..., user: _Optional[_Union[_user_pb2.UserProto, _Mapping]] = ..., dataset_count: _Optional[int] = ..., models_count: _Optional[int] = ..., experiment_count: _Optional[int] = ...) -> None: ...
