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

class InventoryLocationFull(object):
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
        'location': 'LocationDetails',
        'location_additional_information': 'str',
        'location_instructions': 'str',
        'location_types': 'list[str]',
        'location_web_url': 'str',
        'merchant_location_status': 'str',
        'name': 'str',
        'operating_hours': 'list[OperatingHours]',
        'phone': 'str',
        'special_hours': 'list[SpecialHours]'
    }

    attribute_map = {
        'location': 'location',
        'location_additional_information': 'locationAdditionalInformation',
        'location_instructions': 'locationInstructions',
        'location_types': 'locationTypes',
        'location_web_url': 'locationWebUrl',
        'merchant_location_status': 'merchantLocationStatus',
        'name': 'name',
        'operating_hours': 'operatingHours',
        'phone': 'phone',
        'special_hours': 'specialHours'
    }

    def __init__(self, location=None, location_additional_information=None, location_instructions=None, location_types=None, location_web_url=None, merchant_location_status=None, name=None, operating_hours=None, phone=None, special_hours=None):  # noqa: E501
        """InventoryLocationFull - a model defined in Swagger"""  # noqa: E501
        self._location = None
        self._location_additional_information = None
        self._location_instructions = None
        self._location_types = None
        self._location_web_url = None
        self._merchant_location_status = None
        self._name = None
        self._operating_hours = None
        self._phone = None
        self._special_hours = None
        self.discriminator = None
        if location is not None:
            self.location = location
        if location_additional_information is not None:
            self.location_additional_information = location_additional_information
        if location_instructions is not None:
            self.location_instructions = location_instructions
        if location_types is not None:
            self.location_types = location_types
        if location_web_url is not None:
            self.location_web_url = location_web_url
        if merchant_location_status is not None:
            self.merchant_location_status = merchant_location_status
        if name is not None:
            self.name = name
        if operating_hours is not None:
            self.operating_hours = operating_hours
        if phone is not None:
            self.phone = phone
        if special_hours is not None:
            self.special_hours = special_hours

    @property
    def location(self):
        """Gets the location of this InventoryLocationFull.  # noqa: E501


        :return: The location of this InventoryLocationFull.  # noqa: E501
        :rtype: LocationDetails
        """
        return self._location

    @location.setter
    def location(self, location):
        """Sets the location of this InventoryLocationFull.


        :param location: The location of this InventoryLocationFull.  # noqa: E501
        :type: LocationDetails
        """

        self._location = location

    @property
    def location_additional_information(self):
        """Gets the location_additional_information of this InventoryLocationFull.  # noqa: E501

        This text field is used by the merchant to provide additional information about an inventory location. <br><br><b>Max length</b>: 256  # noqa: E501

        :return: The location_additional_information of this InventoryLocationFull.  # noqa: E501
        :rtype: str
        """
        return self._location_additional_information

    @location_additional_information.setter
    def location_additional_information(self, location_additional_information):
        """Sets the location_additional_information of this InventoryLocationFull.

        This text field is used by the merchant to provide additional information about an inventory location. <br><br><b>Max length</b>: 256  # noqa: E501

        :param location_additional_information: The location_additional_information of this InventoryLocationFull.  # noqa: E501
        :type: str
        """

        self._location_additional_information = location_additional_information

    @property
    def location_instructions(self):
        """Gets the location_instructions of this InventoryLocationFull.  # noqa: E501

        This text field is generally used by the merchant to provide special pickup instructions for a store inventory location. Although this field is optional, it is recommended that merchants provide this field to create a pleasant and easy pickup experience for In-Store Pickup and Click and Collect orders. If this field is not included in the call request payload, eBay will use the default pickup instructions contained in the merchant's profile (if available).  # noqa: E501

        :return: The location_instructions of this InventoryLocationFull.  # noqa: E501
        :rtype: str
        """
        return self._location_instructions

    @location_instructions.setter
    def location_instructions(self, location_instructions):
        """Sets the location_instructions of this InventoryLocationFull.

        This text field is generally used by the merchant to provide special pickup instructions for a store inventory location. Although this field is optional, it is recommended that merchants provide this field to create a pleasant and easy pickup experience for In-Store Pickup and Click and Collect orders. If this field is not included in the call request payload, eBay will use the default pickup instructions contained in the merchant's profile (if available).  # noqa: E501

        :param location_instructions: The location_instructions of this InventoryLocationFull.  # noqa: E501
        :type: str
        """

        self._location_instructions = location_instructions

    @property
    def location_types(self):
        """Gets the location_types of this InventoryLocationFull.  # noqa: E501

        This container is used to define the function of the inventory location. Typically, an inventory location will serve as a store or a warehouse, but in some cases, an inventory location may be both.<br><br>For In-Store Pickup inventory, set <b>StoreTypeEnum</b> to <code>STORE</code>.<br><br>If this container is omitted, the location type of the inventory location will default to <code>WAREHOUSE</code>. See <a href=\"/api-docs/sell/inventory/types/api:StoreTypeEnum\">StoreTypeEnum</a> for the supported values.<br><br><b>Default</b>: WAREHOUSE  # noqa: E501

        :return: The location_types of this InventoryLocationFull.  # noqa: E501
        :rtype: list[str]
        """
        return self._location_types

    @location_types.setter
    def location_types(self, location_types):
        """Sets the location_types of this InventoryLocationFull.

        This container is used to define the function of the inventory location. Typically, an inventory location will serve as a store or a warehouse, but in some cases, an inventory location may be both.<br><br>For In-Store Pickup inventory, set <b>StoreTypeEnum</b> to <code>STORE</code>.<br><br>If this container is omitted, the location type of the inventory location will default to <code>WAREHOUSE</code>. See <a href=\"/api-docs/sell/inventory/types/api:StoreTypeEnum\">StoreTypeEnum</a> for the supported values.<br><br><b>Default</b>: WAREHOUSE  # noqa: E501

        :param location_types: The location_types of this InventoryLocationFull.  # noqa: E501
        :type: list[str]
        """

        self._location_types = location_types

    @property
    def location_web_url(self):
        """Gets the location_web_url of this InventoryLocationFull.  # noqa: E501

        This text field is used by the merchant to provide the Website address (URL) associated with the inventory location. <br><br><b>Max length</b>: 512  # noqa: E501

        :return: The location_web_url of this InventoryLocationFull.  # noqa: E501
        :rtype: str
        """
        return self._location_web_url

    @location_web_url.setter
    def location_web_url(self, location_web_url):
        """Sets the location_web_url of this InventoryLocationFull.

        This text field is used by the merchant to provide the Website address (URL) associated with the inventory location. <br><br><b>Max length</b>: 512  # noqa: E501

        :param location_web_url: The location_web_url of this InventoryLocationFull.  # noqa: E501
        :type: str
        """

        self._location_web_url = location_web_url

    @property
    def merchant_location_status(self):
        """Gets the merchant_location_status of this InventoryLocationFull.  # noqa: E501

        This field is used to indicate whether the inventory location will be enabled (inventory can be loaded to location) or disabled (inventory can not be loaded to location). If this field is omitted, a successful <strong>createInventoryLocation</strong> call will automatically enable the inventory location. A merchant may want to create a new inventory location but leave it as disabled if the inventory location is not yet ready for active inventory. Once the inventory location is ready, the merchant can use the <strong>enableInventoryLocation</strong> call to enable an inventory location that is in a disabled state.<br><br>See <a href=\"/api-docs/sell/inventory/types/api:StatusEnum\">StatusEnum</a> for the supported values.  <br><br><b>Default</b>: ENABLED For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/inventory/types/api:StatusEnum'>eBay API documentation</a>  # noqa: E501

        :return: The merchant_location_status of this InventoryLocationFull.  # noqa: E501
        :rtype: str
        """
        return self._merchant_location_status

    @merchant_location_status.setter
    def merchant_location_status(self, merchant_location_status):
        """Sets the merchant_location_status of this InventoryLocationFull.

        This field is used to indicate whether the inventory location will be enabled (inventory can be loaded to location) or disabled (inventory can not be loaded to location). If this field is omitted, a successful <strong>createInventoryLocation</strong> call will automatically enable the inventory location. A merchant may want to create a new inventory location but leave it as disabled if the inventory location is not yet ready for active inventory. Once the inventory location is ready, the merchant can use the <strong>enableInventoryLocation</strong> call to enable an inventory location that is in a disabled state.<br><br>See <a href=\"/api-docs/sell/inventory/types/api:StatusEnum\">StatusEnum</a> for the supported values.  <br><br><b>Default</b>: ENABLED For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/inventory/types/api:StatusEnum'>eBay API documentation</a>  # noqa: E501

        :param merchant_location_status: The merchant_location_status of this InventoryLocationFull.  # noqa: E501
        :type: str
        """

        self._merchant_location_status = merchant_location_status

    @property
    def name(self):
        """Gets the name of this InventoryLocationFull.  # noqa: E501

        The seller-defined name of the inventory location. This name should be a human-friendly name as it will be displayed in In-Store Pickup and Click and Collect listings. A name is not required for warehouse inventory locations. For store inventory locations, this field is not immediately required, but will be required before an offer enabled with the In-Store Pickup or Click and Collect capability can be published. So, if the seller omits this field in a <strong>createInventoryLocation</strong> call, it becomes required for an <strong>updateInventoryLocation</strong> call.<br><br><b>Max length</b>: 1000  # noqa: E501

        :return: The name of this InventoryLocationFull.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InventoryLocationFull.

        The seller-defined name of the inventory location. This name should be a human-friendly name as it will be displayed in In-Store Pickup and Click and Collect listings. A name is not required for warehouse inventory locations. For store inventory locations, this field is not immediately required, but will be required before an offer enabled with the In-Store Pickup or Click and Collect capability can be published. So, if the seller omits this field in a <strong>createInventoryLocation</strong> call, it becomes required for an <strong>updateInventoryLocation</strong> call.<br><br><b>Max length</b>: 1000  # noqa: E501

        :param name: The name of this InventoryLocationFull.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def operating_hours(self):
        """Gets the operating_hours of this InventoryLocationFull.  # noqa: E501

        Although not technically required, this container is highly recommended to be used to specify operating hours for a store inventory location. This container is used to express the regular operating hours for a store location during each day of the week. A <strong>dayOfWeekEnum</strong> field and an <strong>intervals</strong> container will be needed for each day of the week that the store location is open.  # noqa: E501

        :return: The operating_hours of this InventoryLocationFull.  # noqa: E501
        :rtype: list[OperatingHours]
        """
        return self._operating_hours

    @operating_hours.setter
    def operating_hours(self, operating_hours):
        """Sets the operating_hours of this InventoryLocationFull.

        Although not technically required, this container is highly recommended to be used to specify operating hours for a store inventory location. This container is used to express the regular operating hours for a store location during each day of the week. A <strong>dayOfWeekEnum</strong> field and an <strong>intervals</strong> container will be needed for each day of the week that the store location is open.  # noqa: E501

        :param operating_hours: The operating_hours of this InventoryLocationFull.  # noqa: E501
        :type: list[OperatingHours]
        """

        self._operating_hours = operating_hours

    @property
    def phone(self):
        """Gets the phone of this InventoryLocationFull.  # noqa: E501

        This field is used to specify the phone number for an inventory location. <br><br><b>Max length</b>: 36  # noqa: E501

        :return: The phone of this InventoryLocationFull.  # noqa: E501
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, phone):
        """Sets the phone of this InventoryLocationFull.

        This field is used to specify the phone number for an inventory location. <br><br><b>Max length</b>: 36  # noqa: E501

        :param phone: The phone of this InventoryLocationFull.  # noqa: E501
        :type: str
        """

        self._phone = phone

    @property
    def special_hours(self):
        """Gets the special_hours of this InventoryLocationFull.  # noqa: E501

        This container is used to express the special operating hours for a store inventory location on a specific date, such as a holiday. The special hours specified for the specific date will override the normal operating hours for that particular day of the week.  # noqa: E501

        :return: The special_hours of this InventoryLocationFull.  # noqa: E501
        :rtype: list[SpecialHours]
        """
        return self._special_hours

    @special_hours.setter
    def special_hours(self, special_hours):
        """Sets the special_hours of this InventoryLocationFull.

        This container is used to express the special operating hours for a store inventory location on a specific date, such as a holiday. The special hours specified for the specific date will override the normal operating hours for that particular day of the week.  # noqa: E501

        :param special_hours: The special_hours of this InventoryLocationFull.  # noqa: E501
        :type: list[SpecialHours]
        """

        self._special_hours = special_hours

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
        if issubclass(InventoryLocationFull, dict):
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
        if not isinstance(other, InventoryLocationFull):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
