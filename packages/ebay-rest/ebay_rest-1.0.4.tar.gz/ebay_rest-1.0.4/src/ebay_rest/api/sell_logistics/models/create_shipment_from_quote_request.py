# coding: utf-8

"""
    Logistics API

    <span class=\"tablenote\"><b>Note:</b> This is a <a href=\"https://developer.ebay.com/api-docs/static/versioning.html#limited \" target=\"_blank\"> <img src=\"/cms/img/docs/partners-api.svg\" class=\"legend-icon partners-icon\" title=\"Limited Release\"  alt=\"Limited Release\" />(Limited Release)</a> API available only to select developers approved by business units.</span><br /><br />The <b>Logistics API</b> resources offer the following capabilities: <ul><li><b>shipping_quote</b> &ndash; Consolidates into a list a set of live shipping rates, or quotes, from which you can select a rate to ship a package.</li> <li><b>shipment</b> &ndash; Creates a \"shipment\" for the selected shipping rate.</li></ul> Call <b>createShippingQuote</b> to get a list of live shipping rates. The rates returned are all valid for a specific time window and all quoted prices are at eBay-negotiated rates. <br><br>Select one of the live rates and using its associated <b>rateId</b>, create a \"shipment\" for the package by calling <b>createFromShippingQuote</b>. Creating a shipment completes an agreement, and the cost of the base service and any added shipping options are summed into the returned <b>totalShippingCost</b> value. This action also generates a shipping label that you can use to ship the package.  The total cost of the shipment is incurred when the package is shipped using the supplied shipping label.  <p class=\"tablenote\"><b>Important!</b> Sellers must set up a payment method via their eBay account before they can use the methods in this API to create a shipment and the associated shipping label.</p>  # noqa: E501

    OpenAPI spec version: v1_beta.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CreateShipmentFromQuoteRequest(object):
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
        'additional_options': 'list[AdditionalOption]',
        'label_custom_message': 'str',
        'label_size': 'str',
        'rate_id': 'str',
        'return_to': 'Contact',
        'shipping_quote_id': 'str'
    }

    attribute_map = {
        'additional_options': 'additionalOptions',
        'label_custom_message': 'labelCustomMessage',
        'label_size': 'labelSize',
        'rate_id': 'rateId',
        'return_to': 'returnTo',
        'shipping_quote_id': 'shippingQuoteId'
    }

    def __init__(self, additional_options=None, label_custom_message=None, label_size=None, rate_id=None, return_to=None, shipping_quote_id=None):  # noqa: E501
        """CreateShipmentFromQuoteRequest - a model defined in Swagger"""  # noqa: E501
        self._additional_options = None
        self._label_custom_message = None
        self._label_size = None
        self._rate_id = None
        self._return_to = None
        self._shipping_quote_id = None
        self.discriminator = None
        if additional_options is not None:
            self.additional_options = additional_options
        if label_custom_message is not None:
            self.label_custom_message = label_custom_message
        if label_size is not None:
            self.label_size = label_size
        if rate_id is not None:
            self.rate_id = rate_id
        if return_to is not None:
            self.return_to = return_to
        if shipping_quote_id is not None:
            self.shipping_quote_id = shipping_quote_id

    @property
    def additional_options(self):
        """Gets the additional_options of this CreateShipmentFromQuoteRequest.  # noqa: E501

        Supply a list of one or more shipping options that the seller wants to purchase for this shipment.  <br><br>The <b>baseShippingCost</b> field that's associated with the selected shipping rate is the cost of the base service offered in the rate. In addition to the base service, sellers can add additional shipping services to the base service. Shipping options include things such as shipping insurance or a recipient's signature upon delivery. The cost of any added services is summed with the base shipping cost to determine the final cost for the shipment. All options added to the shipment must be chosen from the set of shipping options offered with the selected rate.  # noqa: E501

        :return: The additional_options of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :rtype: list[AdditionalOption]
        """
        return self._additional_options

    @additional_options.setter
    def additional_options(self, additional_options):
        """Sets the additional_options of this CreateShipmentFromQuoteRequest.

        Supply a list of one or more shipping options that the seller wants to purchase for this shipment.  <br><br>The <b>baseShippingCost</b> field that's associated with the selected shipping rate is the cost of the base service offered in the rate. In addition to the base service, sellers can add additional shipping services to the base service. Shipping options include things such as shipping insurance or a recipient's signature upon delivery. The cost of any added services is summed with the base shipping cost to determine the final cost for the shipment. All options added to the shipment must be chosen from the set of shipping options offered with the selected rate.  # noqa: E501

        :param additional_options: The additional_options of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :type: list[AdditionalOption]
        """

        self._additional_options = additional_options

    @property
    def label_custom_message(self):
        """Gets the label_custom_message of this CreateShipmentFromQuoteRequest.  # noqa: E501

        Optional text to be printed on the shipping label if the selected shipping carrier supports custom messages on their labels.  # noqa: E501

        :return: The label_custom_message of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :rtype: str
        """
        return self._label_custom_message

    @label_custom_message.setter
    def label_custom_message(self, label_custom_message):
        """Sets the label_custom_message of this CreateShipmentFromQuoteRequest.

        Optional text to be printed on the shipping label if the selected shipping carrier supports custom messages on their labels.  # noqa: E501

        :param label_custom_message: The label_custom_message of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :type: str
        """

        self._label_custom_message = label_custom_message

    @property
    def label_size(self):
        """Gets the label_size of this CreateShipmentFromQuoteRequest.  # noqa: E501

        The seller's desired label size. Any supplied value is applied only if the shipping carrier supports multiple label sizes, otherwise the carrier's default label size is used.  <br><br>Currently, the only valid value is: <code>4\"x6\"</code>  # noqa: E501

        :return: The label_size of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :rtype: str
        """
        return self._label_size

    @label_size.setter
    def label_size(self, label_size):
        """Sets the label_size of this CreateShipmentFromQuoteRequest.

        The seller's desired label size. Any supplied value is applied only if the shipping carrier supports multiple label sizes, otherwise the carrier's default label size is used.  <br><br>Currently, the only valid value is: <code>4\"x6\"</code>  # noqa: E501

        :param label_size: The label_size of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :type: str
        """

        self._label_size = label_size

    @property
    def rate_id(self):
        """Gets the rate_id of this CreateShipmentFromQuoteRequest.  # noqa: E501

        The unique eBay-assigned identifier of the shipping rate that the seller selected for the shipment. This value is generated by using the <a href=\"/api-docs/sell/logistics/resources/shipping_quote/methods/createShippingQuote\" target=\"_blank\">createShippingQuote</a> method and is returned in the <b>rates.rateId</b> field.  # noqa: E501

        :return: The rate_id of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :rtype: str
        """
        return self._rate_id

    @rate_id.setter
    def rate_id(self, rate_id):
        """Sets the rate_id of this CreateShipmentFromQuoteRequest.

        The unique eBay-assigned identifier of the shipping rate that the seller selected for the shipment. This value is generated by using the <a href=\"/api-docs/sell/logistics/resources/shipping_quote/methods/createShippingQuote\" target=\"_blank\">createShippingQuote</a> method and is returned in the <b>rates.rateId</b> field.  # noqa: E501

        :param rate_id: The rate_id of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :type: str
        """

        self._rate_id = rate_id

    @property
    def return_to(self):
        """Gets the return_to of this CreateShipmentFromQuoteRequest.  # noqa: E501


        :return: The return_to of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :rtype: Contact
        """
        return self._return_to

    @return_to.setter
    def return_to(self, return_to):
        """Sets the return_to of this CreateShipmentFromQuoteRequest.


        :param return_to: The return_to of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :type: Contact
        """

        self._return_to = return_to

    @property
    def shipping_quote_id(self):
        """Gets the shipping_quote_id of this CreateShipmentFromQuoteRequest.  # noqa: E501

        The unique eBay-assigned identifier of the shipping quote that was generated by the <a href=\"/api-docs/sell/logistics/resources/shipping_quote/methods/createShippingQuote\" target=\"_blank\">createShippingQuote</a> method.  # noqa: E501

        :return: The shipping_quote_id of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :rtype: str
        """
        return self._shipping_quote_id

    @shipping_quote_id.setter
    def shipping_quote_id(self, shipping_quote_id):
        """Sets the shipping_quote_id of this CreateShipmentFromQuoteRequest.

        The unique eBay-assigned identifier of the shipping quote that was generated by the <a href=\"/api-docs/sell/logistics/resources/shipping_quote/methods/createShippingQuote\" target=\"_blank\">createShippingQuote</a> method.  # noqa: E501

        :param shipping_quote_id: The shipping_quote_id of this CreateShipmentFromQuoteRequest.  # noqa: E501
        :type: str
        """

        self._shipping_quote_id = shipping_quote_id

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
        if issubclass(CreateShipmentFromQuoteRequest, dict):
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
        if not isinstance(other, CreateShipmentFromQuoteRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
