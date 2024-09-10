from com.terraquantum.experiment.v3alpha1.experimentrun import experiment_run_pb2 as _experiment_run_pb2
from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckExperimentRunAgainstCreditsRequest(_message.Message):
    __slots__ = ("org_id", "experiment_run")
    ORG_ID_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_RUN_FIELD_NUMBER: _ClassVar[int]
    org_id: str
    experiment_run: _experiment_run_pb2.ExperimentRunProto
    def __init__(self, org_id: _Optional[str] = ..., experiment_run: _Optional[_Union[_experiment_run_pb2.ExperimentRunProto, _Mapping]] = ...) -> None: ...
