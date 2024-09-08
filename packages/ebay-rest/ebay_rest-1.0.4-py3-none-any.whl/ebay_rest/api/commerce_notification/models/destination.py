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

class Destination(object):
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
        'delivery_config': 'DeliveryConfig',
        'destination_id': 'str',
        'name': 'str',
        'status': 'str'
    }

    attribute_map = {
        'delivery_config': 'deliveryConfig',
        'destination_id': 'destinationId',
        'name': 'name',
        'status': 'status'
    }

    def __init__(self, delivery_config=None, destination_id=None, name=None, status=None):  # noqa: E501
        """Destination - a model defined in Swagger"""  # noqa: E501
        self._delivery_config = None
        self._destination_id = None
        self._name = None
        self._status = None
        self.discriminator = None
        if delivery_config is not None:
            self.delivery_config = delivery_config
        if destination_id is not None:
            self.destination_id = destination_id
        if name is not None:
            self.name = name
        if status is not None:
            self.status = status

    @property
    def delivery_config(self):
        """Gets the delivery_config of this Destination.  # noqa: E501


        :return: The delivery_config of this Destination.  # noqa: E501
        :rtype: DeliveryConfig
        """
        return self._delivery_config

    @delivery_config.setter
    def delivery_config(self, delivery_config):
        """Sets the delivery_config of this Destination.


        :param delivery_config: The delivery_config of this Destination.  # noqa: E501
        :type: DeliveryConfig
        """

        self._delivery_config = delivery_config

    @property
    def destination_id(self):
        """Gets the destination_id of this Destination.  # noqa: E501

        The unique identifier for the destination.  # noqa: E501

        :return: The destination_id of this Destination.  # noqa: E501
        :rtype: str
        """
        return self._destination_id

    @destination_id.setter
    def destination_id(self, destination_id):
        """Sets the destination_id of this Destination.

        The unique identifier for the destination.  # noqa: E501

        :param destination_id: The destination_id of this Destination.  # noqa: E501
        :type: str
        """

        self._destination_id = destination_id

    @property
    def name(self):
        """Gets the name of this Destination.  # noqa: E501

        The name associated with this destination.  # noqa: E501

        :return: The name of this Destination.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Destination.

        The name associated with this destination.  # noqa: E501

        :param name: The name of this Destination.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def status(self):
        """Gets the status of this Destination.  # noqa: E501

        The status for this destination.<br><br><span class=\"tablenote\"><b>Note:</b> The <b>MARKED_DOWN</b> value is set by eBay systems and cannot be used in a create or update call by applications.</span><br><br><b>Valid values:</b><ul><li><code>ENABLED</code></li><li><code>DISABLED</code></li><li><code>MARKED_DOWN</code></li></ul> For implementation help, refer to <a href='https://developer.ebay.com/api-docs/commerce/notification/types/api:DestinationStatusEnum'>eBay API documentation</a>  # noqa: E501

        :return: The status of this Destination.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Destination.

        The status for this destination.<br><br><span class=\"tablenote\"><b>Note:</b> The <b>MARKED_DOWN</b> value is set by eBay systems and cannot be used in a create or update call by applications.</span><br><br><b>Valid values:</b><ul><li><code>ENABLED</code></li><li><code>DISABLED</code></li><li><code>MARKED_DOWN</code></li></ul> For implementation help, refer to <a href='https://developer.ebay.com/api-docs/commerce/notification/types/api:DestinationStatusEnum'>eBay API documentation</a>  # noqa: E501

        :param status: The status of this Destination.  # noqa: E501
        :type: str
        """

        self._status = status

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
        if issubclass(Destination, dict):
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
        if not isinstance(other, Destination):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
