# coding: utf-8

"""
    Feed API

    <p>The <strong>Feed API</strong> lets sellers upload input files, download reports and files including their status, filter reports using URI parameters, and retrieve customer service metrics task details.</p>  # noqa: E501

    OpenAPI spec version: v1.3.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CreateUserScheduleRequest(object):
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
        'feed_type': 'str',
        'preferred_trigger_day_of_month': 'int',
        'preferred_trigger_day_of_week': 'str',
        'preferred_trigger_hour': 'str',
        'schedule_end_date': 'str',
        'schedule_name': 'str',
        'schedule_start_date': 'str',
        'schedule_template_id': 'str',
        'schema_version': 'str'
    }

    attribute_map = {
        'feed_type': 'feedType',
        'preferred_trigger_day_of_month': 'preferredTriggerDayOfMonth',
        'preferred_trigger_day_of_week': 'preferredTriggerDayOfWeek',
        'preferred_trigger_hour': 'preferredTriggerHour',
        'schedule_end_date': 'scheduleEndDate',
        'schedule_name': 'scheduleName',
        'schedule_start_date': 'scheduleStartDate',
        'schedule_template_id': 'scheduleTemplateId',
        'schema_version': 'schemaVersion'
    }

    def __init__(self, feed_type=None, preferred_trigger_day_of_month=None, preferred_trigger_day_of_week=None, preferred_trigger_hour=None, schedule_end_date=None, schedule_name=None, schedule_start_date=None, schedule_template_id=None, schema_version=None):  # noqa: E501
        """CreateUserScheduleRequest - a model defined in Swagger"""  # noqa: E501
        self._feed_type = None
        self._preferred_trigger_day_of_month = None
        self._preferred_trigger_day_of_week = None
        self._preferred_trigger_hour = None
        self._schedule_end_date = None
        self._schedule_name = None
        self._schedule_start_date = None
        self._schedule_template_id = None
        self._schema_version = None
        self.discriminator = None
        if feed_type is not None:
            self.feed_type = feed_type
        if preferred_trigger_day_of_month is not None:
            self.preferred_trigger_day_of_month = preferred_trigger_day_of_month
        if preferred_trigger_day_of_week is not None:
            self.preferred_trigger_day_of_week = preferred_trigger_day_of_week
        if preferred_trigger_hour is not None:
            self.preferred_trigger_hour = preferred_trigger_hour
        if schedule_end_date is not None:
            self.schedule_end_date = schedule_end_date
        if schedule_name is not None:
            self.schedule_name = schedule_name
        if schedule_start_date is not None:
            self.schedule_start_date = schedule_start_date
        if schedule_template_id is not None:
            self.schedule_template_id = schedule_template_id
        if schema_version is not None:
            self.schema_version = schema_version

    @property
    def feed_type(self):
        """Gets the feed_type of this CreateUserScheduleRequest.  # noqa: E501

        The name of the feed type for the created schedule.<br><br> Use the <a href=\"/api-docs/sell/feed/resources/schedule/methods/getScheduleTemplates\">getScheduleTemplates</a> method to retrieve the feed type of a schedule template.<br><br><span class=\"tablenote\"><b>Note:</b> Schedules are currently only available for <code>LMS_ORDER_REPORT</code>.</span>  # noqa: E501

        :return: The feed_type of this CreateUserScheduleRequest.  # noqa: E501
        :rtype: str
        """
        return self._feed_type

    @feed_type.setter
    def feed_type(self, feed_type):
        """Sets the feed_type of this CreateUserScheduleRequest.

        The name of the feed type for the created schedule.<br><br> Use the <a href=\"/api-docs/sell/feed/resources/schedule/methods/getScheduleTemplates\">getScheduleTemplates</a> method to retrieve the feed type of a schedule template.<br><br><span class=\"tablenote\"><b>Note:</b> Schedules are currently only available for <code>LMS_ORDER_REPORT</code>.</span>  # noqa: E501

        :param feed_type: The feed_type of this CreateUserScheduleRequest.  # noqa: E501
        :type: str
        """

        self._feed_type = feed_type

    @property
    def preferred_trigger_day_of_month(self):
        """Gets the preferred_trigger_day_of_month of this CreateUserScheduleRequest.  # noqa: E501

        The preferred day of the month to trigger the schedule. This field can be used with <strong>preferredTriggerHour</strong> for monthly schedules. The last day of the month is used for numbers larger than the actual number of days in the month. <br /><br />This field is available as specified by the template (<strong>scheduleTemplateId</strong>). The template can specify this field as optional or required, and optionally provides a default value.<br /><br /><b>Minimum: </b>1<br /><br /><b>Maximum: </b>31  # noqa: E501

        :return: The preferred_trigger_day_of_month of this CreateUserScheduleRequest.  # noqa: E501
        :rtype: int
        """
        return self._preferred_trigger_day_of_month

    @preferred_trigger_day_of_month.setter
    def preferred_trigger_day_of_month(self, preferred_trigger_day_of_month):
        """Sets the preferred_trigger_day_of_month of this CreateUserScheduleRequest.

        The preferred day of the month to trigger the schedule. This field can be used with <strong>preferredTriggerHour</strong> for monthly schedules. The last day of the month is used for numbers larger than the actual number of days in the month. <br /><br />This field is available as specified by the template (<strong>scheduleTemplateId</strong>). The template can specify this field as optional or required, and optionally provides a default value.<br /><br /><b>Minimum: </b>1<br /><br /><b>Maximum: </b>31  # noqa: E501

        :param preferred_trigger_day_of_month: The preferred_trigger_day_of_month of this CreateUserScheduleRequest.  # noqa: E501
        :type: int
        """

        self._preferred_trigger_day_of_month = preferred_trigger_day_of_month

    @property
    def preferred_trigger_day_of_week(self):
        """Gets the preferred_trigger_day_of_week of this CreateUserScheduleRequest.  # noqa: E501

        The preferred day of the week to trigger the schedule. This field can be used with <strong>preferredTriggerHour</strong> for weekly schedules. <br /><br />This field is available as specified by the template (<strong>scheduleTemplateId</strong>). The template can specify this field as optional or required, and optionally provides a default value. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/feed/types/api:DayOfWeekEnum'>eBay API documentation</a>  # noqa: E501

        :return: The preferred_trigger_day_of_week of this CreateUserScheduleRequest.  # noqa: E501
        :rtype: str
        """
        return self._preferred_trigger_day_of_week

    @preferred_trigger_day_of_week.setter
    def preferred_trigger_day_of_week(self, preferred_trigger_day_of_week):
        """Sets the preferred_trigger_day_of_week of this CreateUserScheduleRequest.

        The preferred day of the week to trigger the schedule. This field can be used with <strong>preferredTriggerHour</strong> for weekly schedules. <br /><br />This field is available as specified by the template (<strong>scheduleTemplateId</strong>). The template can specify this field as optional or required, and optionally provides a default value. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/feed/types/api:DayOfWeekEnum'>eBay API documentation</a>  # noqa: E501

        :param preferred_trigger_day_of_week: The preferred_trigger_day_of_week of this CreateUserScheduleRequest.  # noqa: E501
        :type: str
        """

        self._preferred_trigger_day_of_week = preferred_trigger_day_of_week

    @property
    def preferred_trigger_hour(self):
        """Gets the preferred_trigger_hour of this CreateUserScheduleRequest.  # noqa: E501

        The preferred two-digit hour of the day to trigger the schedule. <br /><br />This field is available as specified by the template (<strong>scheduleTemplateId</strong>). The template can specify this field as optional or required, and optionally provides a default value.<br /><br /><b>Format:</b> UTC <code>hhZ</code><br /><br />For example, the following represents 11:00 am UTC:<code> 11Z</code>  # noqa: E501

        :return: The preferred_trigger_hour of this CreateUserScheduleRequest.  # noqa: E501
        :rtype: str
        """
        return self._preferred_trigger_hour

    @preferred_trigger_hour.setter
    def preferred_trigger_hour(self, preferred_trigger_hour):
        """Sets the preferred_trigger_hour of this CreateUserScheduleRequest.

        The preferred two-digit hour of the day to trigger the schedule. <br /><br />This field is available as specified by the template (<strong>scheduleTemplateId</strong>). The template can specify this field as optional or required, and optionally provides a default value.<br /><br /><b>Format:</b> UTC <code>hhZ</code><br /><br />For example, the following represents 11:00 am UTC:<code> 11Z</code>  # noqa: E501

        :param preferred_trigger_hour: The preferred_trigger_hour of this CreateUserScheduleRequest.  # noqa: E501
        :type: str
        """

        self._preferred_trigger_hour = preferred_trigger_hour

    @property
    def schedule_end_date(self):
        """Gets the schedule_end_date of this CreateUserScheduleRequest.  # noqa: E501

        The timestamp on which the report generation (subscription) ends. After this date, the schedule status becomes <code>INACTIVE</code>. <br /><br />Use this field, if available, to end the schedule in the future. This value must be later than <strong>scheduleStartDate</strong> (if supplied). This field is available as specified by the template (<strong>scheduleTemplateId</strong>). The template can specify this field as optional or required, and optionally provides a default value.<br /><br /><b>Format:</b> UTC <code>yyyy-MM-dd<strong>T</strong>HH<strong>Z</strong></code><br /><br />For example, the following represents UTC October 10, 2021 at 10:00 AM:<br /><code>2021-10-10T10Z</code>  # noqa: E501

        :return: The schedule_end_date of this CreateUserScheduleRequest.  # noqa: E501
        :rtype: str
        """
        return self._schedule_end_date

    @schedule_end_date.setter
    def schedule_end_date(self, schedule_end_date):
        """Sets the schedule_end_date of this CreateUserScheduleRequest.

        The timestamp on which the report generation (subscription) ends. After this date, the schedule status becomes <code>INACTIVE</code>. <br /><br />Use this field, if available, to end the schedule in the future. This value must be later than <strong>scheduleStartDate</strong> (if supplied). This field is available as specified by the template (<strong>scheduleTemplateId</strong>). The template can specify this field as optional or required, and optionally provides a default value.<br /><br /><b>Format:</b> UTC <code>yyyy-MM-dd<strong>T</strong>HH<strong>Z</strong></code><br /><br />For example, the following represents UTC October 10, 2021 at 10:00 AM:<br /><code>2021-10-10T10Z</code>  # noqa: E501

        :param schedule_end_date: The schedule_end_date of this CreateUserScheduleRequest.  # noqa: E501
        :type: str
        """

        self._schedule_end_date = schedule_end_date

    @property
    def schedule_name(self):
        """Gets the schedule_name of this CreateUserScheduleRequest.  # noqa: E501

        The schedule name assigned by the user for the created schedule.  # noqa: E501

        :return: The schedule_name of this CreateUserScheduleRequest.  # noqa: E501
        :rtype: str
        """
        return self._schedule_name

    @schedule_name.setter
    def schedule_name(self, schedule_name):
        """Sets the schedule_name of this CreateUserScheduleRequest.

        The schedule name assigned by the user for the created schedule.  # noqa: E501

        :param schedule_name: The schedule_name of this CreateUserScheduleRequest.  # noqa: E501
        :type: str
        """

        self._schedule_name = schedule_name

    @property
    def schedule_start_date(self):
        """Gets the schedule_start_date of this CreateUserScheduleRequest.  # noqa: E501

        The timestamp to start generating the report. After this timestamp, the schedule status becomes active until either the <strong>scheduleEndDate</strong> occurs or the <strong>scheduleTemplateId</strong> becomes inactive. <br /><br />Use this field, if available, to start the schedule in the future but before the <strong>scheduleEndDate</strong> (if supplied). This field is available as specified by the template <strong>(scheduleTemplateId)</strong>. The template can specify this field as optional or required, and optionally provides a default value.<br /><br /><b>Format:</b> UTC <code>yyyy-MM-dd<strong>T</strong>HH<strong>Z</strong></code><br /><br />For example, the following represents a schedule start date of UTC October 01, 2020 at 12:00 PM:<br /><code> 2020-01-01T12Z</code>  # noqa: E501

        :return: The schedule_start_date of this CreateUserScheduleRequest.  # noqa: E501
        :rtype: str
        """
        return self._schedule_start_date

    @schedule_start_date.setter
    def schedule_start_date(self, schedule_start_date):
        """Sets the schedule_start_date of this CreateUserScheduleRequest.

        The timestamp to start generating the report. After this timestamp, the schedule status becomes active until either the <strong>scheduleEndDate</strong> occurs or the <strong>scheduleTemplateId</strong> becomes inactive. <br /><br />Use this field, if available, to start the schedule in the future but before the <strong>scheduleEndDate</strong> (if supplied). This field is available as specified by the template <strong>(scheduleTemplateId)</strong>. The template can specify this field as optional or required, and optionally provides a default value.<br /><br /><b>Format:</b> UTC <code>yyyy-MM-dd<strong>T</strong>HH<strong>Z</strong></code><br /><br />For example, the following represents a schedule start date of UTC October 01, 2020 at 12:00 PM:<br /><code> 2020-01-01T12Z</code>  # noqa: E501

        :param schedule_start_date: The schedule_start_date of this CreateUserScheduleRequest.  # noqa: E501
        :type: str
        """

        self._schedule_start_date = schedule_start_date

    @property
    def schedule_template_id(self):
        """Gets the schedule_template_id of this CreateUserScheduleRequest.  # noqa: E501

        The unique identifier of the template to be used for this schedule. <br><br>Use the <a href=\"/api-docs/sell/feed/resources/schedule/methods/getScheduleTemplates\">getScheduleTemplates</a> method to retrieve the schedule template ID. This method requires a schedule template ID that is <code>ACTIVE</code>.<br><br><span class=\"tablenote\"><b>Note:</b> Schedules are currently only available for <code>LMS_ORDER_REPORT</code>.</span>  # noqa: E501

        :return: The schedule_template_id of this CreateUserScheduleRequest.  # noqa: E501
        :rtype: str
        """
        return self._schedule_template_id

    @schedule_template_id.setter
    def schedule_template_id(self, schedule_template_id):
        """Sets the schedule_template_id of this CreateUserScheduleRequest.

        The unique identifier of the template to be used for this schedule. <br><br>Use the <a href=\"/api-docs/sell/feed/resources/schedule/methods/getScheduleTemplates\">getScheduleTemplates</a> method to retrieve the schedule template ID. This method requires a schedule template ID that is <code>ACTIVE</code>.<br><br><span class=\"tablenote\"><b>Note:</b> Schedules are currently only available for <code>LMS_ORDER_REPORT</code>.</span>  # noqa: E501

        :param schedule_template_id: The schedule_template_id of this CreateUserScheduleRequest.  # noqa: E501
        :type: str
        """

        self._schedule_template_id = schedule_template_id

    @property
    def schema_version(self):
        """Gets the schema_version of this CreateUserScheduleRequest.  # noqa: E501

        The schema version of a schedule.  # noqa: E501

        :return: The schema_version of this CreateUserScheduleRequest.  # noqa: E501
        :rtype: str
        """
        return self._schema_version

    @schema_version.setter
    def schema_version(self, schema_version):
        """Sets the schema_version of this CreateUserScheduleRequest.

        The schema version of a schedule.  # noqa: E501

        :param schema_version: The schema_version of this CreateUserScheduleRequest.  # noqa: E501
        :type: str
        """

        self._schema_version = schema_version

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
        if issubclass(CreateUserScheduleRequest, dict):
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
        if not isinstance(other, CreateUserScheduleRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
