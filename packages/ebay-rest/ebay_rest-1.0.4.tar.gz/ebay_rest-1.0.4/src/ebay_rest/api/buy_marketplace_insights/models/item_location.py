# coding: utf-8

"""
    Marketplace Insights API

    <span class=\"tablenote\"><b>Note:</b> This is a <a href=\"/api-docs/static/versioning.html#limited \" target=\"_blank\"> <img src=\"/cms/img/docs/partners-api.svg\" class=\"legend-icon partners-icon\" title=\"Limited Release\"  alt=\"Limited Release\" />(Limited Release)</a> API available only to select developers approved by business units. For information on how to obtain access to this API in production, see the <a href=\"/../api-docs/buy/static/buy-requirements.html\" target=\"_blank\">Buy APIs Requirements</a>.</span>  <p>The Marketplace Insights API provides the ability to search for sold items on eBay by keyword, GTIN, category, and product and returns the of sales history of those items.</p>  # noqa: E501

    OpenAPI spec version: v1_beta.2.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ItemLocation(object):
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
        'address_line1': 'str',
        'address_line2': 'str',
        'city': 'str',
        'country': 'str',
        'county': 'str',
        'postal_code': 'str',
        'state_or_province': 'str'
    }

    attribute_map = {
        'address_line1': 'addressLine1',
        'address_line2': 'addressLine2',
        'city': 'city',
        'country': 'country',
        'county': 'county',
        'postal_code': 'postalCode',
        'state_or_province': 'stateOrProvince'
    }

    def __init__(self, address_line1=None, address_line2=None, city=None, country=None, county=None, postal_code=None, state_or_province=None):  # noqa: E501
        """ItemLocation - a model defined in Swagger"""  # noqa: E501
        self._address_line1 = None
        self._address_line2 = None
        self._city = None
        self._country = None
        self._county = None
        self._postal_code = None
        self._state_or_province = None
        self.discriminator = None
        if address_line1 is not None:
            self.address_line1 = address_line1
        if address_line2 is not None:
            self.address_line2 = address_line2
        if city is not None:
            self.city = city
        if country is not None:
            self.country = country
        if county is not None:
            self.county = county
        if postal_code is not None:
            self.postal_code = postal_code
        if state_or_province is not None:
            self.state_or_province = state_or_province

    @property
    def address_line1(self):
        """Gets the address_line1 of this ItemLocation.  # noqa: E501

        The first line of the street address.  # noqa: E501

        :return: The address_line1 of this ItemLocation.  # noqa: E501
        :rtype: str
        """
        return self._address_line1

    @address_line1.setter
    def address_line1(self, address_line1):
        """Sets the address_line1 of this ItemLocation.

        The first line of the street address.  # noqa: E501

        :param address_line1: The address_line1 of this ItemLocation.  # noqa: E501
        :type: str
        """

        self._address_line1 = address_line1

    @property
    def address_line2(self):
        """Gets the address_line2 of this ItemLocation.  # noqa: E501

        The second line of the street address. This field may contain such values as an apartment or suite number.  # noqa: E501

        :return: The address_line2 of this ItemLocation.  # noqa: E501
        :rtype: str
        """
        return self._address_line2

    @address_line2.setter
    def address_line2(self, address_line2):
        """Sets the address_line2 of this ItemLocation.

        The second line of the street address. This field may contain such values as an apartment or suite number.  # noqa: E501

        :param address_line2: The address_line2 of this ItemLocation.  # noqa: E501
        :type: str
        """

        self._address_line2 = address_line2

    @property
    def city(self):
        """Gets the city of this ItemLocation.  # noqa: E501

        The city in which the item is located.   # noqa: E501

        :return: The city of this ItemLocation.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this ItemLocation.

        The city in which the item is located.   # noqa: E501

        :param city: The city of this ItemLocation.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def country(self):
        """Gets the country of this ItemLocation.  # noqa: E501

        The two-letter <a href=\"https://www.iso.org/iso-3166-country-codes.html \">ISO 3166</a> standard code that indicates the country in which the item is located.  For implementation help, refer to <a href='https://developer.ebay.com/api-docs/buy/marketplace_insights/types/ba:CountryCodeEnum'>eBay API documentation</a>  # noqa: E501

        :return: The country of this ItemLocation.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this ItemLocation.

        The two-letter <a href=\"https://www.iso.org/iso-3166-country-codes.html \">ISO 3166</a> standard code that indicates the country in which the item is located.  For implementation help, refer to <a href='https://developer.ebay.com/api-docs/buy/marketplace_insights/types/ba:CountryCodeEnum'>eBay API documentation</a>  # noqa: E501

        :param country: The country of this ItemLocation.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def county(self):
        """Gets the county of this ItemLocation.  # noqa: E501

        The county in which the item is located.  # noqa: E501

        :return: The county of this ItemLocation.  # noqa: E501
        :rtype: str
        """
        return self._county

    @county.setter
    def county(self, county):
        """Sets the county of this ItemLocation.

        The county in which the item is located.  # noqa: E501

        :param county: The county of this ItemLocation.  # noqa: E501
        :type: str
        """

        self._county = county

    @property
    def postal_code(self):
        """Gets the postal_code of this ItemLocation.  # noqa: E501

        The postal code (or zip code in US) where the item is located.<br> <br><span class=\"tablenote\"> <b>  Note: </b>Beginning in late January 2020, the displayed postal code will be masked to all users. Different countries will mask postal/zip codes in slightly different ways, but an example would be <code>951**</code>.</span>  # noqa: E501

        :return: The postal_code of this ItemLocation.  # noqa: E501
        :rtype: str
        """
        return self._postal_code

    @postal_code.setter
    def postal_code(self, postal_code):
        """Sets the postal_code of this ItemLocation.

        The postal code (or zip code in US) where the item is located.<br> <br><span class=\"tablenote\"> <b>  Note: </b>Beginning in late January 2020, the displayed postal code will be masked to all users. Different countries will mask postal/zip codes in slightly different ways, but an example would be <code>951**</code>.</span>  # noqa: E501

        :param postal_code: The postal_code of this ItemLocation.  # noqa: E501
        :type: str
        """

        self._postal_code = postal_code

    @property
    def state_or_province(self):
        """Gets the state_or_province of this ItemLocation.  # noqa: E501

        The state or province in which the item is located.  # noqa: E501

        :return: The state_or_province of this ItemLocation.  # noqa: E501
        :rtype: str
        """
        return self._state_or_province

    @state_or_province.setter
    def state_or_province(self, state_or_province):
        """Sets the state_or_province of this ItemLocation.

        The state or province in which the item is located.  # noqa: E501

        :param state_or_province: The state_or_province of this ItemLocation.  # noqa: E501
        :type: str
        """

        self._state_or_province = state_or_province

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
        if issubclass(ItemLocation, dict):
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
        if not isinstance(other, ItemLocation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
