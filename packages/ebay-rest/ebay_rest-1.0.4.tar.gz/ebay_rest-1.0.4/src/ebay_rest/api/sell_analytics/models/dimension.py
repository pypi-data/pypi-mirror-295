# coding: utf-8

"""
     Seller Service Metrics API 

    The <i>Analytics API</i> provides data and information about a seller and their eBay business.  <br><br>The resources and methods in this API let sellers review information on their listing performance, metrics on their customer service performance, and details on their eBay seller performance rating.  <br><br>The three resources in the Analytics API provide the following data and information: <ul><li><b>Customer Service Metric</b> &ndash; Returns benchmark data and a metric rating pertaining to a seller's customer service performance as compared to other seller's in the same peer group.</li> <li><b>Traffic Report</b> &ndash; Returns data and information that shows how buyers are engaging with a seller's listings.</li> <li><b>Seller Standards Profile</b> &ndash; Returns information pertaining to a seller's profile rating.</li></ul> Sellers can use the data and information returned by the various Analytics API methods to determine where they can make improvements to increase sales and how they might improve their seller status as viewed by eBay buyers.  <br><br>For details on using this API, see <a href=\"/api-docs/sell/static/performance/analyzing-performance.html\" title=\"Selling Integration Guide\">Analyzing seller performance</a>.  # noqa: E501

    OpenAPI spec version: 1.3.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Dimension(object):
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
        'dimension_key': 'str',
        'name': 'str',
        'value': 'str'
    }

    attribute_map = {
        'dimension_key': 'dimensionKey',
        'name': 'name',
        'value': 'value'
    }

    def __init__(self, dimension_key=None, name=None, value=None):  # noqa: E501
        """Dimension - a model defined in Swagger"""  # noqa: E501
        self._dimension_key = None
        self._name = None
        self._value = None
        self.discriminator = None
        if dimension_key is not None:
            self.dimension_key = dimension_key
        if name is not None:
            self.name = name
        if value is not None:
            self.value = value

    @property
    def dimension_key(self):
        """Gets the dimension_key of this Dimension.  # noqa: E501

        <b>dimensionKey</b> defines the basis against which the seller's customer service metric is measured.  <br><br>The value of this field gets set according to the value of the <b>customer_service_metric_type</b> input parameter. The following input configurations return the responses shown: <ul><li><code>ITEM_NOT_AS_DESCRIBED</code> &ndash; Returns benchmark ratings based on L1 listing categories, so the result shows metrics where the <b>dimensionKey</b> is set to <code>LISTING_CATEGORY</code>.</li>  <li><code>ITEM_NOT_RECEIVED</code> &ndash; Returns benchmark ratings based on world shipping regions, so the result shows metrics where the <b>dimensionKey</b> is set to <code>SHIPPING_REGION</code>.  <br><br>The shipping region is indicated by the associated <b>value</b> field. For specifics on world shipping regions, see the FAQ section on the following page: <a href=\"https://www.ebay.com/help/selling/selling/monitor-service-metrics?id=4785\" title=\"eBay Help page\" target=\"_blank\">Monitor your service metrics</a></li></ul> For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/analytics/types/api:DimensionTypeEnum'>eBay API documentation</a>  # noqa: E501

        :return: The dimension_key of this Dimension.  # noqa: E501
        :rtype: str
        """
        return self._dimension_key

    @dimension_key.setter
    def dimension_key(self, dimension_key):
        """Sets the dimension_key of this Dimension.

        <b>dimensionKey</b> defines the basis against which the seller's customer service metric is measured.  <br><br>The value of this field gets set according to the value of the <b>customer_service_metric_type</b> input parameter. The following input configurations return the responses shown: <ul><li><code>ITEM_NOT_AS_DESCRIBED</code> &ndash; Returns benchmark ratings based on L1 listing categories, so the result shows metrics where the <b>dimensionKey</b> is set to <code>LISTING_CATEGORY</code>.</li>  <li><code>ITEM_NOT_RECEIVED</code> &ndash; Returns benchmark ratings based on world shipping regions, so the result shows metrics where the <b>dimensionKey</b> is set to <code>SHIPPING_REGION</code>.  <br><br>The shipping region is indicated by the associated <b>value</b> field. For specifics on world shipping regions, see the FAQ section on the following page: <a href=\"https://www.ebay.com/help/selling/selling/monitor-service-metrics?id=4785\" title=\"eBay Help page\" target=\"_blank\">Monitor your service metrics</a></li></ul> For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/analytics/types/api:DimensionTypeEnum'>eBay API documentation</a>  # noqa: E501

        :param dimension_key: The dimension_key of this Dimension.  # noqa: E501
        :type: str
        """

        self._dimension_key = dimension_key

    @property
    def name(self):
        """Gets the name of this Dimension.  # noqa: E501

        The dimension name returned in this field depends on the <b>dimensionKey</b>: <ul><li>If  <b>dimensionKey</b> is set to <code>SHIPPING_REGION</code>, this field is set to one of following values, which represent established shipping corridors: <ul><li><code>Domestic</code></li> <li><code>International: Mature region</code></li> <li><code>International: Emerging region</code></li></ul></li>  <li>If <b>dimensionKey</b> is set to <code>LISTING_CATEGORY</code>, this field is set to the name of the primary (L1) category in which the items being rated were listed.</li></ul>  # noqa: E501

        :return: The name of this Dimension.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Dimension.

        The dimension name returned in this field depends on the <b>dimensionKey</b>: <ul><li>If  <b>dimensionKey</b> is set to <code>SHIPPING_REGION</code>, this field is set to one of following values, which represent established shipping corridors: <ul><li><code>Domestic</code></li> <li><code>International: Mature region</code></li> <li><code>International: Emerging region</code></li></ul></li>  <li>If <b>dimensionKey</b> is set to <code>LISTING_CATEGORY</code>, this field is set to the name of the primary (L1) category in which the items being rated were listed.</li></ul>  # noqa: E501

        :param name: The name of this Dimension.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def value(self):
        """Gets the value of this Dimension.  # noqa: E501

        The value returned in this field depends on the <b>dimensionKey</b>.  <br><br>If <b>dimensionKey</b> equals <code>LISTING_CATEGORY</code>, the value returned in this field is the category ID of the primary (L1) category in which the items being rated were listed.  <br><br>If <b>dimensionKey</b> equals <code>SHIPPING_REGION</code>, one of the following values is returned:  <ul><li><code>DOMESTIC</code></li> <li><code>INTERNATIONAL_MATURED_REGION</code></li> <li><code>INTERNATIONAL_EMERGING_REGION</code></li></ul>  # noqa: E501

        :return: The value of this Dimension.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this Dimension.

        The value returned in this field depends on the <b>dimensionKey</b>.  <br><br>If <b>dimensionKey</b> equals <code>LISTING_CATEGORY</code>, the value returned in this field is the category ID of the primary (L1) category in which the items being rated were listed.  <br><br>If <b>dimensionKey</b> equals <code>SHIPPING_REGION</code>, one of the following values is returned:  <ul><li><code>DOMESTIC</code></li> <li><code>INTERNATIONAL_MATURED_REGION</code></li> <li><code>INTERNATIONAL_EMERGING_REGION</code></li></ul>  # noqa: E501

        :param value: The value of this Dimension.  # noqa: E501
        :type: str
        """

        self._value = value

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
        if issubclass(Dimension, dict):
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
        if not isinstance(other, Dimension):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
