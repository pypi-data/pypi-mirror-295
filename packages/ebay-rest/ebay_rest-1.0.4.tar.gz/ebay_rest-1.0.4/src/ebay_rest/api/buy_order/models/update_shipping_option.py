# coding: utf-8

"""
    Order API

    <span class=\"tablenote\"><b>Note:</b> The Order API (v2) currently only supports the guest payment/checkout flow. If you need to support member payment/checkout flow, use the <a href=\"/api-docs/buy/order_v1/resources/methods\">v1_beta version</a> of the Order API.</span><br><br><span class=\"tablenote\"><b>Note:</b> This is a <a href=\"https://developer.ebay.com/api-docs/static/versioning.html#limited\" target=\"_blank\"><img src=\"/cms/img/docs/partners-api.svg\" class=\"legend-icon partners-icon\"  alt=\"Limited Release\" title=\"Limited Release\" />(Limited Release)</a> API available only to select developers approved by business units.</span><br><br>The Order API provides interfaces that let shoppers pay for items. It also returns payment and shipping status of the order.  # noqa: E501

    OpenAPI spec version: v2.1.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class UpdateShippingOption(object):
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
        'line_item_id': 'str',
        'shipping_option_id': 'str'
    }

    attribute_map = {
        'line_item_id': 'lineItemId',
        'shipping_option_id': 'shippingOptionId'
    }

    def __init__(self, line_item_id=None, shipping_option_id=None):  # noqa: E501
        """UpdateShippingOption - a model defined in Swagger"""  # noqa: E501
        self._line_item_id = None
        self._shipping_option_id = None
        self.discriminator = None
        if line_item_id is not None:
            self.line_item_id = line_item_id
        if shipping_option_id is not None:
            self.shipping_option_id = shipping_option_id

    @property
    def line_item_id(self):
        """Gets the line_item_id of this UpdateShippingOption.  # noqa: E501

        A unique eBay-assigned ID value that identifies the line item in a checkout session.<br><br><b>For example:</b> <code>v1|2**********6|5**********4</code> or <code>v1|1**********9|0</code>.<br><br>For more information about item IDs for RESTful APIs, see <a href=\"/api-docs/buy/static/api-browse.html#Legacy\">Legacy API compatibility</a>  # noqa: E501

        :return: The line_item_id of this UpdateShippingOption.  # noqa: E501
        :rtype: str
        """
        return self._line_item_id

    @line_item_id.setter
    def line_item_id(self, line_item_id):
        """Sets the line_item_id of this UpdateShippingOption.

        A unique eBay-assigned ID value that identifies the line item in a checkout session.<br><br><b>For example:</b> <code>v1|2**********6|5**********4</code> or <code>v1|1**********9|0</code>.<br><br>For more information about item IDs for RESTful APIs, see <a href=\"/api-docs/buy/static/api-browse.html#Legacy\">Legacy API compatibility</a>  # noqa: E501

        :param line_item_id: The line_item_id of this UpdateShippingOption.  # noqa: E501
        :type: str
        """

        self._line_item_id = line_item_id

    @property
    def shipping_option_id(self):
        """Gets the shipping_option_id of this UpdateShippingOption.  # noqa: E501

        A unique identifier of the selected shipping option/method.  # noqa: E501

        :return: The shipping_option_id of this UpdateShippingOption.  # noqa: E501
        :rtype: str
        """
        return self._shipping_option_id

    @shipping_option_id.setter
    def shipping_option_id(self, shipping_option_id):
        """Sets the shipping_option_id of this UpdateShippingOption.

        A unique identifier of the selected shipping option/method.  # noqa: E501

        :param shipping_option_id: The shipping_option_id of this UpdateShippingOption.  # noqa: E501
        :type: str
        """

        self._shipping_option_id = shipping_option_id

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
        if issubclass(UpdateShippingOption, dict):
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
        if not isinstance(other, UpdateShippingOption):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
