from .utils.json_map import JsonMap
from .utils.base_model import BaseModel


@JsonMap({})
class ReallocateContainer(BaseModel):
    """Represents a request to reallocate a container.

    :param reason: The reason for reallocating the container. This value is reported to SaladCloud support for quality assurance of Salad Nodes.
    :type reason: str
    """

    def __init__(self, reason: str):
        """Represents a request to reallocate a container.

        :param reason: The reason for reallocating the container. This value is reported to SaladCloud support for quality assurance of Salad Nodes.
        :type reason: str
        """
        self.reason = self._define_str("reason", reason, min_length=1, max_length=1000)
