# coding: utf-8

"""
    Fulfillment API

    Use the Fulfillment API to complete the process of packaging, addressing, handling, and shipping each order on behalf of the seller, in accordance with the payment method and timing specified at checkout.  # noqa: E501

    OpenAPI spec version: v1.20.4
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TaxIdentifier(object):
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
        'taxpayer_id': 'str',
        'tax_identifier_type': 'str',
        'issuing_country': 'str'
    }

    attribute_map = {
        'taxpayer_id': 'taxpayerId',
        'tax_identifier_type': 'taxIdentifierType',
        'issuing_country': 'issuingCountry'
    }

    def __init__(self, taxpayer_id=None, tax_identifier_type=None, issuing_country=None):  # noqa: E501
        """TaxIdentifier - a model defined in Swagger"""  # noqa: E501
        self._taxpayer_id = None
        self._tax_identifier_type = None
        self._issuing_country = None
        self.discriminator = None
        if taxpayer_id is not None:
            self.taxpayer_id = taxpayer_id
        if tax_identifier_type is not None:
            self.tax_identifier_type = tax_identifier_type
        if issuing_country is not None:
            self.issuing_country = issuing_country

    @property
    def taxpayer_id(self):
        """Gets the taxpayer_id of this TaxIdentifier.  # noqa: E501

        This value is the unique tax ID associated with the buyer. The type of tax identification is shown in the <strong>taxIdentifierType</strong> field.  # noqa: E501

        :return: The taxpayer_id of this TaxIdentifier.  # noqa: E501
        :rtype: str
        """
        return self._taxpayer_id

    @taxpayer_id.setter
    def taxpayer_id(self, taxpayer_id):
        """Sets the taxpayer_id of this TaxIdentifier.

        This value is the unique tax ID associated with the buyer. The type of tax identification is shown in the <strong>taxIdentifierType</strong> field.  # noqa: E501

        :param taxpayer_id: The taxpayer_id of this TaxIdentifier.  # noqa: E501
        :type: str
        """

        self._taxpayer_id = taxpayer_id

    @property
    def tax_identifier_type(self):
        """Gets the tax_identifier_type of this TaxIdentifier.  # noqa: E501

        This enumeration value indicates the type of tax identification being used for the buyer. The different tax types are defined in the <strong>TaxIdentifierTypeEnum</strong> type. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/fulfillment/types/sel:TaxIdentifierTypeEnum'>eBay API documentation</a>  # noqa: E501

        :return: The tax_identifier_type of this TaxIdentifier.  # noqa: E501
        :rtype: str
        """
        return self._tax_identifier_type

    @tax_identifier_type.setter
    def tax_identifier_type(self, tax_identifier_type):
        """Sets the tax_identifier_type of this TaxIdentifier.

        This enumeration value indicates the type of tax identification being used for the buyer. The different tax types are defined in the <strong>TaxIdentifierTypeEnum</strong> type. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/fulfillment/types/sel:TaxIdentifierTypeEnum'>eBay API documentation</a>  # noqa: E501

        :param tax_identifier_type: The tax_identifier_type of this TaxIdentifier.  # noqa: E501
        :type: str
        """

        self._tax_identifier_type = tax_identifier_type

    @property
    def issuing_country(self):
        """Gets the issuing_country of this TaxIdentifier.  # noqa: E501

        This two-letter code indicates the country that issued the buyer's tax ID. The country that the two-letter code represents can be found in the <strong>CountryCodeEnum</strong> type, or in the  <a href=\"https://www.iso.org/iso-3166-country-codes.html \">ISO 3166</a> standard. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/fulfillment/types/ba:CountryCodeEnum'>eBay API documentation</a>  # noqa: E501

        :return: The issuing_country of this TaxIdentifier.  # noqa: E501
        :rtype: str
        """
        return self._issuing_country

    @issuing_country.setter
    def issuing_country(self, issuing_country):
        """Sets the issuing_country of this TaxIdentifier.

        This two-letter code indicates the country that issued the buyer's tax ID. The country that the two-letter code represents can be found in the <strong>CountryCodeEnum</strong> type, or in the  <a href=\"https://www.iso.org/iso-3166-country-codes.html \">ISO 3166</a> standard. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/fulfillment/types/ba:CountryCodeEnum'>eBay API documentation</a>  # noqa: E501

        :param issuing_country: The issuing_country of this TaxIdentifier.  # noqa: E501
        :type: str
        """

        self._issuing_country = issuing_country

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
        if issubclass(TaxIdentifier, dict):
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
        if not isinstance(other, TaxIdentifier):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
