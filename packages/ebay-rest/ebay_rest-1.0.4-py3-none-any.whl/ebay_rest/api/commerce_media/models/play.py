# coding: utf-8

"""
    Media API

    The <b>Media API</b> lets sellers to create, upload, and retrieve files, including:<ul><li>videos</li><li>documents (for GPSR regulations)</li></ul>  # noqa: E501

    OpenAPI spec version: v1_beta.2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Play(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'play_url': 'str',
        'protocol': 'str'
    }

    attribute_map = {
        'play_url': 'playUrl',
        'protocol': 'protocol'
    }

    def __init__(self, play_url=None, protocol=None):  # noqa: E501
        """Play - a model defined in Swagger"""  # noqa: E501
        self._play_url = None
        self._protocol = None
        self.discriminator = None
        if play_url is not None:
            self.play_url = play_url
        if protocol is not None:
            self.protocol = protocol

    @property
    def play_url(self):
        """Gets the play_url of this Play.  # noqa: E501

        The playable URL for this video.  # noqa: E501

        :return: The play_url of this Play.  # noqa: E501
        :rtype: str
        """
        return self._play_url

    @play_url.setter
    def play_url(self, play_url):
        """Sets the play_url of this Play.

        The playable URL for this video.  # noqa: E501

        :param play_url: The play_url of this Play.  # noqa: E501
        :type: str
        """

        self._play_url = play_url

    @property
    def protocol(self):
        """Gets the protocol of this Play.  # noqa: E501

        The protocol for the video playlist. Supported protocols are DASH (Dynamic Adaptive Streaming over HTTP) and HLS (HTTP Live Streaming). For implementation help, refer to <a href='https://developer.ebay.com/api-docs/commerce/media/types/api:ProtocolEnum'>eBay API documentation</a>  # noqa: E501

        :return: The protocol of this Play.  # noqa: E501
        :rtype: str
        """
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        """Sets the protocol of this Play.

        The protocol for the video playlist. Supported protocols are DASH (Dynamic Adaptive Streaming over HTTP) and HLS (HTTP Live Streaming). For implementation help, refer to <a href='https://developer.ebay.com/api-docs/commerce/media/types/api:ProtocolEnum'>eBay API documentation</a>  # noqa: E501

        :param protocol: The protocol of this Play.  # noqa: E501
        :type: str
        """

        self._protocol = protocol

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Play, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Play):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
