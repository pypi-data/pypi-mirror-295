# coding: utf-8

"""
    Deal API

    <span class=\"tablenote\"><b>Note:</b> This is a <a href=\"https://developer.ebay.com/api-docs/static/versioning.html#limited\" target=\"_blank\"> <img src=\"/cms/img/docs/partners-api.svg\" class=\"legend-icon partners-icon\" title=\"Limited Release\"  alt=\"Limited Release\" />(Limited Release)</a> API available only to select developers approved by business units. For information on how to obtain access to this API in production, see the <a href=\"/../api-docs/buy/static/buy-requirements.html\" target=\"_blank\">Buy APIs Requirements</a>.</span><br /><br />This API allows third-party developers to search for and retrieve details about eBay deals and events, as well as the items associated with those deals and events.  # noqa: E501

    OpenAPI spec version: v1.3.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Coupon(object):
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
        'redemption_code': 'str',
        'terms': 'Terms'
    }

    attribute_map = {
        'redemption_code': 'redemptionCode',
        'terms': 'terms'
    }

    def __init__(self, redemption_code=None, terms=None):  # noqa: E501
        """Coupon - a model defined in Swagger"""  # noqa: E501
        self._redemption_code = None
        self._terms = None
        self.discriminator = None
        if redemption_code is not None:
            self.redemption_code = redemption_code
        if terms is not None:
            self.terms = terms

    @property
    def redemption_code(self):
        """Gets the redemption_code of this Coupon.  # noqa: E501

        The coupon code.  # noqa: E501

        :return: The redemption_code of this Coupon.  # noqa: E501
        :rtype: str
        """
        return self._redemption_code

    @redemption_code.setter
    def redemption_code(self, redemption_code):
        """Sets the redemption_code of this Coupon.

        The coupon code.  # noqa: E501

        :param redemption_code: The redemption_code of this Coupon.  # noqa: E501
        :type: str
        """

        self._redemption_code = redemption_code

    @property
    def terms(self):
        """Gets the terms of this Coupon.  # noqa: E501


        :return: The terms of this Coupon.  # noqa: E501
        :rtype: Terms
        """
        return self._terms

    @terms.setter
    def terms(self, terms):
        """Sets the terms of this Coupon.


        :param terms: The terms of this Coupon.  # noqa: E501
        :type: Terms
        """

        self._terms = terms

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
        if issubclass(Coupon, dict):
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
        if not isinstance(other, Coupon):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
