from typing import Callable

import google.protobuf.empty_pb2 as empty_pb2
import grpc

from orchestra._internals.common.models.basemodels import PydObjectId
import orchestra._internals.rpc.orchestra.elements_pb2 as elements_pb2
import orchestra._internals.rpc.orchestra.element_types_pb2 as element_types_pb2
from orchestra._internals.rpc.orchestra import element_types_pb2_grpc
from orchestra._internals.rpc.orchestra import elements_pb2_grpc
from orchestra._internals.watcher.watcher import Watcher

from orchestra.elements.models.element import Element
from orchestra.elements.models.element_type import ElementType


class OrchestraElementInterface:
    def __init__(self, channel: grpc.Channel):
        self.elements_stub = elements_pb2_grpc.ElementsServiceStub(channel)
        self.element_types_stub = element_types_pb2_grpc.ElementTypesServiceStub(channel)

    def get_element(self, element_id: PydObjectId) -> Element:
        # TODO: exception handling
        response: elements_pb2.Element = self.elements_stub.Get(
            elements_pb2.GetElementRequest(id=str(element_id))
        )
        return Element.from_protobuf_model(proto=response)

    def get_element_type(self, element_type_id: PydObjectId) -> ElementType:
        # TODO: exception handling
        response: element_types_pb2.ElementType = self.element_types_stub.Get(
            element_types_pb2.GetElementTypeRequest(
                id=element_types_pb2.ElementTypeIdentifier(element_type_id=str(element_type_id))
            )
        )
        return ElementType.from_protobuf_model(proto=response)

    def create_element(self, name: str, element_type_id: PydObjectId) -> Element:
        # TODO: exception handling
        response: elements_pb2.Element = self.elements_stub.Create(
            elements_pb2.CreateElementRequest(name=name, element_type_id=str(element_type_id))
        )
        return Element.from_protobuf_model(proto=response)

    def get_element_type_by_element_id(self, element_id: PydObjectId) -> ElementType:
        # TODO: exception handling
        # TODO: implement this better
        element: Element = self.get_element(element_id=element_id)
        return self.get_element_type(element_type_id=element.element_type_id)

    def delete_element(self, element_id: PydObjectId) -> None:
        # TODO: exception handling
        response: empty_pb2.Empty = self.elements_stub.Delete(
            elements_pb2.DeleteElementRequest(id=str(element_id))
        )

    def make_element_watcher(
        self, element_id: PydObjectId, callback: Callable[[str, str], None]
    ) -> Callable[[], None]:
        def _callback(response: elements_pb2.WatchElementResponse) -> None:
            callback(response.twin_id, response.type)

        watcher: Watcher = Watcher(
            rpc=self.elements_stub.Watch,
            proto_request=elements_pb2.WatchElementRequest(id=str(element_id)),
            callback=_callback,
        )

        return watcher.cancel
