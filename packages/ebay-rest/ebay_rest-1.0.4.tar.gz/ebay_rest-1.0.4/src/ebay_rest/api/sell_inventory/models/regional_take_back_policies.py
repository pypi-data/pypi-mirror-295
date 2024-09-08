# coding: utf-8

"""
    Inventory API

    The Inventory API is used to create and manage inventory, and then to publish and manage this inventory on an eBay marketplace. There are also methods in this API that will convert eligible, active eBay listings into the Inventory API model.  # noqa: E501

    OpenAPI spec version: 1.17.6
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class RegionalTakeBackPolicies(object):
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
        'country_policies': 'list[CountryPolicy]'
    }

    attribute_map = {
        'country_policies': 'countryPolicies'
    }

    def __init__(self, country_policies=None):  # noqa: E501
        """RegionalTakeBackPolicies - a model defined in Swagger"""  # noqa: E501
        self._country_policies = None
        self.discriminator = None
        if country_policies is not None:
            self.country_policies = country_policies

    @property
    def country_policies(self):
        """Gets the country_policies of this RegionalTakeBackPolicies.  # noqa: E501

        The array of country-specific take-back policies to be used by an offer when it is published and converted to a listing.  # noqa: E501

        :return: The country_policies of this RegionalTakeBackPolicies.  # noqa: E501
        :rtype: list[CountryPolicy]
        """
        return self._country_policies

    @country_policies.setter
    def country_policies(self, country_policies):
        """Sets the country_policies of this RegionalTakeBackPolicies.

        The array of country-specific take-back policies to be used by an offer when it is published and converted to a listing.  # noqa: E501

        :param country_policies: The country_policies of this RegionalTakeBackPolicies.  # noqa: E501
        :type: list[CountryPolicy]
        """

        self._country_policies = country_policies

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
        if issubclass(RegionalTakeBackPolicies, dict):
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
        if not isinstance(other, RegionalTakeBackPolicies):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
