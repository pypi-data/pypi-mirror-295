from typing import Any
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..models.utils.cast_models import cast_models
from ..models.reallocate_container import ReallocateContainer
from ..models.container_token import ContainerToken
from ..models.container_status import ContainerStatus


class MetadataService(BaseService):

    @cast_models
    def reallocate_container(self, request_body: ReallocateContainer) -> Any:
        """Reallocates the running container to another Salad Node

        :param request_body: The request body.
        :type request_body: ReallocateContainer
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(ReallocateContainer).validate(request_body)

        serialized_request = (
            Serializer(f"{self.base_url}/v1/reallocate", self.get_default_headers())
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response = self.send_request(serialized_request)
        return response

    @cast_models
    def get_container_status(self) -> ContainerStatus:
        """Gets the health statuses of the running container

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ContainerStatus
        """

        serialized_request = (
            Serializer(f"{self.base_url}/v1/status", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return ContainerStatus._unmap(response)

    @cast_models
    def get_container_token(self) -> ContainerToken:
        """Gets the identity token of the running container

        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: OK
        :rtype: ContainerToken
        """

        serialized_request = (
            Serializer(f"{self.base_url}/v1/token", self.get_default_headers())
            .serialize()
            .set_method("GET")
        )

        response = self.send_request(serialized_request)
        return ContainerToken._unmap(response)
