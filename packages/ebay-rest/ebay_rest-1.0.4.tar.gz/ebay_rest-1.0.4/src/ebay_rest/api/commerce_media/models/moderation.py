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

class Moderation(object):
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
        'reject_reasons': 'list[str]'
    }

    attribute_map = {
        'reject_reasons': 'rejectReasons'
    }

    def __init__(self, reject_reasons=None):  # noqa: E501
        """Moderation - a model defined in Swagger"""  # noqa: E501
        self._reject_reasons = None
        self.discriminator = None
        if reject_reasons is not None:
            self.reject_reasons = reject_reasons

    @property
    def reject_reasons(self):
        """Gets the reject_reasons of this Moderation.  # noqa: E501

        The reason(s) why the specified video was blocked by moderators.  # noqa: E501

        :return: The reject_reasons of this Moderation.  # noqa: E501
        :rtype: list[str]
        """
        return self._reject_reasons

    @reject_reasons.setter
    def reject_reasons(self, reject_reasons):
        """Sets the reject_reasons of this Moderation.

        The reason(s) why the specified video was blocked by moderators.  # noqa: E501

        :param reject_reasons: The reject_reasons of this Moderation.  # noqa: E501
        :type: list[str]
        """

        self._reject_reasons = reject_reasons

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
        if issubclass(Moderation, dict):
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
        if not isinstance(other, Moderation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
