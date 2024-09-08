# coding: utf-8

"""
    Recommendation API

    The <b>Recommendation API</b> returns information that sellers can use to optimize the configuration of their listings on eBay. <br><br>Currently, the API contains a single method, <b>findListingRecommendations</b>. This method provides information that sellers can use to configure Promoted Listings ad campaigns to maximize the visibility of their items in the eBay marketplace.  # noqa: E501

    OpenAPI spec version: v1.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class BidPercentages(object):
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
        'basis': 'str',
        'value': 'str'
    }

    attribute_map = {
        'basis': 'basis',
        'value': 'value'
    }

    def __init__(self, basis=None, value=None):  # noqa: E501
        """BidPercentages - a model defined in Swagger"""  # noqa: E501
        self._basis = None
        self._value = None
        self.discriminator = None
        if basis is not None:
            self.basis = basis
        if value is not None:
            self.value = value

    @property
    def basis(self):
        """Gets the basis of this BidPercentages.  # noqa: E501

        The basis by which the ad rate is calculated.<br /><br /><b>Valid Values:</b> <code>ITEM</code> and <code>TRENDING</code> For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/recommendation/types/api:Basis'>eBay API documentation</a>  # noqa: E501

        :return: The basis of this BidPercentages.  # noqa: E501
        :rtype: str
        """
        return self._basis

    @basis.setter
    def basis(self, basis):
        """Sets the basis of this BidPercentages.

        The basis by which the ad rate is calculated.<br /><br /><b>Valid Values:</b> <code>ITEM</code> and <code>TRENDING</code> For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/recommendation/types/api:Basis'>eBay API documentation</a>  # noqa: E501

        :param basis: The basis of this BidPercentages.  # noqa: E501
        :type: str
        """

        self._basis = basis

    @property
    def value(self):
        """Gets the value of this BidPercentages.  # noqa: E501

        The bid percentage data is a single precision value, as calculated by the associated basis. <p>In Promoted listings ad campaigns, the <b>bid percentage</b> (also known as the <i>ad rate</i>) is a user-defined value that sets the level that eBay raises the visibility of the listing in the marketplace. It is also the rate that is used to calculate the Promoted Listings fee.</p> <p><b>Minimum value:</b> 1.0 &nbsp; <b>Maximum value:</b> 100.0</p>  # noqa: E501

        :return: The value of this BidPercentages.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this BidPercentages.

        The bid percentage data is a single precision value, as calculated by the associated basis. <p>In Promoted listings ad campaigns, the <b>bid percentage</b> (also known as the <i>ad rate</i>) is a user-defined value that sets the level that eBay raises the visibility of the listing in the marketplace. It is also the rate that is used to calculate the Promoted Listings fee.</p> <p><b>Minimum value:</b> 1.0 &nbsp; <b>Maximum value:</b> 100.0</p>  # noqa: E501

        :param value: The value of this BidPercentages.  # noqa: E501
        :type: str
        """

        self._value = value

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
        if issubclass(BidPercentages, dict):
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
        if not isinstance(other, BidPercentages):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
