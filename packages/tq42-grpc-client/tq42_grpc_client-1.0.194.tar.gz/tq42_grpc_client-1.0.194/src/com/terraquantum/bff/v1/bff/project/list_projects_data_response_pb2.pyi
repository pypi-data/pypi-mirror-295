from com.terraquantum.bff.v1.bff.project import project_data_pb2 as _project_data_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListProjectsDataResponse(_message.Message):
    __slots__ = ("projects",)
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    projects: _containers.RepeatedCompositeFieldContainer[_project_data_pb2.ProjectDataProto]
    def __init__(self, projects: _Optional[_Iterable[_Union[_project_data_pb2.ProjectDataProto, _Mapping]]] = ...) -> None: ...
