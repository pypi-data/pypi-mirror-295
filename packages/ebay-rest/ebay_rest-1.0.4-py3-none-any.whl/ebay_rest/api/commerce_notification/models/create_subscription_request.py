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

class CreateSubscriptionRequest(object):
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
        'destination_id': 'str',
        'payload': 'SubscriptionPayloadDetail',
        'status': 'str',
        'topic_id': 'str'
    }

    attribute_map = {
        'destination_id': 'destinationId',
        'payload': 'payload',
        'status': 'status',
        'topic_id': 'topicId'
    }

    def __init__(self, destination_id=None, payload=None, status=None, topic_id=None):  # noqa: E501
        """CreateSubscriptionRequest - a model defined in Swagger"""  # noqa: E501
        self._destination_id = None
        self._payload = None
        self._status = None
        self._topic_id = None
        self.discriminator = None
        if destination_id is not None:
            self.destination_id = destination_id
        if payload is not None:
            self.payload = payload
        if status is not None:
            self.status = status
        if topic_id is not None:
            self.topic_id = topic_id

    @property
    def destination_id(self):
        """Gets the destination_id of this CreateSubscriptionRequest.  # noqa: E501

        The unique identifier of the destination endpoint that will receive notifications associated with this subscription. Use the <b>getDestinations</b> method to retrieve destination IDs.  # noqa: E501

        :return: The destination_id of this CreateSubscriptionRequest.  # noqa: E501
        :rtype: str
        """
        return self._destination_id

    @destination_id.setter
    def destination_id(self, destination_id):
        """Sets the destination_id of this CreateSubscriptionRequest.

        The unique identifier of the destination endpoint that will receive notifications associated with this subscription. Use the <b>getDestinations</b> method to retrieve destination IDs.  # noqa: E501

        :param destination_id: The destination_id of this CreateSubscriptionRequest.  # noqa: E501
        :type: str
        """

        self._destination_id = destination_id

    @property
    def payload(self):
        """Gets the payload of this CreateSubscriptionRequest.  # noqa: E501


        :return: The payload of this CreateSubscriptionRequest.  # noqa: E501
        :rtype: SubscriptionPayloadDetail
        """
        return self._payload

    @payload.setter
    def payload(self, payload):
        """Sets the payload of this CreateSubscriptionRequest.


        :param payload: The payload of this CreateSubscriptionRequest.  # noqa: E501
        :type: SubscriptionPayloadDetail
        """

        self._payload = payload

    @property
    def status(self):
        """Gets the status of this CreateSubscriptionRequest.  # noqa: E501

        Set the status of the subscription to <code>ENABLED</code> or <code>DISABLED</code>. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/commerce/notification/types/api:SubscriptionStatusEnum'>eBay API documentation</a>  # noqa: E501

        :return: The status of this CreateSubscriptionRequest.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this CreateSubscriptionRequest.

        Set the status of the subscription to <code>ENABLED</code> or <code>DISABLED</code>. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/commerce/notification/types/api:SubscriptionStatusEnum'>eBay API documentation</a>  # noqa: E501

        :param status: The status of this CreateSubscriptionRequest.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def topic_id(self):
        """Gets the topic_id of this CreateSubscriptionRequest.  # noqa: E501

        The unique identifier of the notification topic to subscribe to. Use <b>getTopics</b> to get topic IDs.  # noqa: E501

        :return: The topic_id of this CreateSubscriptionRequest.  # noqa: E501
        :rtype: str
        """
        return self._topic_id

    @topic_id.setter
    def topic_id(self, topic_id):
        """Sets the topic_id of this CreateSubscriptionRequest.

        The unique identifier of the notification topic to subscribe to. Use <b>getTopics</b> to get topic IDs.  # noqa: E501

        :param topic_id: The topic_id of this CreateSubscriptionRequest.  # noqa: E501
        :type: str
        """

        self._topic_id = topic_id

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
        if issubclass(CreateSubscriptionRequest, dict):
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
        if not isinstance(other, CreateSubscriptionRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
