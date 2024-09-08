# coding: utf-8

"""
    Inventory API

    The Inventory API is used to create and manage inventory, and then to publish and manage this inventory on an eBay marketplace. There are also methods in this API that will convert eligible, active eBay listings into the Inventory API model.  # noqa: E501

    OpenAPI spec version: 1.17.6
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class MigrateListing(object):
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
        'listing_id': 'str'
    }

    attribute_map = {
        'listing_id': 'listingId'
    }

    def __init__(self, listing_id=None):  # noqa: E501
        """MigrateListing - a model defined in Swagger"""  # noqa: E501
        self._listing_id = None
        self.discriminator = None
        if listing_id is not None:
            self.listing_id = listing_id

    @property
    def listing_id(self):
        """Gets the listing_id of this MigrateListing.  # noqa: E501

        The unique identifier of the eBay listing to migrate to the new Inventory model. In the Trading API, this field is known as the <strong>ItemID</strong>.<br><br>Up to five unique eBay listings may be specified here in separate <strong>listingId</strong> fields. The seller should make sure that each of these listings meet the requirements that are stated at the top of this Call Reference page.  # noqa: E501

        :return: The listing_id of this MigrateListing.  # noqa: E501
        :rtype: str
        """
        return self._listing_id

    @listing_id.setter
    def listing_id(self, listing_id):
        """Sets the listing_id of this MigrateListing.

        The unique identifier of the eBay listing to migrate to the new Inventory model. In the Trading API, this field is known as the <strong>ItemID</strong>.<br><br>Up to five unique eBay listings may be specified here in separate <strong>listingId</strong> fields. The seller should make sure that each of these listings meet the requirements that are stated at the top of this Call Reference page.  # noqa: E501

        :param listing_id: The listing_id of this MigrateListing.  # noqa: E501
        :type: str
        """

        self._listing_id = listing_id

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
        if issubclass(MigrateListing, dict):
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
        if not isinstance(other, MigrateListing):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
