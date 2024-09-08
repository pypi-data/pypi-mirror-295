# coding: utf-8

"""
    Analytics API

    The <b>Analytics API</b> retrieves call-limit data and the quotas that are set for the RESTful APIs and the legacy Trading API.  <br><br>Responses from calls made to <b>getRateLimits</b> and <b>getUerRateLimits</b> include a list of the applicable resources and the \"call limit\", or quota, that is set for each resource. In addition to quota information, the response also includes the number of remaining calls available before the limit is reached, the time remaining before the quota resets, and the length of the \"time window\" to which the quota applies.  <br><br>The <b>getRateLimits</b> and <b>getUserRateLimits</b> methods retrieve call-limit information for either an application or user, respectively, and each method must be called with an appropriate OAuth token. That is, <b>getRateLimites</b> requires an access token generated with a client credentials grant and <b>getUserRateLimites</b> requires an access token generated with an authorization code grant. For more information, see <a href=\"/api-docs/static/oauth-tokens.html\">OAuth tokens</a>.  <br><br>Users can analyze the response data to see whether or not a limit might be reached, and from that determine if any action needs to be taken (such as programmatically throttling their request rate). For more on call limits, see <a href=\"https://developer.ebay.com/support/app-check \" target=\"_blank\">Compatible Application Check</a>.  # noqa: E501

    OpenAPI spec version: v1_beta.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Rate(object):
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
        'limit': 'int',
        'remaining': 'int',
        'reset': 'str',
        'time_window': 'int'
    }

    attribute_map = {
        'limit': 'limit',
        'remaining': 'remaining',
        'reset': 'reset',
        'time_window': 'timeWindow'
    }

    def __init__(self, limit=None, remaining=None, reset=None, time_window=None):  # noqa: E501
        """Rate - a model defined in Swagger"""  # noqa: E501
        self._limit = None
        self._remaining = None
        self._reset = None
        self._time_window = None
        self.discriminator = None
        if limit is not None:
            self.limit = limit
        if remaining is not None:
            self.remaining = remaining
        if reset is not None:
            self.reset = reset
        if time_window is not None:
            self.time_window = time_window

    @property
    def limit(self):
        """Gets the limit of this Rate.  # noqa: E501

        The maximum number of requests that can be made to this resource during a set time period. The length of time to which the limit is applied is defined by the associated <b>timeWindow</b> value.  <br><br>This value is often referred to as the \"call quota\" for the resource.  # noqa: E501

        :return: The limit of this Rate.  # noqa: E501
        :rtype: int
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """Sets the limit of this Rate.

        The maximum number of requests that can be made to this resource during a set time period. The length of time to which the limit is applied is defined by the associated <b>timeWindow</b> value.  <br><br>This value is often referred to as the \"call quota\" for the resource.  # noqa: E501

        :param limit: The limit of this Rate.  # noqa: E501
        :type: int
        """

        self._limit = limit

    @property
    def remaining(self):
        """Gets the remaining of this Rate.  # noqa: E501

        The remaining number of requests that can be made to this resource before the associated time window resets.  # noqa: E501

        :return: The remaining of this Rate.  # noqa: E501
        :rtype: int
        """
        return self._remaining

    @remaining.setter
    def remaining(self, remaining):
        """Sets the remaining of this Rate.

        The remaining number of requests that can be made to this resource before the associated time window resets.  # noqa: E501

        :param remaining: The remaining of this Rate.  # noqa: E501
        :type: int
        """

        self._remaining = remaining

    @property
    def reset(self):
        """Gets the reset of this Rate.  # noqa: E501

        The data and time the time window and accumulated calls for this resource reset.  <br><br>When the <b>reset</b> time is reached, the <b>remaining</b> value is reset to the value of <b>limit</b>, and this <b>reset</b> value is reset to the current time plus the number of seconds defined by the <b>timeWindow</b> value. <br><br>The time stamp is formatted as an <a href=\"http://www.iso.org/iso/home/standards/iso8601.htm \" target=\"_blank\">ISO 8601</a> string, which is based on the 24-hour Universal Coordinated Time (UTC) clock. <br><br><b>Format:</b> <code>[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss].[sss]Z</code> <br><b>Example:</b> <code>2018-08-04T07:09:00.000Z</code>  # noqa: E501

        :return: The reset of this Rate.  # noqa: E501
        :rtype: str
        """
        return self._reset

    @reset.setter
    def reset(self, reset):
        """Sets the reset of this Rate.

        The data and time the time window and accumulated calls for this resource reset.  <br><br>When the <b>reset</b> time is reached, the <b>remaining</b> value is reset to the value of <b>limit</b>, and this <b>reset</b> value is reset to the current time plus the number of seconds defined by the <b>timeWindow</b> value. <br><br>The time stamp is formatted as an <a href=\"http://www.iso.org/iso/home/standards/iso8601.htm \" target=\"_blank\">ISO 8601</a> string, which is based on the 24-hour Universal Coordinated Time (UTC) clock. <br><br><b>Format:</b> <code>[YYYY]-[MM]-[DD]T[hh]:[mm]:[ss].[sss]Z</code> <br><b>Example:</b> <code>2018-08-04T07:09:00.000Z</code>  # noqa: E501

        :param reset: The reset of this Rate.  # noqa: E501
        :type: str
        """

        self._reset = reset

    @property
    def time_window(self):
        """Gets the time_window of this Rate.  # noqa: E501

        A period of time, expressed in seconds. The call quota for a resource is applied to the period of time defined by the value of this field.  # noqa: E501

        :return: The time_window of this Rate.  # noqa: E501
        :rtype: int
        """
        return self._time_window

    @time_window.setter
    def time_window(self, time_window):
        """Sets the time_window of this Rate.

        A period of time, expressed in seconds. The call quota for a resource is applied to the period of time defined by the value of this field.  # noqa: E501

        :param time_window: The time_window of this Rate.  # noqa: E501
        :type: int
        """

        self._time_window = time_window

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
        if issubclass(Rate, dict):
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
        if not isinstance(other, Rate):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
