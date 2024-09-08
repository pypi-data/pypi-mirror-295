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

class PriceQuantity(object):
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
        'offers': 'list[OfferPriceQuantity]',
        'ship_to_location_availability': 'ShipToLocationAvailability',
        'sku': 'str'
    }

    attribute_map = {
        'offers': 'offers',
        'ship_to_location_availability': 'shipToLocationAvailability',
        'sku': 'sku'
    }

    def __init__(self, offers=None, ship_to_location_availability=None, sku=None):  # noqa: E501
        """PriceQuantity - a model defined in Swagger"""  # noqa: E501
        self._offers = None
        self._ship_to_location_availability = None
        self._sku = None
        self.discriminator = None
        if offers is not None:
            self.offers = offers
        if ship_to_location_availability is not None:
            self.ship_to_location_availability = ship_to_location_availability
        if sku is not None:
            self.sku = sku

    @property
    def offers(self):
        """Gets the offers of this PriceQuantity.  # noqa: E501

        This container is needed if the seller is updating the price and/or quantity of one or more published offers, and a successful call will actually update the active eBay listing with the revised price and/or available quantity.<br><br>This call is not designed to work with unpublished offers. For unpublished offers, the seller should use the <strong>updateOffer</strong> call to update the available quantity and/or price.<br><br>If the seller is also using the <strong>shipToLocationAvailability</strong> container and <strong>sku</strong> field to update the total 'ship-to-home' quantity of the inventory item, the SKU value associated with the corresponding <strong>offerId</strong> value(s) must be the same as the corresponding <strong>sku</strong> value that is passed in, or an error will occur.<br><br>A separate (<strong>OfferPriceQuantity</strong>) node is required for each offer being updated.  # noqa: E501

        :return: The offers of this PriceQuantity.  # noqa: E501
        :rtype: list[OfferPriceQuantity]
        """
        return self._offers

    @offers.setter
    def offers(self, offers):
        """Sets the offers of this PriceQuantity.

        This container is needed if the seller is updating the price and/or quantity of one or more published offers, and a successful call will actually update the active eBay listing with the revised price and/or available quantity.<br><br>This call is not designed to work with unpublished offers. For unpublished offers, the seller should use the <strong>updateOffer</strong> call to update the available quantity and/or price.<br><br>If the seller is also using the <strong>shipToLocationAvailability</strong> container and <strong>sku</strong> field to update the total 'ship-to-home' quantity of the inventory item, the SKU value associated with the corresponding <strong>offerId</strong> value(s) must be the same as the corresponding <strong>sku</strong> value that is passed in, or an error will occur.<br><br>A separate (<strong>OfferPriceQuantity</strong>) node is required for each offer being updated.  # noqa: E501

        :param offers: The offers of this PriceQuantity.  # noqa: E501
        :type: list[OfferPriceQuantity]
        """

        self._offers = offers

    @property
    def ship_to_location_availability(self):
        """Gets the ship_to_location_availability of this PriceQuantity.  # noqa: E501


        :return: The ship_to_location_availability of this PriceQuantity.  # noqa: E501
        :rtype: ShipToLocationAvailability
        """
        return self._ship_to_location_availability

    @ship_to_location_availability.setter
    def ship_to_location_availability(self, ship_to_location_availability):
        """Sets the ship_to_location_availability of this PriceQuantity.


        :param ship_to_location_availability: The ship_to_location_availability of this PriceQuantity.  # noqa: E501
        :type: ShipToLocationAvailability
        """

        self._ship_to_location_availability = ship_to_location_availability

    @property
    def sku(self):
        """Gets the sku of this PriceQuantity.  # noqa: E501

        This is the seller-defined SKU value of the inventory item whose total 'ship-to-home' quantity will be updated. This field is only required when the seller is updating the total quantity of an inventory item using the <strong>shipToLocationAvailability</strong> container. If the seller is updating the price and/or quantity of one or more specific offers, one or more <strong>offerId</strong> values are used instead, and the <strong>sku</strong> value is not needed.<br><br>If the seller wants to update the price and/or quantity of one or more offers, and also wants to update the total 'ship-to-home' quantity of the corresponding inventory item, the SKU value associated with the <strong>offerId</strong> value(s) must be the same as the corresponding <strong>sku</strong> value that is passed in, or an error will occur.<br><br>Use the <a href=\"/api-docs/sell/inventory/resources/inventory_item/methods/getInventoryItems\" target=\"_blank \">getInventoryItems</a> method to retrieve SKU values.<br><br><strong>Max Length</strong>: 50<br>  # noqa: E501

        :return: The sku of this PriceQuantity.  # noqa: E501
        :rtype: str
        """
        return self._sku

    @sku.setter
    def sku(self, sku):
        """Sets the sku of this PriceQuantity.

        This is the seller-defined SKU value of the inventory item whose total 'ship-to-home' quantity will be updated. This field is only required when the seller is updating the total quantity of an inventory item using the <strong>shipToLocationAvailability</strong> container. If the seller is updating the price and/or quantity of one or more specific offers, one or more <strong>offerId</strong> values are used instead, and the <strong>sku</strong> value is not needed.<br><br>If the seller wants to update the price and/or quantity of one or more offers, and also wants to update the total 'ship-to-home' quantity of the corresponding inventory item, the SKU value associated with the <strong>offerId</strong> value(s) must be the same as the corresponding <strong>sku</strong> value that is passed in, or an error will occur.<br><br>Use the <a href=\"/api-docs/sell/inventory/resources/inventory_item/methods/getInventoryItems\" target=\"_blank \">getInventoryItems</a> method to retrieve SKU values.<br><br><strong>Max Length</strong>: 50<br>  # noqa: E501

        :param sku: The sku of this PriceQuantity.  # noqa: E501
        :type: str
        """

        self._sku = sku

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
        if issubclass(PriceQuantity, dict):
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
        if not isinstance(other, PriceQuantity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
