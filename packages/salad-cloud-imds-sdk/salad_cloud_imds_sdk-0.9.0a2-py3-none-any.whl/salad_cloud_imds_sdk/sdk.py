from .services.metadata import MetadataService
from .net.environment import Environment


class SaladCloudImdsSdk:
    def __init__(self, base_url: str = Environment.DEFAULT.value, timeout: int = 60000):
        """
        Initializes SaladCloudImdsSdk the SDK class.
        """

        self.metadata = MetadataService(base_url=base_url)
        self.set_timeout(timeout)

    def set_base_url(self, base_url):
        """
        Sets the base URL for the entire SDK.
        """
        self.metadata.set_base_url(base_url)

        return self

    def set_timeout(self, timeout: int):
        """
        Sets the timeout for the entire SDK.

        :param int timeout: The timeout (ms) to be set.
        :return: The SDK instance.
        """
        self.metadata.set_timeout(timeout)

        return self


# c029837e0e474b76bc487506e8799df5e3335891efe4fb02bda7a1441840310c
