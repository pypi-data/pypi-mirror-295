# coding: utf-8

"""
    Charity API

    The Charity API allows third-party developers to search for and access details on supported charitable organizations.  # noqa: E501

    OpenAPI spec version: v1.2.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Location(object):
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
        'address': 'Address',
        'geo_coordinates': 'GeoCoordinates'
    }

    attribute_map = {
        'address': 'address',
        'geo_coordinates': 'geoCoordinates'
    }

    def __init__(self, address=None, geo_coordinates=None):  # noqa: E501
        """Location - a model defined in Swagger"""  # noqa: E501
        self._address = None
        self._geo_coordinates = None
        self.discriminator = None
        if address is not None:
            self.address = address
        if geo_coordinates is not None:
            self.geo_coordinates = geo_coordinates

    @property
    def address(self):
        """Gets the address of this Location.  # noqa: E501


        :return: The address of this Location.  # noqa: E501
        :rtype: Address
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Location.


        :param address: The address of this Location.  # noqa: E501
        :type: Address
        """

        self._address = address

    @property
    def geo_coordinates(self):
        """Gets the geo_coordinates of this Location.  # noqa: E501


        :return: The geo_coordinates of this Location.  # noqa: E501
        :rtype: GeoCoordinates
        """
        return self._geo_coordinates

    @geo_coordinates.setter
    def geo_coordinates(self, geo_coordinates):
        """Sets the geo_coordinates of this Location.


        :param geo_coordinates: The geo_coordinates of this Location.  # noqa: E501
        :type: GeoCoordinates
        """

        self._geo_coordinates = geo_coordinates

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
        if issubclass(Location, dict):
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
        if not isinstance(other, Location):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
