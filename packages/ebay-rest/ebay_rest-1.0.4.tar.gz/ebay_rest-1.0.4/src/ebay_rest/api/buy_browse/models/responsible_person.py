# coding: utf-8

"""
    Browse API

    The Browse API has the following resources:<ul><li><b>item_summary:</b><br>Allows shoppers to search for specific items by keyword, GTIN, category, charity, product, image, or item aspects and refine the results by using filters, such as aspects, compatibility, and fields values, or UI parameters.</li><li><b>item:</b><br>Allows shoppers to retrieve the details of a specific item or all items in an item group, which is an item with variations such as color and size and check if a product is compatible with the specified item, such as if a specific car is compatible with a specific part.<br><br>This resource also provides a bridge between the eBay legacy APIs, such as the <a href=\"/api-docs/user-guides/static/finding-user-guide-landing.html\" target=\"_blank\">Finding</b>, and the RESTful APIs, which use different formats for the item IDs.</li></ul>The <b>item_summary</b>, <b>search_by_image</b>, and <b>item</b> resource calls require an <a href=\"/api-docs/static/oauth-client-credentials-grant.html\" target=\"_blank\">Application access token</a>.  # noqa: E501

    OpenAPI spec version: v1.19.8
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ResponsiblePerson(object):
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
        'company_name': 'str',
        'country': 'str',
        'country_name': 'str',
        'county': 'str',
        'email': 'str',
        'phone': 'str',
        'postal_code': 'str',
        'state_or_province': 'str',
        'types': 'list[str]'
    }

    attribute_map = {
        'address_line1': 'addressLine1',
        'address_line2': 'addressLine2',
        'city': 'city',
        'company_name': 'companyName',
        'country': 'country',
        'country_name': 'countryName',
        'county': 'county',
        'email': 'email',
        'phone': 'phone',
        'postal_code': 'postalCode',
        'state_or_province': 'stateOrProvince',
        'types': 'types'
    }

    def __init__(self, address_line1=None, address_line2=None, city=None, company_name=None, country=None, country_name=None, county=None, email=None, phone=None, postal_code=None, state_or_province=None, types=None):  # noqa: E501
        """ResponsiblePerson - a model defined in Swagger"""  # noqa: E501
        self._address_line1 = None
        self._address_line2 = None
        self._city = None
        self._company_name = None
        self._country = None
        self._country_name = None
        self._county = None
        self._email = None
        self._phone = None
        self._postal_code = None
        self._state_or_province = None
        self._types = None
        self.discriminator = None
        if address_line1 is not None:
            self.address_line1 = address_line1
        if address_line2 is not None:
            self.address_line2 = address_line2
        if city is not None:
            self.city = city
        if company_name is not None:
            self.company_name = company_name
        if country is not None:
            self.country = country
        if country_name is not None:
            self.country_name = country_name
        if county is not None:
            self.county = county
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if postal_code is not None:
            self.postal_code = postal_code
        if state_or_province is not None:
            self.state_or_province = state_or_province
        if types is not None:
            self.types = types

    @property
    def address_line1(self):
        """Gets the address_line1 of this ResponsiblePerson.  # noqa: E501

        The first line of the Responsible Person's street address.  # noqa: E501

        :return: The address_line1 of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._address_line1

    @address_line1.setter
    def address_line1(self, address_line1):
        """Sets the address_line1 of this ResponsiblePerson.

        The first line of the Responsible Person's street address.  # noqa: E501

        :param address_line1: The address_line1 of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._address_line1 = address_line1

    @property
    def address_line2(self):
        """Gets the address_line2 of this ResponsiblePerson.  # noqa: E501

        The second line of the Responsible Person's address. This field is not always used, but can be used for secondary address information such as 'Suite Number' or 'Apt Number'.  # noqa: E501

        :return: The address_line2 of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._address_line2

    @address_line2.setter
    def address_line2(self, address_line2):
        """Sets the address_line2 of this ResponsiblePerson.

        The second line of the Responsible Person's address. This field is not always used, but can be used for secondary address information such as 'Suite Number' or 'Apt Number'.  # noqa: E501

        :param address_line2: The address_line2 of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._address_line2 = address_line2

    @property
    def city(self):
        """Gets the city of this ResponsiblePerson.  # noqa: E501

        The city of the Responsible Person's street address.  # noqa: E501

        :return: The city of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this ResponsiblePerson.

        The city of the Responsible Person's street address.  # noqa: E501

        :param city: The city of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def company_name(self):
        """Gets the company_name of this ResponsiblePerson.  # noqa: E501

        The name of the the Responsible Person or entity.  # noqa: E501

        :return: The company_name of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._company_name

    @company_name.setter
    def company_name(self, company_name):
        """Sets the company_name of this ResponsiblePerson.

        The name of the the Responsible Person or entity.  # noqa: E501

        :param company_name: The company_name of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._company_name = company_name

    @property
    def country(self):
        """Gets the country of this ResponsiblePerson.  # noqa: E501

        The two-letter <a href=\"https://www.iso.org/iso-3166-country-codes.html \" target=\"_blank\">ISO 3166</a> standard of the country of the address. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/buy/browse/types/ba:CountryCodeEnum'>eBay API documentation</a>  # noqa: E501

        :return: The country of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this ResponsiblePerson.

        The two-letter <a href=\"https://www.iso.org/iso-3166-country-codes.html \" target=\"_blank\">ISO 3166</a> standard of the country of the address. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/buy/browse/types/ba:CountryCodeEnum'>eBay API documentation</a>  # noqa: E501

        :param country: The country of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def country_name(self):
        """Gets the country_name of this ResponsiblePerson.  # noqa: E501

        The country name of the Responsible Person's street address.  # noqa: E501

        :return: The country_name of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._country_name

    @country_name.setter
    def country_name(self, country_name):
        """Sets the country_name of this ResponsiblePerson.

        The country name of the Responsible Person's street address.  # noqa: E501

        :param country_name: The country_name of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._country_name = country_name

    @property
    def county(self):
        """Gets the county of this ResponsiblePerson.  # noqa: E501

        The county of the Responsible Person's street address.  # noqa: E501

        :return: The county of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._county

    @county.setter
    def county(self, county):
        """Sets the county of this ResponsiblePerson.

        The county of the Responsible Person's street address.  # noqa: E501

        :param county: The county of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._county = county

    @property
    def email(self):
        """Gets the email of this ResponsiblePerson.  # noqa: E501

        The email of the Responsible Person's street address.  # noqa: E501

        :return: The email of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this ResponsiblePerson.

        The email of the Responsible Person's street address.  # noqa: E501

        :param email: The email of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def phone(self):
        """Gets the phone of this ResponsiblePerson.  # noqa: E501

        The phone number of the Responsible Person's street address.  # noqa: E501

        :return: The phone of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this ResponsiblePerson.

        The phone number of the Responsible Person's street address.  # noqa: E501

        :param phone: The phone of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def postal_code(self):
        """Gets the postal_code of this ResponsiblePerson.  # noqa: E501

        The postal code of the Responsible Person's street address.  # noqa: E501

        :return: The postal_code of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._postal_code

    @postal_code.setter
    def postal_code(self, postal_code):
        """Sets the postal_code of this ResponsiblePerson.

        The postal code of the Responsible Person's street address.  # noqa: E501

        :param postal_code: The postal_code of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._postal_code = postal_code

    @property
    def state_or_province(self):
        """Gets the state_or_province of this ResponsiblePerson.  # noqa: E501

        The state or province of the Responsible Person's street address.  # noqa: E501

        :return: The state_or_province of this ResponsiblePerson.  # noqa: E501
        :rtype: str
        """
        return self._state_or_province

    @state_or_province.setter
    def state_or_province(self, state_or_province):
        """Sets the state_or_province of this ResponsiblePerson.

        The state or province of the Responsible Person's street address.  # noqa: E501

        :param state_or_province: The state_or_province of this ResponsiblePerson.  # noqa: E501
        :type: str
        """

        self._state_or_province = state_or_province

    @property
    def types(self):
        """Gets the types of this ResponsiblePerson.  # noqa: E501

        The type(s) associated with the Responsible Person or entity.  # noqa: E501

        :return: The types of this ResponsiblePerson.  # noqa: E501
        :rtype: list[str]
        """
        return self._types

    @types.setter
    def types(self, types):
        """Sets the types of this ResponsiblePerson.

        The type(s) associated with the Responsible Person or entity.  # noqa: E501

        :param types: The types of this ResponsiblePerson.  # noqa: E501
        :type: list[str]
        """

        self._types = types

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
        if issubclass(ResponsiblePerson, dict):
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
        if not isinstance(other, ResponsiblePerson):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
