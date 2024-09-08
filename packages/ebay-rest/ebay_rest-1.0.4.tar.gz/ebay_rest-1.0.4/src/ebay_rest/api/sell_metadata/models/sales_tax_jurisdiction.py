# coding: utf-8

"""
    Metadata API

    The Metadata API has operations that retrieve configuration details pertaining to the different eBay marketplaces. In addition to marketplace information, the API also has operations that get information that helps sellers list items on eBay.  # noqa: E501

    OpenAPI spec version: v1.8.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class SalesTaxJurisdiction(object):
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
        'sales_tax_jurisdiction_id': 'str'
    }

    attribute_map = {
        'sales_tax_jurisdiction_id': 'salesTaxJurisdictionId'
    }

    def __init__(self, sales_tax_jurisdiction_id=None):  # noqa: E501
        """SalesTaxJurisdiction - a model defined in Swagger"""  # noqa: E501
        self._sales_tax_jurisdiction_id = None
        self.discriminator = None
        if sales_tax_jurisdiction_id is not None:
            self.sales_tax_jurisdiction_id = sales_tax_jurisdiction_id

    @property
    def sales_tax_jurisdiction_id(self):
        """Gets the sales_tax_jurisdiction_id of this SalesTaxJurisdiction.  # noqa: E501

        The unique ID for a sales-tax jurisdiction.<br><br><div class=\"msgbox_important\"><p class=\"msgbox_importantInDiv\" data-mc-autonum=\"&lt;b&gt;&lt;span style=&quot;color: #dd1e31;&quot; class=&quot;mcFormatColor&quot;&gt;Important! &lt;/span&gt;&lt;/b&gt;\"><span class=\"autonumber\"><span><b><span style=\"color: #dd1e31;\" class=\"mcFormatColor\">Important!</span></b></span></span> When <code>countryCode</code> is set to <code>US</code>, IDs for all 50 states, Washington, DC, and all US territories will be returned. However, the only <code>salesTaxJurisdictionId</code> values currently supported are:<ul><li><code>AS</code> (American Samoa)</li><li><code>GU</code> (Guam</li><li><code>MP</code> Northern Mariana Islands</li><li><code>PW (Palau)</li><li><code>VI</code> (US Virgin Islands)</li></ul></p></div>  # noqa: E501

        :return: The sales_tax_jurisdiction_id of this SalesTaxJurisdiction.  # noqa: E501
        :rtype: str
        """
        return self._sales_tax_jurisdiction_id

    @sales_tax_jurisdiction_id.setter
    def sales_tax_jurisdiction_id(self, sales_tax_jurisdiction_id):
        """Sets the sales_tax_jurisdiction_id of this SalesTaxJurisdiction.

        The unique ID for a sales-tax jurisdiction.<br><br><div class=\"msgbox_important\"><p class=\"msgbox_importantInDiv\" data-mc-autonum=\"&lt;b&gt;&lt;span style=&quot;color: #dd1e31;&quot; class=&quot;mcFormatColor&quot;&gt;Important! &lt;/span&gt;&lt;/b&gt;\"><span class=\"autonumber\"><span><b><span style=\"color: #dd1e31;\" class=\"mcFormatColor\">Important!</span></b></span></span> When <code>countryCode</code> is set to <code>US</code>, IDs for all 50 states, Washington, DC, and all US territories will be returned. However, the only <code>salesTaxJurisdictionId</code> values currently supported are:<ul><li><code>AS</code> (American Samoa)</li><li><code>GU</code> (Guam</li><li><code>MP</code> Northern Mariana Islands</li><li><code>PW (Palau)</li><li><code>VI</code> (US Virgin Islands)</li></ul></p></div>  # noqa: E501

        :param sales_tax_jurisdiction_id: The sales_tax_jurisdiction_id of this SalesTaxJurisdiction.  # noqa: E501
        :type: str
        """

        self._sales_tax_jurisdiction_id = sales_tax_jurisdiction_id

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
        if issubclass(SalesTaxJurisdiction, dict):
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
        if not isinstance(other, SalesTaxJurisdiction):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
