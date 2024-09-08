# coding: utf-8

"""
    Browse API

    The Browse API has the following resources:<ul><li><b>item_summary:</b><br>Allows shoppers to search for specific items by keyword, GTIN, category, charity, product, image, or item aspects and refine the results by using filters, such as aspects, compatibility, and fields values, or UI parameters.</li><li><b>item:</b><br>Allows shoppers to retrieve the details of a specific item or all items in an item group, which is an item with variations such as color and size and check if a product is compatible with the specified item, such as if a specific car is compatible with a specific part.<br><br>This resource also provides a bridge between the eBay legacy APIs, such as the <a href=\"/api-docs/user-guides/static/finding-user-guide-landing.html\" target=\"_blank\">Finding</b>, and the RESTful APIs, which use different formats for the item IDs.</li></ul>The <b>item_summary</b>, <b>search_by_image</b>, and <b>item</b> resource calls require an <a href=\"/api-docs/static/oauth-client-credentials-grant.html\" target=\"_blank\">Application access token</a>.  # noqa: E501

    OpenAPI spec version: v1.19.8
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class BuyingOptionDistribution(object):
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
        'buying_option': 'str',
        'match_count': 'int',
        'refinement_href': 'str'
    }

    attribute_map = {
        'buying_option': 'buyingOption',
        'match_count': 'matchCount',
        'refinement_href': 'refinementHref'
    }

    def __init__(self, buying_option=None, match_count=None, refinement_href=None):  # noqa: E501
        """BuyingOptionDistribution - a model defined in Swagger"""  # noqa: E501
        self._buying_option = None
        self._match_count = None
        self._refinement_href = None
        self.discriminator = None
        if buying_option is not None:
            self.buying_option = buying_option
        if match_count is not None:
            self.match_count = match_count
        if refinement_href is not None:
            self.refinement_href = refinement_href

    @property
    def buying_option(self):
        """Gets the buying_option of this BuyingOptionDistribution.  # noqa: E501

        The container that returns the buying option type. This will be AUCTION, FIXED_PRICE, CLASSIFIED_AD, or a combination of these options. For details, see <a href=\"/api-docs/buy/browse/resources/item_summary/methods/search#response.itemSummaries.buyingOptions\">buyingOptions</a>.  # noqa: E501

        :return: The buying_option of this BuyingOptionDistribution.  # noqa: E501
        :rtype: str
        """
        return self._buying_option

    @buying_option.setter
    def buying_option(self, buying_option):
        """Sets the buying_option of this BuyingOptionDistribution.

        The container that returns the buying option type. This will be AUCTION, FIXED_PRICE, CLASSIFIED_AD, or a combination of these options. For details, see <a href=\"/api-docs/buy/browse/resources/item_summary/methods/search#response.itemSummaries.buyingOptions\">buyingOptions</a>.  # noqa: E501

        :param buying_option: The buying_option of this BuyingOptionDistribution.  # noqa: E501
        :type: str
        """

        self._buying_option = buying_option

    @property
    def match_count(self):
        """Gets the match_count of this BuyingOptionDistribution.  # noqa: E501

        The number of items having this buying option.  # noqa: E501

        :return: The match_count of this BuyingOptionDistribution.  # noqa: E501
        :rtype: int
        """
        return self._match_count

    @match_count.setter
    def match_count(self, match_count):
        """Sets the match_count of this BuyingOptionDistribution.

        The number of items having this buying option.  # noqa: E501

        :param match_count: The match_count of this BuyingOptionDistribution.  # noqa: E501
        :type: int
        """

        self._match_count = match_count

    @property
    def refinement_href(self):
        """Gets the refinement_href of this BuyingOptionDistribution.  # noqa: E501

        The HATEOAS reference for this buying option.  # noqa: E501

        :return: The refinement_href of this BuyingOptionDistribution.  # noqa: E501
        :rtype: str
        """
        return self._refinement_href

    @refinement_href.setter
    def refinement_href(self, refinement_href):
        """Sets the refinement_href of this BuyingOptionDistribution.

        The HATEOAS reference for this buying option.  # noqa: E501

        :param refinement_href: The refinement_href of this BuyingOptionDistribution.  # noqa: E501
        :type: str
        """

        self._refinement_href = refinement_href

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
        if issubclass(BuyingOptionDistribution, dict):
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
        if not isinstance(other, BuyingOptionDistribution):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
