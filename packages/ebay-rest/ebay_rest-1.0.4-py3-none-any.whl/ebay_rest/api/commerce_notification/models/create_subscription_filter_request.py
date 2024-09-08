# coding: utf-8

"""
    Notification API

    The eBay Notification API enables management of the entire end-to-end eBay notification experience by allowing users to:<ul><li>Browse for supported notification topics and retrieve topic details</li><li>Create, configure, and manage notification destination endpoints</li><li>Configure, manage, and test notification subscriptions</li><li>Process eBay notifications and verify the integrity of the message payload</li></ul>  # noqa: E501

    OpenAPI spec version: v1.6.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CreateSubscriptionFilterRequest(object):
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
        'filter_schema': 'dict(str, object)'
    }

    attribute_map = {
        'filter_schema': 'filterSchema'
    }

    def __init__(self, filter_schema=None):  # noqa: E501
        """CreateSubscriptionFilterRequest - a model defined in Swagger"""  # noqa: E501
        self._filter_schema = None
        self.discriminator = None
        if filter_schema is not None:
            self.filter_schema = filter_schema

    @property
    def filter_schema(self):
        """Gets the filter_schema of this CreateSubscriptionFilterRequest.  # noqa: E501

        The content of a subscription filter as a valid <a href=\"https://json-schema.org \" target=\"_blank\">JSON Schema Core document</a> (version 2020-12 or later). The <strong>filterSchema</strong> provided must describe the subscription's notification payload such that it supplies valid criteria to filter the subscription's notifications.<br><br><span class=\"tablenote\"><b>Note:</b> Not all topics can have filters applied to them. Use <a href=\"/api-docs/commerce/notification/resources/topic/methods/getTopic\">getTopic</a> and <a href=\"/api-docs/commerce/notification/resources/topic/methods/getTopics\">getTopics</a> requests to determine if a specific topic is filterable. Filterable topics have the boolean <b>filterable</b> returned as <code>true</code> in the response.</span><br><span class=\"tablenote\"><b>Note:</b> If the JSON supplied as a subscription filter specifies a field that does not exist in the notifications for a topic, or if the topic is not filterable, the filter will be rejected and become <strong>DISABLED</strong>. If it is valid, however, the filter will move from <strong>PENDING</strong> status to <strong>ENABLED</strong> status.</span><br>Initially, when the <b>createSubscriptionFilter</b> request has been made, if the request has a valid JSON body a <b>201&nbsp;Created</b> is returned. After that, the validation of the <b>filterSchema</b> happens. See <a href=\"/api-docs/commerce/notification/overview.html#create-filter\" target=\"_blank\">Creating a subscription filter for a topic</a> for additional information.  # noqa: E501

        :return: The filter_schema of this CreateSubscriptionFilterRequest.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._filter_schema

    @filter_schema.setter
    def filter_schema(self, filter_schema):
        """Sets the filter_schema of this CreateSubscriptionFilterRequest.

        The content of a subscription filter as a valid <a href=\"https://json-schema.org \" target=\"_blank\">JSON Schema Core document</a> (version 2020-12 or later). The <strong>filterSchema</strong> provided must describe the subscription's notification payload such that it supplies valid criteria to filter the subscription's notifications.<br><br><span class=\"tablenote\"><b>Note:</b> Not all topics can have filters applied to them. Use <a href=\"/api-docs/commerce/notification/resources/topic/methods/getTopic\">getTopic</a> and <a href=\"/api-docs/commerce/notification/resources/topic/methods/getTopics\">getTopics</a> requests to determine if a specific topic is filterable. Filterable topics have the boolean <b>filterable</b> returned as <code>true</code> in the response.</span><br><span class=\"tablenote\"><b>Note:</b> If the JSON supplied as a subscription filter specifies a field that does not exist in the notifications for a topic, or if the topic is not filterable, the filter will be rejected and become <strong>DISABLED</strong>. If it is valid, however, the filter will move from <strong>PENDING</strong> status to <strong>ENABLED</strong> status.</span><br>Initially, when the <b>createSubscriptionFilter</b> request has been made, if the request has a valid JSON body a <b>201&nbsp;Created</b> is returned. After that, the validation of the <b>filterSchema</b> happens. See <a href=\"/api-docs/commerce/notification/overview.html#create-filter\" target=\"_blank\">Creating a subscription filter for a topic</a> for additional information.  # noqa: E501

        :param filter_schema: The filter_schema of this CreateSubscriptionFilterRequest.  # noqa: E501
        :type: dict(str, object)
        """

        self._filter_schema = filter_schema

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
        if issubclass(CreateSubscriptionFilterRequest, dict):
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
        if not isinstance(other, CreateSubscriptionFilterRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
