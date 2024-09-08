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

class PackageSpecification(object):
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
        'dimensions': 'Dimensions',
        'weight': 'Weight'
    }

    attribute_map = {
        'dimensions': 'dimensions',
        'weight': 'weight'
    }

    def __init__(self, dimensions=None, weight=None):  # noqa: E501
        """PackageSpecification - a model defined in Swagger"""  # noqa: E501
        self._dimensions = None
        self._weight = None
        self.discriminator = None
        if dimensions is not None:
            self.dimensions = dimensions
        if weight is not None:
            self.weight = weight

    @property
    def dimensions(self):
        """Gets the dimensions of this PackageSpecification.  # noqa: E501


        :return: The dimensions of this PackageSpecification.  # noqa: E501
        :rtype: Dimensions
        """
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dimensions):
        """Sets the dimensions of this PackageSpecification.


        :param dimensions: The dimensions of this PackageSpecification.  # noqa: E501
        :type: Dimensions
        """

        self._dimensions = dimensions

    @property
    def weight(self):
        """Gets the weight of this PackageSpecification.  # noqa: E501


        :return: The weight of this PackageSpecification.  # noqa: E501
        :rtype: Weight
        """
        return self._weight

    @weight.setter
    def weight(self, weight):
        """Sets the weight of this PackageSpecification.


        :param weight: The weight of this PackageSpecification.  # noqa: E501
        :type: Weight
        """

        self._weight = weight

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
        if issubclass(PackageSpecification, dict):
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
        if not isinstance(other, PackageSpecification):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
