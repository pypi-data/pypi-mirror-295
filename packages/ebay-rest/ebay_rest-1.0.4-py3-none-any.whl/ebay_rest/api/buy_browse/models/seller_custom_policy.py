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

class SellerCustomPolicy(object):
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
        'description': 'str',
        'label': 'str',
        'type': 'str'
    }

    attribute_map = {
        'description': 'description',
        'label': 'label',
        'type': 'type'
    }

    def __init__(self, description=None, label=None, type=None):  # noqa: E501
        """SellerCustomPolicy - a model defined in Swagger"""  # noqa: E501
        self._description = None
        self._label = None
        self._type = None
        self.discriminator = None
        if description is not None:
            self.description = description
        if label is not None:
            self.label = label
        if type is not None:
            self.type = type

    @property
    def description(self):
        """Gets the description of this SellerCustomPolicy.  # noqa: E501

        The seller-defined description of the policy.  # noqa: E501

        :return: The description of this SellerCustomPolicy.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this SellerCustomPolicy.

        The seller-defined description of the policy.  # noqa: E501

        :param description: The description of this SellerCustomPolicy.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def label(self):
        """Gets the label of this SellerCustomPolicy.  # noqa: E501

        The seller-defined label for an individual custom policy.  # noqa: E501

        :return: The label of this SellerCustomPolicy.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this SellerCustomPolicy.

        The seller-defined label for an individual custom policy.  # noqa: E501

        :param label: The label of this SellerCustomPolicy.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def type(self):
        """Gets the type of this SellerCustomPolicy.  # noqa: E501

        The type of custom policy, such as PRODUCT_COMPLIANCE or TAKE_BACK. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/buy/browse/types/gct:SellerCustomPolicyTypeEnum'>eBay API documentation</a>  # noqa: E501

        :return: The type of this SellerCustomPolicy.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this SellerCustomPolicy.

        The type of custom policy, such as PRODUCT_COMPLIANCE or TAKE_BACK. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/buy/browse/types/gct:SellerCustomPolicyTypeEnum'>eBay API documentation</a>  # noqa: E501

        :param type: The type of this SellerCustomPolicy.  # noqa: E501
        :type: str
        """

        self._type = type

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
        if issubclass(SellerCustomPolicy, dict):
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
        if not isinstance(other, SellerCustomPolicy):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
