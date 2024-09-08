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

class PublishByInventoryItemGroupRequest(object):
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
        'inventory_item_group_key': 'str',
        'marketplace_id': 'str'
    }

    attribute_map = {
        'inventory_item_group_key': 'inventoryItemGroupKey',
        'marketplace_id': 'marketplaceId'
    }

    def __init__(self, inventory_item_group_key=None, marketplace_id=None):  # noqa: E501
        """PublishByInventoryItemGroupRequest - a model defined in Swagger"""  # noqa: E501
        self._inventory_item_group_key = None
        self._marketplace_id = None
        self.discriminator = None
        if inventory_item_group_key is not None:
            self.inventory_item_group_key = inventory_item_group_key
        if marketplace_id is not None:
            self.marketplace_id = marketplace_id

    @property
    def inventory_item_group_key(self):
        """Gets the inventory_item_group_key of this PublishByInventoryItemGroupRequest.  # noqa: E501

        This is the unique identifier of the inventory item group. All unpublished offers associated with this inventory item group will be published as a multiple-variation listing if the <strong>publishByInventoryItemGroup</strong> call is successful. The <strong>inventoryItemGroupKey</strong> identifier is automatically generated by eBay once an inventory item group is created.<br><br>To retrieve an <strong>inventoryItemGroupKey</strong> value, you can use the <a href=\"/api-docs/sell/inventory/resources/inventory_item/methods/getInventoryItem \" target=\"_blank\">getInventoryItem</a> method to retrieve an inventory item that is known to be in the inventory item group to publish, and then look for the inventory item group identifier under the <strong>groupIds</strong> container in the response of that call.  # noqa: E501

        :return: The inventory_item_group_key of this PublishByInventoryItemGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._inventory_item_group_key

    @inventory_item_group_key.setter
    def inventory_item_group_key(self, inventory_item_group_key):
        """Sets the inventory_item_group_key of this PublishByInventoryItemGroupRequest.

        This is the unique identifier of the inventory item group. All unpublished offers associated with this inventory item group will be published as a multiple-variation listing if the <strong>publishByInventoryItemGroup</strong> call is successful. The <strong>inventoryItemGroupKey</strong> identifier is automatically generated by eBay once an inventory item group is created.<br><br>To retrieve an <strong>inventoryItemGroupKey</strong> value, you can use the <a href=\"/api-docs/sell/inventory/resources/inventory_item/methods/getInventoryItem \" target=\"_blank\">getInventoryItem</a> method to retrieve an inventory item that is known to be in the inventory item group to publish, and then look for the inventory item group identifier under the <strong>groupIds</strong> container in the response of that call.  # noqa: E501

        :param inventory_item_group_key: The inventory_item_group_key of this PublishByInventoryItemGroupRequest.  # noqa: E501
        :type: str
        """

        self._inventory_item_group_key = inventory_item_group_key

    @property
    def marketplace_id(self):
        """Gets the marketplace_id of this PublishByInventoryItemGroupRequest.  # noqa: E501

        This is the unique identifier of the eBay site on which the multiple-variation listing will be published. The <strong>marketplaceId</strong> enumeration values are found in <strong>MarketplaceEnum</strong>. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/inventory/types/slr:MarketplaceEnum'>eBay API documentation</a>  # noqa: E501

        :return: The marketplace_id of this PublishByInventoryItemGroupRequest.  # noqa: E501
        :rtype: str
        """
        return self._marketplace_id

    @marketplace_id.setter
    def marketplace_id(self, marketplace_id):
        """Sets the marketplace_id of this PublishByInventoryItemGroupRequest.

        This is the unique identifier of the eBay site on which the multiple-variation listing will be published. The <strong>marketplaceId</strong> enumeration values are found in <strong>MarketplaceEnum</strong>. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/inventory/types/slr:MarketplaceEnum'>eBay API documentation</a>  # noqa: E501

        :param marketplace_id: The marketplace_id of this PublishByInventoryItemGroupRequest.  # noqa: E501
        :type: str
        """

        self._marketplace_id = marketplace_id

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
        if issubclass(PublishByInventoryItemGroupRequest, dict):
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
        if not isinstance(other, PublishByInventoryItemGroupRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
