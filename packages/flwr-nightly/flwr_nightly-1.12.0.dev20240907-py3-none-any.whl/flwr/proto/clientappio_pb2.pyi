"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import flwr.proto.fab_pb2
import flwr.proto.message_pb2
import flwr.proto.run_pb2
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _ClientAppOutputCode:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _ClientAppOutputCodeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ClientAppOutputCode.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    SUCCESS: _ClientAppOutputCode.ValueType  # 0
    DEADLINE_EXCEEDED: _ClientAppOutputCode.ValueType  # 1
    UNKNOWN_ERROR: _ClientAppOutputCode.ValueType  # 2
class ClientAppOutputCode(_ClientAppOutputCode, metaclass=_ClientAppOutputCodeEnumTypeWrapper):
    pass

SUCCESS: ClientAppOutputCode.ValueType  # 0
DEADLINE_EXCEEDED: ClientAppOutputCode.ValueType  # 1
UNKNOWN_ERROR: ClientAppOutputCode.ValueType  # 2
global___ClientAppOutputCode = ClientAppOutputCode


class ClientAppOutputStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CODE_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    code: global___ClientAppOutputCode.ValueType
    message: typing.Text
    def __init__(self,
        *,
        code: global___ClientAppOutputCode.ValueType = ...,
        message: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["code",b"code","message",b"message"]) -> None: ...
global___ClientAppOutputStatus = ClientAppOutputStatus

class GetTokenRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    def __init__(self,
        ) -> None: ...
global___GetTokenRequest = GetTokenRequest

class GetTokenResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TOKEN_FIELD_NUMBER: builtins.int
    token: builtins.int
    def __init__(self,
        *,
        token: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["token",b"token"]) -> None: ...
global___GetTokenResponse = GetTokenResponse

class PullClientAppInputsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TOKEN_FIELD_NUMBER: builtins.int
    token: builtins.int
    def __init__(self,
        *,
        token: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["token",b"token"]) -> None: ...
global___PullClientAppInputsRequest = PullClientAppInputsRequest

class PullClientAppInputsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MESSAGE_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    RUN_FIELD_NUMBER: builtins.int
    FAB_FIELD_NUMBER: builtins.int
    @property
    def message(self) -> flwr.proto.message_pb2.Message: ...
    @property
    def context(self) -> flwr.proto.message_pb2.Context: ...
    @property
    def run(self) -> flwr.proto.run_pb2.Run: ...
    @property
    def fab(self) -> flwr.proto.fab_pb2.Fab: ...
    def __init__(self,
        *,
        message: typing.Optional[flwr.proto.message_pb2.Message] = ...,
        context: typing.Optional[flwr.proto.message_pb2.Context] = ...,
        run: typing.Optional[flwr.proto.run_pb2.Run] = ...,
        fab: typing.Optional[flwr.proto.fab_pb2.Fab] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["context",b"context","fab",b"fab","message",b"message","run",b"run"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context",b"context","fab",b"fab","message",b"message","run",b"run"]) -> None: ...
global___PullClientAppInputsResponse = PullClientAppInputsResponse

class PushClientAppOutputsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TOKEN_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    token: builtins.int
    @property
    def message(self) -> flwr.proto.message_pb2.Message: ...
    @property
    def context(self) -> flwr.proto.message_pb2.Context: ...
    def __init__(self,
        *,
        token: builtins.int = ...,
        message: typing.Optional[flwr.proto.message_pb2.Message] = ...,
        context: typing.Optional[flwr.proto.message_pb2.Context] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["context",b"context","message",b"message"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context",b"context","message",b"message","token",b"token"]) -> None: ...
global___PushClientAppOutputsRequest = PushClientAppOutputsRequest

class PushClientAppOutputsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STATUS_FIELD_NUMBER: builtins.int
    @property
    def status(self) -> global___ClientAppOutputStatus: ...
    def __init__(self,
        *,
        status: typing.Optional[global___ClientAppOutputStatus] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["status",b"status"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["status",b"status"]) -> None: ...
global___PushClientAppOutputsResponse = PushClientAppOutputsResponse
