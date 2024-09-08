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
        'geo_coordinates': 'GeoCoordinates',
        'location_id': 'str'
    }

    attribute_map = {
        'address': 'address',
        'geo_coordinates': 'geoCoordinates',
        'location_id': 'locationId'
    }

    def __init__(self, address=None, geo_coordinates=None, location_id=None):  # noqa: E501
        """Location - a model defined in Swagger"""  # noqa: E501
        self._address = None
        self._geo_coordinates = None
        self._location_id = None
        self.discriminator = None
        if address is not None:
            self.address = address
        if geo_coordinates is not None:
            self.geo_coordinates = geo_coordinates
        if location_id is not None:
            self.location_id = location_id

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

    @property
    def location_id(self):
        """Gets the location_id of this Location.  # noqa: E501

        A unique eBay-assigned ID for the location. <br><br> <span class=\"tablenote\"> <strong>Note:</strong> This field should not be confused with the seller-defined <b>merchantLocationKey</b> value. It is the <b>merchantLocationKey</b> value which is used to identify an inventory location when working with inventory location API calls. The <strong>locationId</strong> value is only used internally by eBay.</span>  # noqa: E501

        :return: The location_id of this Location.  # noqa: E501
        :rtype: str
        """
        return self._location_id

    @location_id.setter
    def location_id(self, location_id):
        """Sets the location_id of this Location.

        A unique eBay-assigned ID for the location. <br><br> <span class=\"tablenote\"> <strong>Note:</strong> This field should not be confused with the seller-defined <b>merchantLocationKey</b> value. It is the <b>merchantLocationKey</b> value which is used to identify an inventory location when working with inventory location API calls. The <strong>locationId</strong> value is only used internally by eBay.</span>  # noqa: E501

        :param location_id: The location_id of this Location.  # noqa: E501
        :type: str
        """

        self._location_id = location_id

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
