# coding: utf-8

"""
    eBay Finances API

    This API is used to retrieve seller payouts and monetary transaction details related to those payouts.  # noqa: E501

    OpenAPI spec version: v1.17.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Transfer(object):
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
        'funding_source': 'FundingSource',
        'transaction_date': 'str',
        'transfer_amount': 'Amount',
        'transfer_detail': 'TransferDetail',
        'transfer_id': 'str'
    }

    attribute_map = {
        'funding_source': 'fundingSource',
        'transaction_date': 'transactionDate',
        'transfer_amount': 'transferAmount',
        'transfer_detail': 'transferDetail',
        'transfer_id': 'transferId'
    }

    def __init__(self, funding_source=None, transaction_date=None, transfer_amount=None, transfer_detail=None, transfer_id=None):  # noqa: E501
        """Transfer - a model defined in Swagger"""  # noqa: E501
        self._funding_source = None
        self._transaction_date = None
        self._transfer_amount = None
        self._transfer_detail = None
        self._transfer_id = None
        self.discriminator = None
        if funding_source is not None:
            self.funding_source = funding_source
        if transaction_date is not None:
            self.transaction_date = transaction_date
        if transfer_amount is not None:
            self.transfer_amount = transfer_amount
        if transfer_detail is not None:
            self.transfer_detail = transfer_detail
        if transfer_id is not None:
            self.transfer_id = transfer_id

    @property
    def funding_source(self):
        """Gets the funding_source of this Transfer.  # noqa: E501


        :return: The funding_source of this Transfer.  # noqa: E501
        :rtype: FundingSource
        """
        return self._funding_source

    @funding_source.setter
    def funding_source(self, funding_source):
        """Sets the funding_source of this Transfer.


        :param funding_source: The funding_source of this Transfer.  # noqa: E501
        :type: FundingSource
        """

        self._funding_source = funding_source

    @property
    def transaction_date(self):
        """Gets the transaction_date of this Transfer.  # noqa: E501

        This timestamp indicates the date/time of the transfer. The following (UTC) format is used: <code>YYYY-MM-DDTHH:MM:SS.SSSZ</code>. For example, <code>2020-08-04T19:09:02.768Z</code>  # noqa: E501

        :return: The transaction_date of this Transfer.  # noqa: E501
        :rtype: str
        """
        return self._transaction_date

    @transaction_date.setter
    def transaction_date(self, transaction_date):
        """Sets the transaction_date of this Transfer.

        This timestamp indicates the date/time of the transfer. The following (UTC) format is used: <code>YYYY-MM-DDTHH:MM:SS.SSSZ</code>. For example, <code>2020-08-04T19:09:02.768Z</code>  # noqa: E501

        :param transaction_date: The transaction_date of this Transfer.  # noqa: E501
        :type: str
        """

        self._transaction_date = transaction_date

    @property
    def transfer_amount(self):
        """Gets the transfer_amount of this Transfer.  # noqa: E501


        :return: The transfer_amount of this Transfer.  # noqa: E501
        :rtype: Amount
        """
        return self._transfer_amount

    @transfer_amount.setter
    def transfer_amount(self, transfer_amount):
        """Sets the transfer_amount of this Transfer.


        :param transfer_amount: The transfer_amount of this Transfer.  # noqa: E501
        :type: Amount
        """

        self._transfer_amount = transfer_amount

    @property
    def transfer_detail(self):
        """Gets the transfer_detail of this Transfer.  # noqa: E501


        :return: The transfer_detail of this Transfer.  # noqa: E501
        :rtype: TransferDetail
        """
        return self._transfer_detail

    @transfer_detail.setter
    def transfer_detail(self, transfer_detail):
        """Sets the transfer_detail of this Transfer.


        :param transfer_detail: The transfer_detail of this Transfer.  # noqa: E501
        :type: TransferDetail
        """

        self._transfer_detail = transfer_detail

    @property
    def transfer_id(self):
        """Gets the transfer_id of this Transfer.  # noqa: E501

        The unique identifier of the <code>TRANSFER</code> transaction type. This is the same value that was passed into the end of the call URI.  # noqa: E501

        :return: The transfer_id of this Transfer.  # noqa: E501
        :rtype: str
        """
        return self._transfer_id

    @transfer_id.setter
    def transfer_id(self, transfer_id):
        """Sets the transfer_id of this Transfer.

        The unique identifier of the <code>TRANSFER</code> transaction type. This is the same value that was passed into the end of the call URI.  # noqa: E501

        :param transfer_id: The transfer_id of this Transfer.  # noqa: E501
        :type: str
        """

        self._transfer_id = transfer_id

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
        if issubclass(Transfer, dict):
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
        if not isinstance(other, Transfer):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
