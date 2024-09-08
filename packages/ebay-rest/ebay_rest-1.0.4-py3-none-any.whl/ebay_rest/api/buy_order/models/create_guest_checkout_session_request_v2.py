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

class CreateGuestCheckoutSessionRequestV2(object):
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
        'contact_email': 'str',
        'line_item_inputs': 'list[LineItemInput]',
        'shipping_address': 'ShippingAddress'
    }

    attribute_map = {
        'contact_email': 'contactEmail',
        'line_item_inputs': 'lineItemInputs',
        'shipping_address': 'shippingAddress'
    }

    def __init__(self, contact_email=None, line_item_inputs=None, shipping_address=None):  # noqa: E501
        """CreateGuestCheckoutSessionRequestV2 - a model defined in Swagger"""  # noqa: E501
        self._contact_email = None
        self._line_item_inputs = None
        self._shipping_address = None
        self.discriminator = None
        if contact_email is not None:
            self.contact_email = contact_email
        if line_item_inputs is not None:
            self.line_item_inputs = line_item_inputs
        if shipping_address is not None:
            self.shipping_address = shipping_address

    @property
    def contact_email(self):
        """Gets the contact_email of this CreateGuestCheckoutSessionRequestV2.  # noqa: E501

        The buyer's email address.  # noqa: E501

        :return: The contact_email of this CreateGuestCheckoutSessionRequestV2.  # noqa: E501
        :rtype: str
        """
        return self._contact_email

    @contact_email.setter
    def contact_email(self, contact_email):
        """Sets the contact_email of this CreateGuestCheckoutSessionRequestV2.

        The buyer's email address.  # noqa: E501

        :param contact_email: The contact_email of this CreateGuestCheckoutSessionRequestV2.  # noqa: E501
        :type: str
        """

        self._contact_email = contact_email

    @property
    def line_item_inputs(self):
        """Gets the line_item_inputs of this CreateGuestCheckoutSessionRequestV2.  # noqa: E501

        An array used to define the line item(s) and desired quantity for an eBay guest checkout session.<br><br><b>Maximum:</b> 10 line items  # noqa: E501

        :return: The line_item_inputs of this CreateGuestCheckoutSessionRequestV2.  # noqa: E501
        :rtype: list[LineItemInput]
        """
        return self._line_item_inputs

    @line_item_inputs.setter
    def line_item_inputs(self, line_item_inputs):
        """Sets the line_item_inputs of this CreateGuestCheckoutSessionRequestV2.

        An array used to define the line item(s) and desired quantity for an eBay guest checkout session.<br><br><b>Maximum:</b> 10 line items  # noqa: E501

        :param line_item_inputs: The line_item_inputs of this CreateGuestCheckoutSessionRequestV2.  # noqa: E501
        :type: list[LineItemInput]
        """

        self._line_item_inputs = line_item_inputs

    @property
    def shipping_address(self):
        """Gets the shipping_address of this CreateGuestCheckoutSessionRequestV2.  # noqa: E501


        :return: The shipping_address of this CreateGuestCheckoutSessionRequestV2.  # noqa: E501
        :rtype: ShippingAddress
        """
        return self._shipping_address

    @shipping_address.setter
    def shipping_address(self, shipping_address):
        """Sets the shipping_address of this CreateGuestCheckoutSessionRequestV2.


        :param shipping_address: The shipping_address of this CreateGuestCheckoutSessionRequestV2.  # noqa: E501
        :type: ShippingAddress
        """

        self._shipping_address = shipping_address

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
        if issubclass(CreateGuestCheckoutSessionRequestV2, dict):
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
        if not isinstance(other, CreateGuestCheckoutSessionRequestV2):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
