# coding: utf-8

"""
    Fulfillment API

    Use the Fulfillment API to complete the process of packaging, addressing, handling, and shipping each order on behalf of the seller, in accordance with the payment method and timing specified at checkout.  # noqa: E501

    OpenAPI spec version: v1.20.4
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CancelStatus(object):
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
        'cancelled_date': 'str',
        'cancel_requests': 'list[CancelRequest]',
        'cancel_state': 'str'
    }

    attribute_map = {
        'cancelled_date': 'cancelledDate',
        'cancel_requests': 'cancelRequests',
        'cancel_state': 'cancelState'
    }

    def __init__(self, cancelled_date=None, cancel_requests=None, cancel_state=None):  # noqa: E501
        """CancelStatus - a model defined in Swagger"""  # noqa: E501
        self._cancelled_date = None
        self._cancel_requests = None
        self._cancel_state = None
        self.discriminator = None
        if cancelled_date is not None:
            self.cancelled_date = cancelled_date
        if cancel_requests is not None:
            self.cancel_requests = cancel_requests
        if cancel_state is not None:
            self.cancel_state = cancel_state

    @property
    def cancelled_date(self):
        """Gets the cancelled_date of this CancelStatus.  # noqa: E501

        The date and time the order was cancelled, if applicable. This timestamp is in ISO 8601 format, which uses the 24-hour Universal Coordinated Time (UTC) clock. <br><br><b>Format:</b> <code>[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss].[sss]Z</code> <br><b>Example:</b> <code>2015-08-04T19:09:02.768Z</code>  # noqa: E501

        :return: The cancelled_date of this CancelStatus.  # noqa: E501
        :rtype: str
        """
        return self._cancelled_date

    @cancelled_date.setter
    def cancelled_date(self, cancelled_date):
        """Sets the cancelled_date of this CancelStatus.

        The date and time the order was cancelled, if applicable. This timestamp is in ISO 8601 format, which uses the 24-hour Universal Coordinated Time (UTC) clock. <br><br><b>Format:</b> <code>[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss].[sss]Z</code> <br><b>Example:</b> <code>2015-08-04T19:09:02.768Z</code>  # noqa: E501

        :param cancelled_date: The cancelled_date of this CancelStatus.  # noqa: E501
        :type: str
        """

        self._cancelled_date = cancelled_date

    @property
    def cancel_requests(self):
        """Gets the cancel_requests of this CancelStatus.  # noqa: E501

        This array contains details of one or more buyer requests to cancel the order. <br><br><b>For the getOrders call:</b>  This array is returned but is always empty.<br><b>For the getOrder call:</b> This array is returned fully populated with information about any cancellation requests.  # noqa: E501

        :return: The cancel_requests of this CancelStatus.  # noqa: E501
        :rtype: list[CancelRequest]
        """
        return self._cancel_requests

    @cancel_requests.setter
    def cancel_requests(self, cancel_requests):
        """Sets the cancel_requests of this CancelStatus.

        This array contains details of one or more buyer requests to cancel the order. <br><br><b>For the getOrders call:</b>  This array is returned but is always empty.<br><b>For the getOrder call:</b> This array is returned fully populated with information about any cancellation requests.  # noqa: E501

        :param cancel_requests: The cancel_requests of this CancelStatus.  # noqa: E501
        :type: list[CancelRequest]
        """

        self._cancel_requests = cancel_requests

    @property
    def cancel_state(self):
        """Gets the cancel_state of this CancelStatus.  # noqa: E501

        The state of the order with regard to cancellation. This field is always returned, and if there are no cancellation requests, a value of <code>NONE_REQUESTED</code> is returned.  For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/fulfillment/types/sel:CancelStateEnum'>eBay API documentation</a>  # noqa: E501

        :return: The cancel_state of this CancelStatus.  # noqa: E501
        :rtype: str
        """
        return self._cancel_state

    @cancel_state.setter
    def cancel_state(self, cancel_state):
        """Sets the cancel_state of this CancelStatus.

        The state of the order with regard to cancellation. This field is always returned, and if there are no cancellation requests, a value of <code>NONE_REQUESTED</code> is returned.  For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/fulfillment/types/sel:CancelStateEnum'>eBay API documentation</a>  # noqa: E501

        :param cancel_state: The cancel_state of this CancelStatus.  # noqa: E501
        :type: str
        """

        self._cancel_state = cancel_state

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
        if issubclass(CancelStatus, dict):
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
        if not isinstance(other, CancelStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
