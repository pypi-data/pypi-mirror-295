import grpc

import orchestra._internals.rpc.orchestra.element_types_pb2 as element_types_pb2
from orchestra._internals.rpc.orchestra import element_types_pb2_grpc

from orchestra.elements.models.element_type import ElementType


class OrchestraElementTypeInterface:
    def __init__(self, channel: grpc.Channel):
        self.element_types_stub = element_types_pb2_grpc.ElementTypesServiceStub(channel)

    def create_element_type(self, name: str) -> ElementType:
        # TODO: exception handling
        response: element_types_pb2.ElementType = self.element_types_stub.Create(
            element_types_pb2.CreateElementTypeRequest(name=name)
        )
        return ElementType.from_protobuf_model(proto=response)

    def get_element_type_by_name(self, name: str) -> ElementType:
        response: element_types_pb2.ElementType = self.element_types_stub.GetByName(
            element_types_pb2.GetElementTypeByNameRequest(name=name)
        )
        return ElementType.from_protobuf_model(proto=response)
