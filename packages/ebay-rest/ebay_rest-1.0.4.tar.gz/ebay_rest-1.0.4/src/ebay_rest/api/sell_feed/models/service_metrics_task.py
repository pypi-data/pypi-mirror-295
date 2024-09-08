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

class ServiceMetricsTask(object):
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
        'completion_date': 'str',
        'creation_date': 'str',
        'detail_href': 'str',
        'feed_type': 'str',
        'filter_criteria': 'CustomerServiceMetricsFilterCriteria',
        'schema_version': 'str',
        'status': 'str',
        'task_id': 'str'
    }

    attribute_map = {
        'completion_date': 'completionDate',
        'creation_date': 'creationDate',
        'detail_href': 'detailHref',
        'feed_type': 'feedType',
        'filter_criteria': 'filterCriteria',
        'schema_version': 'schemaVersion',
        'status': 'status',
        'task_id': 'taskId'
    }

    def __init__(self, completion_date=None, creation_date=None, detail_href=None, feed_type=None, filter_criteria=None, schema_version=None, status=None, task_id=None):  # noqa: E501
        """ServiceMetricsTask - a model defined in Swagger"""  # noqa: E501
        self._completion_date = None
        self._creation_date = None
        self._detail_href = None
        self._feed_type = None
        self._filter_criteria = None
        self._schema_version = None
        self._status = None
        self._task_id = None
        self.discriminator = None
        if completion_date is not None:
            self.completion_date = completion_date
        if creation_date is not None:
            self.creation_date = creation_date
        if detail_href is not None:
            self.detail_href = detail_href
        if feed_type is not None:
            self.feed_type = feed_type
        if filter_criteria is not None:
            self.filter_criteria = filter_criteria
        if schema_version is not None:
            self.schema_version = schema_version
        if status is not None:
            self.status = status
        if task_id is not None:
            self.task_id = task_id

    @property
    def completion_date(self):
        """Gets the completion_date of this ServiceMetricsTask.  # noqa: E501

        The timestamp when the customer service metrics task went into the <code>COMPLETED</code> or <code>COMPLETED_WITH_ERROR</code> state. This field is only returned if the status is one of the two completed values. This state means that eBay has compiled the report for the seller based on the seller’s filter criteria, and the seller can run a <strong>getResultFile</strong> call to download the report.  # noqa: E501

        :return: The completion_date of this ServiceMetricsTask.  # noqa: E501
        :rtype: str
        """
        return self._completion_date

    @completion_date.setter
    def completion_date(self, completion_date):
        """Sets the completion_date of this ServiceMetricsTask.

        The timestamp when the customer service metrics task went into the <code>COMPLETED</code> or <code>COMPLETED_WITH_ERROR</code> state. This field is only returned if the status is one of the two completed values. This state means that eBay has compiled the report for the seller based on the seller’s filter criteria, and the seller can run a <strong>getResultFile</strong> call to download the report.  # noqa: E501

        :param completion_date: The completion_date of this ServiceMetricsTask.  # noqa: E501
        :type: str
        """

        self._completion_date = completion_date

    @property
    def creation_date(self):
        """Gets the creation_date of this ServiceMetricsTask.  # noqa: E501

        The date the customer service metrics task was created.  # noqa: E501

        :return: The creation_date of this ServiceMetricsTask.  # noqa: E501
        :rtype: str
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        """Sets the creation_date of this ServiceMetricsTask.

        The date the customer service metrics task was created.  # noqa: E501

        :param creation_date: The creation_date of this ServiceMetricsTask.  # noqa: E501
        :type: str
        """

        self._creation_date = creation_date

    @property
    def detail_href(self):
        """Gets the detail_href of this ServiceMetricsTask.  # noqa: E501

        The relative <strong>getCustomerServiceMetricTask</strong> call URI path to retrieve the corresponding task.  # noqa: E501

        :return: The detail_href of this ServiceMetricsTask.  # noqa: E501
        :rtype: str
        """
        return self._detail_href

    @detail_href.setter
    def detail_href(self, detail_href):
        """Sets the detail_href of this ServiceMetricsTask.

        The relative <strong>getCustomerServiceMetricTask</strong> call URI path to retrieve the corresponding task.  # noqa: E501

        :param detail_href: The detail_href of this ServiceMetricsTask.  # noqa: E501
        :type: str
        """

        self._detail_href = detail_href

    @property
    def feed_type(self):
        """Gets the feed_type of this ServiceMetricsTask.  # noqa: E501

        The feed type associated with the task.  # noqa: E501

        :return: The feed_type of this ServiceMetricsTask.  # noqa: E501
        :rtype: str
        """
        return self._feed_type

    @feed_type.setter
    def feed_type(self, feed_type):
        """Sets the feed_type of this ServiceMetricsTask.

        The feed type associated with the task.  # noqa: E501

        :param feed_type: The feed_type of this ServiceMetricsTask.  # noqa: E501
        :type: str
        """

        self._feed_type = feed_type

    @property
    def filter_criteria(self):
        """Gets the filter_criteria of this ServiceMetricsTask.  # noqa: E501


        :return: The filter_criteria of this ServiceMetricsTask.  # noqa: E501
        :rtype: CustomerServiceMetricsFilterCriteria
        """
        return self._filter_criteria

    @filter_criteria.setter
    def filter_criteria(self, filter_criteria):
        """Sets the filter_criteria of this ServiceMetricsTask.


        :param filter_criteria: The filter_criteria of this ServiceMetricsTask.  # noqa: E501
        :type: CustomerServiceMetricsFilterCriteria
        """

        self._filter_criteria = filter_criteria

    @property
    def schema_version(self):
        """Gets the schema_version of this ServiceMetricsTask.  # noqa: E501

        The schema version number of the file format. If omitted, the default value is used. <p><b>Default value: </b><code>1.0</code><p>  # noqa: E501

        :return: The schema_version of this ServiceMetricsTask.  # noqa: E501
        :rtype: str
        """
        return self._schema_version

    @schema_version.setter
    def schema_version(self, schema_version):
        """Sets the schema_version of this ServiceMetricsTask.

        The schema version number of the file format. If omitted, the default value is used. <p><b>Default value: </b><code>1.0</code><p>  # noqa: E501

        :param schema_version: The schema_version of this ServiceMetricsTask.  # noqa: E501
        :type: str
        """

        self._schema_version = schema_version

    @property
    def status(self):
        """Gets the status of this ServiceMetricsTask.  # noqa: E501

        An enumeration value that indicates the state of the task. See <strong>FeedStatusEnum</strong> for values. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/feed/types/api:FeedStatusEnum'>eBay API documentation</a>  # noqa: E501

        :return: The status of this ServiceMetricsTask.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ServiceMetricsTask.

        An enumeration value that indicates the state of the task. See <strong>FeedStatusEnum</strong> for values. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/feed/types/api:FeedStatusEnum'>eBay API documentation</a>  # noqa: E501

        :param status: The status of this ServiceMetricsTask.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def task_id(self):
        """Gets the task_id of this ServiceMetricsTask.  # noqa: E501

        The unique eBay-assigned ID of the task.  # noqa: E501

        :return: The task_id of this ServiceMetricsTask.  # noqa: E501
        :rtype: str
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this ServiceMetricsTask.

        The unique eBay-assigned ID of the task.  # noqa: E501

        :param task_id: The task_id of this ServiceMetricsTask.  # noqa: E501
        :type: str
        """

        self._task_id = task_id

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
        if issubclass(ServiceMetricsTask, dict):
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
        if not isinstance(other, ServiceMetricsTask):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
