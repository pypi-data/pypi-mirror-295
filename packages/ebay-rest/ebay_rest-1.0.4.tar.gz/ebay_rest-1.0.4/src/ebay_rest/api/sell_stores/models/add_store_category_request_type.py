# coding: utf-8

"""
    Store API

    <p>This API provides stores-related resources for third-party developers. These resources let you retrieve basic store information such as store name, description, store url, return store category hierarchy, add,rename,move,delete a single user's eBay store category, and retrieve the processing status of these tasks.</p> <p>The stores resource methods require an access token created with the <a href=\"/api-docs/static/oauth-authorization-code-grant.html\">authorization code grant</a> flow, using one or more scopes from the following list (please check your Application Keys page for a list of OAuth scopes available to your application)</p>  # noqa: E501

    OpenAPI spec version: 1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class AddStoreCategoryRequestType(object):
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
        'category_name': 'str',
        'destination_parent_category_id': 'str',
        'listing_destination_category_id': 'str'
    }

    attribute_map = {
        'category_name': 'categoryName',
        'destination_parent_category_id': 'destinationParentCategoryId',
        'listing_destination_category_id': 'listingDestinationCategoryId'
    }

    def __init__(self, category_name=None, destination_parent_category_id=None, listing_destination_category_id=None):  # noqa: E501
        """AddStoreCategoryRequestType - a model defined in Swagger"""  # noqa: E501
        self._category_name = None
        self._destination_parent_category_id = None
        self._listing_destination_category_id = None
        self.discriminator = None
        if category_name is not None:
            self.category_name = category_name
        if destination_parent_category_id is not None:
            self.destination_parent_category_id = destination_parent_category_id
        if listing_destination_category_id is not None:
            self.listing_destination_category_id = listing_destination_category_id

    @property
    def category_name(self):
        """Gets the category_name of this AddStoreCategoryRequestType.  # noqa: E501

        The seller-specified name of the custom category.<br><br> <b>Max Length: </b>35  # noqa: E501

        :return: The category_name of this AddStoreCategoryRequestType.  # noqa: E501
        :rtype: str
        """
        return self._category_name

    @category_name.setter
    def category_name(self, category_name):
        """Sets the category_name of this AddStoreCategoryRequestType.

        The seller-specified name of the custom category.<br><br> <b>Max Length: </b>35  # noqa: E501

        :param category_name: The category_name of this AddStoreCategoryRequestType.  # noqa: E501
        :type: str
        """

        self._category_name = category_name

    @property
    def destination_parent_category_id(self):
        """Gets the destination_parent_category_id of this AddStoreCategoryRequestType.  # noqa: E501

        This field is used to specify the parent category to which the new category belongs. To specify the new category as a top-level category, set the value of this field to -999, or just omit this field, as the default value is -999.<br>The <a href=\"/api-docs/sell/stores/resources/store/methods/getStoreCategories\"><b>getStoreCategories</b></a> method can be used to retrieve store category IDs.<br><br><b>Default: ROOT</b> category ID<b>(-999)</b> if it's null.  # noqa: E501

        :return: The destination_parent_category_id of this AddStoreCategoryRequestType.  # noqa: E501
        :rtype: str
        """
        return self._destination_parent_category_id

    @destination_parent_category_id.setter
    def destination_parent_category_id(self, destination_parent_category_id):
        """Sets the destination_parent_category_id of this AddStoreCategoryRequestType.

        This field is used to specify the parent category to which the new category belongs. To specify the new category as a top-level category, set the value of this field to -999, or just omit this field, as the default value is -999.<br>The <a href=\"/api-docs/sell/stores/resources/store/methods/getStoreCategories\"><b>getStoreCategories</b></a> method can be used to retrieve store category IDs.<br><br><b>Default: ROOT</b> category ID<b>(-999)</b> if it's null.  # noqa: E501

        :param destination_parent_category_id: The destination_parent_category_id of this AddStoreCategoryRequestType.  # noqa: E501
        :type: str
        """

        self._destination_parent_category_id = destination_parent_category_id

    @property
    def listing_destination_category_id(self):
        """Gets the listing_destination_category_id of this AddStoreCategoryRequestType.  # noqa: E501

        If the store category specified as the <b>destinationParentCategoryId</b> is a leaf category with active listings, those listings are moved to the store category identified through this <b>listingDestinationCategoryId</b>. If this field is omitted, the new store category being added under the parent category inherits those listings.<br>The <a href=\"/api-docs/sell/stores/resources/store/methods/getStoreCategories\"><b>getStoreCategories</b></a> method can be used to retrieve store category IDs.<br><br><b>Default:</b> Newly added category ID if it's null.  # noqa: E501

        :return: The listing_destination_category_id of this AddStoreCategoryRequestType.  # noqa: E501
        :rtype: str
        """
        return self._listing_destination_category_id

    @listing_destination_category_id.setter
    def listing_destination_category_id(self, listing_destination_category_id):
        """Sets the listing_destination_category_id of this AddStoreCategoryRequestType.

        If the store category specified as the <b>destinationParentCategoryId</b> is a leaf category with active listings, those listings are moved to the store category identified through this <b>listingDestinationCategoryId</b>. If this field is omitted, the new store category being added under the parent category inherits those listings.<br>The <a href=\"/api-docs/sell/stores/resources/store/methods/getStoreCategories\"><b>getStoreCategories</b></a> method can be used to retrieve store category IDs.<br><br><b>Default:</b> Newly added category ID if it's null.  # noqa: E501

        :param listing_destination_category_id: The listing_destination_category_id of this AddStoreCategoryRequestType.  # noqa: E501
        :type: str
        """

        self._listing_destination_category_id = listing_destination_category_id

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
        if issubclass(AddStoreCategoryRequestType, dict):
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
        if not isinstance(other, AddStoreCategoryRequestType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
