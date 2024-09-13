from datetime import datetime, timezone
from typing import Generator, Iterable, Optional, Tuple, List, Dict

import google.protobuf.empty_pb2 as empty_pb2
import grpc
from pydantic import NonNegativeInt

from orchestra._internals.common.models.basemodels import PydObjectId
from orchestra._internals.common.models.granularity import TimeseriesGranularity
from orchestra._internals.common.models.pagination import Pagination
from orchestra._internals.common.models.sort import Sort
import orchestra._internals.common.utils as utils
import orchestra._internals.rpc.orchestra.element_telemetry_pb2 as element_telemetry_pb2
import orchestra._internals.rpc.orchestra.pagination_pb2 as pagination_pb2
from orchestra._internals.rpc.orchestra import element_telemetry_pb2_grpc

from orchestra.elements.models.element_telemetry import (
    AggregateTelemetryResult,
    ElementTelemetry,
    MultipleElementTelemetry,
    SingleElementTelemetry,
)


class OrchestraTelemetryInterface:
    def __init__(self, channel: grpc.Channel):
        self.element_telemetry_stub = element_telemetry_pb2_grpc.ElementTelemetryServiceStub(
            channel
        )

    def get_telemetry(
        self,
        element_id: PydObjectId,
        ts_from: datetime,
        ts_to: datetime,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
    ) -> List[Tuple[datetime, dict]]:
        # TODO: exception handling
        response: Generator[element_telemetry_pb2.GetElementTelemetryResponse, None, None] = (
            self.element_telemetry_stub.Get(
                element_telemetry_pb2.GetElementTelemetryRequest(
                    element_id=str(element_id),
                    ts_from=utils._get_pb2_timestamp_from_datetime(ts_from),
                    ts_to=utils._get_pb2_timestamp_from_datetime(ts_to),
                    sort=Sort.to_protobuf_model(ts_sort),
                    granularity=granularity.to_protobuf_model() if granularity else None,
                )
            )
        )

        result: Optional[element_telemetry_pb2.GetElementTelemetryResponse] = None

        for item in response:
            if result == None:
                result = element_telemetry_pb2.GetElementTelemetryResponse(
                    element_id=item.element_id,
                    telemetry=item.telemetry,
                    pagination=item.pagination,
                )
            else:
                result.telemetry.extend(item.telemetry)

        return [SingleElementTelemetry.to_tuple(proto_model=x) for x in result.telemetry]

    def get_telemetry_paginated(
        self,
        element_id: PydObjectId,
        ts_from: datetime,
        ts_to: datetime,
        limit: NonNegativeInt,
        offset: NonNegativeInt,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
    ) -> Tuple[List[Tuple[datetime, dict]], Pagination]:
        # TODO: exception handling
        response: Generator[element_telemetry_pb2.GetElementTelemetryResponse, None, None] = (
            self.element_telemetry_stub.Get(
                element_telemetry_pb2.GetElementTelemetryRequest(
                    element_id=str(element_id),
                    ts_from=utils._get_pb2_timestamp_from_datetime(ts_from),
                    ts_to=utils._get_pb2_timestamp_from_datetime(ts_to),
                    pagination=pagination_pb2.PaginationRequest(limit=limit, offset=offset),
                    sort=Sort.to_protobuf_model(ts_sort),
                    granularity=granularity.to_protobuf_model() if granularity else None,
                )
            )
        )

        result: Optional[element_telemetry_pb2.GetElementTelemetryResponse] = None

        for item in response:
            if result == None:
                result = element_telemetry_pb2.GetElementTelemetryResponse(
                    element_id=item.element_id,
                    telemetry=item.telemetry,
                    pagination=item.pagination,
                )
            else:
                result.telemetry.extend(item.telemetry)

        return (
            [SingleElementTelemetry.to_tuple(x) for x in result.telemetry],
            Pagination.from_protobuf_model(proto_model=result.pagination),
        )

    def get_many_telemetry(
        self,
        element_ids: Iterable[PydObjectId],
        ts_from: datetime,
        ts_to: datetime,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
    ) -> Dict[PydObjectId, List[Tuple[datetime, dict]]]:
        # TODO: exception handling
        response: Generator[element_telemetry_pb2.GetManyElementTelemetryResponse, None, None] = (
            self.element_telemetry_stub.GetMany(
                element_telemetry_pb2.GetManyElementTelemetryRequest(
                    element_ids=[str(id) for id in element_ids],
                    ts_from=utils._get_pb2_timestamp_from_datetime(ts_from),
                    ts_to=utils._get_pb2_timestamp_from_datetime(ts_to),
                    sort=Sort.to_protobuf_model(ts_sort),
                    granularity=granularity.to_protobuf_model() if granularity else None,
                )
            )
        )

        result: Optional[element_telemetry_pb2.GetManyElementTelemetryResponse] = None

        for item in response:
            if result == None:
                result = element_telemetry_pb2.GetManyElementTelemetryResponse(
                    element_ids=item.element_ids,
                    telemetry=item.telemetry,
                    pagination=item.pagination,
                )
            else:
                result.telemetry.extend(item.telemetry)

        ret: Dict[PydObjectId, List[Tuple[datetime, dict]]] = {
            PydObjectId(element_id): [] for element_id in element_ids
        }

        for doc in result.telemetry:
            ret[PydObjectId(doc.element_id)].append(MultipleElementTelemetry.to_tuple(doc))
        return ret

    def get_many_telemetry_paginated(
        self,
        element_ids: Iterable[PydObjectId],
        ts_from: datetime,
        ts_to: datetime,
        limit: NonNegativeInt,
        offset: NonNegativeInt,
        ts_sort: Sort = Sort.ASCENDING,
        granularity: Optional[TimeseriesGranularity] = None,
    ) -> Tuple[List[Tuple[PydObjectId, datetime, dict]], Pagination]:
        # TODO: exception handling
        response: Generator[element_telemetry_pb2.GetManyElementTelemetryResponse, None, None] = (
            self.element_telemetry_stub.GetMany(
                element_telemetry_pb2.GetManyElementTelemetryRequest(
                    element_ids=[str(id) for id in element_ids],
                    ts_from=utils._get_pb2_timestamp_from_datetime(ts_from),
                    ts_to=utils._get_pb2_timestamp_from_datetime(ts_to),
                    pagination=pagination_pb2.PaginationRequest(limit=limit, offset=offset),
                    sort=Sort.to_protobuf_model(ts_sort),
                    granularity=granularity.to_protobuf_model() if granularity else None,
                )
            )
        )

        result: Optional[element_telemetry_pb2.GetManyElementTelemetryResponse] = None

        for item in response:
            if result == None:
                result = element_telemetry_pb2.GetManyElementTelemetryResponse(
                    element_ids=item.element_ids,
                    telemetry=item.telemetry,
                    pagination=item.pagination,
                )
            else:
                result.telemetry.extend(item.telemetry)

        return (
            [MultipleElementTelemetry.to_tuple(x) for x in result.telemetry],
            Pagination.from_protobuf_model(proto_model=result.pagination),
        )

    def get_latest_telemetry_by_element_id(
        self, element_id: PydObjectId, ts_upper_bound: Optional[datetime] = None
    ) -> Tuple[datetime, dict]:
        # TODO: exception handling
        request = element_telemetry_pb2.GetLatestElementTelemetryRequest()
        request.element_id = str(element_id)
        if ts_upper_bound:
            request.ts_upper_bound = utils._get_pb2_timestamp_from_datetime(ts_upper_bound)
        response: element_telemetry_pb2.GetLatestElementTelemetryResponse = (
            self.element_telemetry_stub.GetLatest(request)
        )
        return SingleElementTelemetry.to_tuple(response.telemetry)

    def get_many_latest_telemetry_by_element_ids(
        self, element_ids: Iterable[PydObjectId], ts_upper_bound: Optional[datetime] = None
    ) -> Dict[PydObjectId, Tuple[datetime, dict]]:
        # TODO: exception handling
        request = element_telemetry_pb2.GetManyLatestElementTelemetryRequest(
            element_ids=[str(id) for id in element_ids]
        )
        if ts_upper_bound:
            request.ts_upper_bound = utils._get_pb2_timestamp_from_datetime(ts_upper_bound)
        response: Generator[
            element_telemetry_pb2.GetManyLatestElementTelemetryResponse, None, None
        ] = self.element_telemetry_stub.GetManyLatest(request)
        # TODO: handle missing telemetry? it's part of exception handling though
        # due to API behaviour of crashing if not all telemetry is available

        result: Optional[element_telemetry_pb2.GetManyLatestElementTelemetryResponse] = None

        for item in response:
            if result == None:
                result = element_telemetry_pb2.GetManyLatestElementTelemetryResponse(
                    telemetry=item.telemetry
                )
            else:
                result.telemetry.extend(item.telemetry)

        return {
            PydObjectId(x.element_id): SingleElementTelemetry.to_tuple(x.telemetry)
            for x in result.telemetry
        }

    def push_telemetry(
        self, element_id: PydObjectId, data: dict, ts: Optional[datetime] = None
    ) -> PydObjectId:
        # TODO: exception handling
        response: element_telemetry_pb2.PushElementTelemetryResponse = (
            self.element_telemetry_stub.Push(
                ElementTelemetry(
                    element_id=element_id,
                    ts=ts if ts else datetime.now(timezone.utc),
                    data=data,
                ).to_protobuf_model_push_request()
            )
        )
        return PydObjectId(response.document_id)

    def push_batch_telemetry(
        self, element_id: PydObjectId, data: Iterable[Tuple[datetime, dict]]
    ) -> None:
        # TODO: exception handling
        data: List[Tuple[datetime, dict]] = list(data)
        data.sort(key=lambda x: x[0])
        response: empty_pb2.Empty = self.element_telemetry_stub.PushMany(
            element_telemetry_pb2.PushManyElementTelemetryRequest(
                element_id=str(element_id),
                telemetry=[
                    ElementTelemetry(
                        element_id=element_id, ts=x, data=y
                    ).to_protobuf_model_single_element()
                    for x, y in data
                ],
            )
        )

    def aggregate(self, pipeline: List[Dict]) -> AggregateTelemetryResult:
        # TODO: exception handling
        response: Generator[element_telemetry_pb2.GetAggregatedTelemetryResponse, None, None] = (
            self.element_telemetry_stub.Aggregate(
                element_telemetry_pb2.GetAggregatedTelemetryRequest(
                    pipeline=[utils._get_pb2_struct(prop=p) for p in pipeline]
                )
            )
        )
        result: Optional[element_telemetry_pb2.GetAggregatedTelemetryResponse] = None
        for item in response:
            if result == None:
                result = element_telemetry_pb2.GetAggregatedTelemetryResponse(result=item.result)
            else:
                result.result.extend(item.result)

        return AggregateTelemetryResult.from_protobuf_model(result)
