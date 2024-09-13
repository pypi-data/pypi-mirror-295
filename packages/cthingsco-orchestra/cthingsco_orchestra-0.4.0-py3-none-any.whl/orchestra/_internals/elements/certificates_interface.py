from typing import Optional

import grpc
from google.protobuf import empty_pb2

from orchestra._internals.rpc.orchestra import certificates_pb2
from orchestra._internals.rpc.orchestra import certificates_pb2_grpc
from orchestra._internals.rpc.orchestra import certificates_public_pb2
from orchestra._internals.rpc.orchestra import certificates_public_pb2_grpc


class OrchestraCertificatesInterface:
    def __init__(self, channel: grpc.Channel, public_channel: grpc.Channel):
        self.certificates_public_stub = certificates_public_pb2_grpc.CertificatesPublicServiceStub(
            public_channel
        )
        self.certificates_stub: Optional[certificates_pb2_grpc.CertificatesServiceStub] = None
        if channel:
            self.certificates_stub = certificates_pb2_grpc.CertificatesServiceStub(channel)

    def sign(self, csr_pem: str, token: str) -> certificates_public_pb2.CertificateSignResponse:
        response: certificates_public_pb2.CertificateSignResponse = (
            self.certificates_public_stub.Sign(
                certificates_public_pb2.CertificateSignRequest(
                    csr_pem=csr_pem,
                    token=token,
                )
            )
        )
        return response

    def revoke(self, certificate_pem: str) -> empty_pb2.Empty():
        certificates_pb2.CertificateRevokeRequest = self.certificates_stub.Revoke(
            certificates_pb2.CertificateRevokeRequest(
                certificate_pem=certificate_pem,
            )
        )
        return empty_pb2.Empty()
