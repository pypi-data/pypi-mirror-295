# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: flwr/proto/exec.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from flwr.proto import fab_pb2 as flwr_dot_proto_dot_fab__pb2
from flwr.proto import transport_pb2 as flwr_dot_proto_dot_transport__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x66lwr/proto/exec.proto\x12\nflwr.proto\x1a\x14\x66lwr/proto/fab.proto\x1a\x1a\x66lwr/proto/transport.proto\"\xdf\x02\n\x0fStartRunRequest\x12\x1c\n\x03\x66\x61\x62\x18\x01 \x01(\x0b\x32\x0f.flwr.proto.Fab\x12H\n\x0foverride_config\x18\x02 \x03(\x0b\x32/.flwr.proto.StartRunRequest.OverrideConfigEntry\x12L\n\x11\x66\x65\x64\x65ration_config\x18\x03 \x03(\x0b\x32\x31.flwr.proto.StartRunRequest.FederationConfigEntry\x1aI\n\x13OverrideConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12!\n\x05value\x18\x02 \x01(\x0b\x32\x12.flwr.proto.Scalar:\x02\x38\x01\x1aK\n\x15\x46\x65\x64\x65rationConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12!\n\x05value\x18\x02 \x01(\x0b\x32\x12.flwr.proto.Scalar:\x02\x38\x01\"\"\n\x10StartRunResponse\x12\x0e\n\x06run_id\x18\x01 \x01(\x12\"#\n\x11StreamLogsRequest\x12\x0e\n\x06run_id\x18\x01 \x01(\x12\"(\n\x12StreamLogsResponse\x12\x12\n\nlog_output\x18\x01 \x01(\t2\xa0\x01\n\x04\x45xec\x12G\n\x08StartRun\x12\x1b.flwr.proto.StartRunRequest\x1a\x1c.flwr.proto.StartRunResponse\"\x00\x12O\n\nStreamLogs\x12\x1d.flwr.proto.StreamLogsRequest\x1a\x1e.flwr.proto.StreamLogsResponse\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'flwr.proto.exec_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_STARTRUNREQUEST_OVERRIDECONFIGENTRY']._options = None
  _globals['_STARTRUNREQUEST_OVERRIDECONFIGENTRY']._serialized_options = b'8\001'
  _globals['_STARTRUNREQUEST_FEDERATIONCONFIGENTRY']._options = None
  _globals['_STARTRUNREQUEST_FEDERATIONCONFIGENTRY']._serialized_options = b'8\001'
  _globals['_STARTRUNREQUEST']._serialized_start=88
  _globals['_STARTRUNREQUEST']._serialized_end=439
  _globals['_STARTRUNREQUEST_OVERRIDECONFIGENTRY']._serialized_start=289
  _globals['_STARTRUNREQUEST_OVERRIDECONFIGENTRY']._serialized_end=362
  _globals['_STARTRUNREQUEST_FEDERATIONCONFIGENTRY']._serialized_start=364
  _globals['_STARTRUNREQUEST_FEDERATIONCONFIGENTRY']._serialized_end=439
  _globals['_STARTRUNRESPONSE']._serialized_start=441
  _globals['_STARTRUNRESPONSE']._serialized_end=475
  _globals['_STREAMLOGSREQUEST']._serialized_start=477
  _globals['_STREAMLOGSREQUEST']._serialized_end=512
  _globals['_STREAMLOGSRESPONSE']._serialized_start=514
  _globals['_STREAMLOGSRESPONSE']._serialized_end=554
  _globals['_EXEC']._serialized_start=557
  _globals['_EXEC']._serialized_end=717
# @@protoc_insertion_point(module_scope)
