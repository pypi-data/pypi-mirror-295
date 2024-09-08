# coding: utf-8

"""
    Taxonomy API

    Use the Taxonomy API to discover the most appropriate eBay categories under which sellers can offer inventory items for sale, and the most likely categories under which buyers can browse or search for items to purchase. In addition, the Taxonomy API provides metadata about the required and recommended category aspects to include in listings, and also has two operations to retrieve parts compatibility information.  # noqa: E501

    OpenAPI spec version: v1.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class CategorySuggestion(object):
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
        'category': 'Category',
        'category_tree_node_ancestors': 'list[AncestorReference]',
        'category_tree_node_level': 'int',
        'relevancy': 'str'
    }

    attribute_map = {
        'category': 'category',
        'category_tree_node_ancestors': 'categoryTreeNodeAncestors',
        'category_tree_node_level': 'categoryTreeNodeLevel',
        'relevancy': 'relevancy'
    }

    def __init__(self, category=None, category_tree_node_ancestors=None, category_tree_node_level=None, relevancy=None):  # noqa: E501
        """CategorySuggestion - a model defined in Swagger"""  # noqa: E501
        self._category = None
        self._category_tree_node_ancestors = None
        self._category_tree_node_level = None
        self._relevancy = None
        self.discriminator = None
        if category is not None:
            self.category = category
        if category_tree_node_ancestors is not None:
            self.category_tree_node_ancestors = category_tree_node_ancestors
        if category_tree_node_level is not None:
            self.category_tree_node_level = category_tree_node_level
        if relevancy is not None:
            self.relevancy = relevancy

    @property
    def category(self):
        """Gets the category of this CategorySuggestion.  # noqa: E501


        :return: The category of this CategorySuggestion.  # noqa: E501
        :rtype: Category
        """
        return self._category

    @category.setter
    def category(self, category):
        """Sets the category of this CategorySuggestion.


        :param category: The category of this CategorySuggestion.  # noqa: E501
        :type: Category
        """

        self._category = category

    @property
    def category_tree_node_ancestors(self):
        """Gets the category_tree_node_ancestors of this CategorySuggestion.  # noqa: E501

        An ordered list of category references that describes the location of the suggested category in the specified category tree. The list identifies the category's ancestry as a sequence of parent nodes, from the current node's immediate parent to the root node of the category tree.<br><br><span class=\"tablenote\"> <strong>Note:</strong> The root node of a full default category tree includes <b>categoryId</b> and <b>categoryName</b> fields, but their values should not be relied upon. They provide no useful information for application development.</span>  # noqa: E501

        :return: The category_tree_node_ancestors of this CategorySuggestion.  # noqa: E501
        :rtype: list[AncestorReference]
        """
        return self._category_tree_node_ancestors

    @category_tree_node_ancestors.setter
    def category_tree_node_ancestors(self, category_tree_node_ancestors):
        """Sets the category_tree_node_ancestors of this CategorySuggestion.

        An ordered list of category references that describes the location of the suggested category in the specified category tree. The list identifies the category's ancestry as a sequence of parent nodes, from the current node's immediate parent to the root node of the category tree.<br><br><span class=\"tablenote\"> <strong>Note:</strong> The root node of a full default category tree includes <b>categoryId</b> and <b>categoryName</b> fields, but their values should not be relied upon. They provide no useful information for application development.</span>  # noqa: E501

        :param category_tree_node_ancestors: The category_tree_node_ancestors of this CategorySuggestion.  # noqa: E501
        :type: list[AncestorReference]
        """

        self._category_tree_node_ancestors = category_tree_node_ancestors

    @property
    def category_tree_node_level(self):
        """Gets the category_tree_node_level of this CategorySuggestion.  # noqa: E501

        The absolute level of the category tree node in the hierarchy of its category tree.<br><br><span class=\"tablenote\"> <strong>Note:</strong> The root node of any full category tree is always at level <code><b>0</b></code>.</span>  # noqa: E501

        :return: The category_tree_node_level of this CategorySuggestion.  # noqa: E501
        :rtype: int
        """
        return self._category_tree_node_level

    @category_tree_node_level.setter
    def category_tree_node_level(self, category_tree_node_level):
        """Sets the category_tree_node_level of this CategorySuggestion.

        The absolute level of the category tree node in the hierarchy of its category tree.<br><br><span class=\"tablenote\"> <strong>Note:</strong> The root node of any full category tree is always at level <code><b>0</b></code>.</span>  # noqa: E501

        :param category_tree_node_level: The category_tree_node_level of this CategorySuggestion.  # noqa: E501
        :type: int
        """

        self._category_tree_node_level = category_tree_node_level

    @property
    def relevancy(self):
        """Gets the relevancy of this CategorySuggestion.  # noqa: E501

        This field is reserved for internal or future use.  # noqa: E501

        :return: The relevancy of this CategorySuggestion.  # noqa: E501
        :rtype: str
        """
        return self._relevancy

    @relevancy.setter
    def relevancy(self, relevancy):
        """Sets the relevancy of this CategorySuggestion.

        This field is reserved for internal or future use.  # noqa: E501

        :param relevancy: The relevancy of this CategorySuggestion.  # noqa: E501
        :type: str
        """

        self._relevancy = relevancy

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
        if issubclass(CategorySuggestion, dict):
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
        if not isinstance(other, CategorySuggestion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
