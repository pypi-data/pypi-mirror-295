"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import flwr.proto.node_pb2
import flwr.proto.task_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class CreateNodeRequest(google.protobuf.message.Message):
    """CreateNode messages"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PING_INTERVAL_FIELD_NUMBER: builtins.int
    ping_interval: builtins.float
    def __init__(self,
        *,
        ping_interval: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["ping_interval",b"ping_interval"]) -> None: ...
global___CreateNodeRequest = CreateNodeRequest

class CreateNodeResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NODE_FIELD_NUMBER: builtins.int
    @property
    def node(self) -> flwr.proto.node_pb2.Node: ...
    def __init__(self,
        *,
        node: typing.Optional[flwr.proto.node_pb2.Node] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["node",b"node"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["node",b"node"]) -> None: ...
global___CreateNodeResponse = CreateNodeResponse

class DeleteNodeRequest(google.protobuf.message.Message):
    """DeleteNode messages"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NODE_FIELD_NUMBER: builtins.int
    @property
    def node(self) -> flwr.proto.node_pb2.Node: ...
    def __init__(self,
        *,
        node: typing.Optional[flwr.proto.node_pb2.Node] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["node",b"node"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["node",b"node"]) -> None: ...
global___DeleteNodeRequest = DeleteNodeRequest

class DeleteNodeResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    def __init__(self,
        ) -> None: ...
global___DeleteNodeResponse = DeleteNodeResponse

class PingRequest(google.protobuf.message.Message):
    """Ping messages"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NODE_FIELD_NUMBER: builtins.int
    PING_INTERVAL_FIELD_NUMBER: builtins.int
    @property
    def node(self) -> flwr.proto.node_pb2.Node: ...
    ping_interval: builtins.float
    def __init__(self,
        *,
        node: typing.Optional[flwr.proto.node_pb2.Node] = ...,
        ping_interval: builtins.float = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["node",b"node"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["node",b"node","ping_interval",b"ping_interval"]) -> None: ...
global___PingRequest = PingRequest

class PingResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SUCCESS_FIELD_NUMBER: builtins.int
    success: builtins.bool
    def __init__(self,
        *,
        success: builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["success",b"success"]) -> None: ...
global___PingResponse = PingResponse

class PullTaskInsRequest(google.protobuf.message.Message):
    """PullTaskIns messages"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NODE_FIELD_NUMBER: builtins.int
    TASK_IDS_FIELD_NUMBER: builtins.int
    @property
    def node(self) -> flwr.proto.node_pb2.Node: ...
    @property
    def task_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
    def __init__(self,
        *,
        node: typing.Optional[flwr.proto.node_pb2.Node] = ...,
        task_ids: typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["node",b"node"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["node",b"node","task_ids",b"task_ids"]) -> None: ...
global___PullTaskInsRequest = PullTaskInsRequest

class PullTaskInsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RECONNECT_FIELD_NUMBER: builtins.int
    TASK_INS_LIST_FIELD_NUMBER: builtins.int
    @property
    def reconnect(self) -> global___Reconnect: ...
    @property
    def task_ins_list(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[flwr.proto.task_pb2.TaskIns]: ...
    def __init__(self,
        *,
        reconnect: typing.Optional[global___Reconnect] = ...,
        task_ins_list: typing.Optional[typing.Iterable[flwr.proto.task_pb2.TaskIns]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["reconnect",b"reconnect"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["reconnect",b"reconnect","task_ins_list",b"task_ins_list"]) -> None: ...
global___PullTaskInsResponse = PullTaskInsResponse

class PushTaskResRequest(google.protobuf.message.Message):
    """PushTaskRes messages"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TASK_RES_LIST_FIELD_NUMBER: builtins.int
    @property
    def task_res_list(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[flwr.proto.task_pb2.TaskRes]: ...
    def __init__(self,
        *,
        task_res_list: typing.Optional[typing.Iterable[flwr.proto.task_pb2.TaskRes]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["task_res_list",b"task_res_list"]) -> None: ...
global___PushTaskResRequest = PushTaskResRequest

class PushTaskResResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class ResultsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: builtins.int
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: builtins.int = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    RECONNECT_FIELD_NUMBER: builtins.int
    RESULTS_FIELD_NUMBER: builtins.int
    @property
    def reconnect(self) -> global___Reconnect: ...
    @property
    def results(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, builtins.int]: ...
    def __init__(self,
        *,
        reconnect: typing.Optional[global___Reconnect] = ...,
        results: typing.Optional[typing.Mapping[typing.Text, builtins.int]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["reconnect",b"reconnect"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["reconnect",b"reconnect","results",b"results"]) -> None: ...
global___PushTaskResResponse = PushTaskResResponse

class Reconnect(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RECONNECT_FIELD_NUMBER: builtins.int
    reconnect: builtins.int
    def __init__(self,
        *,
        reconnect: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["reconnect",b"reconnect"]) -> None: ...
global___Reconnect = Reconnect
