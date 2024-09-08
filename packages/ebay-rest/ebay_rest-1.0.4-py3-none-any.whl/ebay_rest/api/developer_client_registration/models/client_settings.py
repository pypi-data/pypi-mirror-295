# coding: utf-8

"""
    Developer Registration API

    <span class=\"tablenote\"><b>Note:</b> The Client Registration API is not intended for use by developers who have previously registered for a Developer Account on the eBay platform.</span><br/>The Client Registration API provides Dynamic Client Registration for regulated Third Party Providers (TPPs) who are, or will be, engaged in financial transactions on behalf of individuals domiciled in the EU/UK. This is required by the EU's Second Payment Services Directive (PSD2) which requires all regulated Account Servicing Payment Service Providers (ASPSPs) to provide secure APIs to access account and payment services on behalf of account holders.<br/><br/>A successful registration response returns a <b>HTTP 201 Created</b> status code with a JSON payload [RFC7519] that includes registration information.  # noqa: E501

    OpenAPI spec version: v1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ClientSettings(object):
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
        'client_name': 'str',
        'contacts': 'list[str]',
        'policy_uri': 'str',
        'redirect_uris': 'list[str]',
        'software_id': 'str',
        'software_statement': 'str'
    }

    attribute_map = {
        'client_name': 'client_name',
        'contacts': 'contacts',
        'policy_uri': 'policy_uri',
        'redirect_uris': 'redirect_uris',
        'software_id': 'software_id',
        'software_statement': 'software_statement'
    }

    def __init__(self, client_name=None, contacts=None, policy_uri=None, redirect_uris=None, software_id=None, software_statement=None):  # noqa: E501
        """ClientSettings - a model defined in Swagger"""  # noqa: E501
        self._client_name = None
        self._contacts = None
        self._policy_uri = None
        self._redirect_uris = None
        self._software_id = None
        self._software_statement = None
        self.discriminator = None
        if client_name is not None:
            self.client_name = client_name
        if contacts is not None:
            self.contacts = contacts
        if policy_uri is not None:
            self.policy_uri = policy_uri
        if redirect_uris is not None:
            self.redirect_uris = redirect_uris
        if software_id is not None:
            self.software_id = software_id
        if software_statement is not None:
            self.software_statement = software_statement

    @property
    def client_name(self):
        """Gets the client_name of this ClientSettings.  # noqa: E501

        User-friendly name for the third party financial application.<br/><br/><span class=\"tablenote\"><b>Note:</b> Language tags are not supported. Therefore, <code>client_name</code> must be specified in English.</span>  # noqa: E501

        :return: The client_name of this ClientSettings.  # noqa: E501
        :rtype: str
        """
        return self._client_name

    @client_name.setter
    def client_name(self, client_name):
        """Sets the client_name of this ClientSettings.

        User-friendly name for the third party financial application.<br/><br/><span class=\"tablenote\"><b>Note:</b> Language tags are not supported. Therefore, <code>client_name</code> must be specified in English.</span>  # noqa: E501

        :param client_name: The client_name of this ClientSettings.  # noqa: E501
        :type: str
        """

        self._client_name = client_name

    @property
    def contacts(self):
        """Gets the contacts of this ClientSettings.  # noqa: E501

        This container stores an array of email addresses that can be used to contact the registrant.<br/><br/><span class=\"tablenote\"><b>Note:</b> When more than one email address is provided, the first email in the array will be used as the developer account's email address. All other email addresses will be used as general contact information.</span>  # noqa: E501

        :return: The contacts of this ClientSettings.  # noqa: E501
        :rtype: list[str]
        """
        return self._contacts

    @contacts.setter
    def contacts(self, contacts):
        """Sets the contacts of this ClientSettings.

        This container stores an array of email addresses that can be used to contact the registrant.<br/><br/><span class=\"tablenote\"><b>Note:</b> When more than one email address is provided, the first email in the array will be used as the developer account's email address. All other email addresses will be used as general contact information.</span>  # noqa: E501

        :param contacts: The contacts of this ClientSettings.  # noqa: E501
        :type: list[str]
        """

        self._contacts = contacts

    @property
    def policy_uri(self):
        """Gets the policy_uri of this ClientSettings.  # noqa: E501

        The URL string pointing to a human-readable privacy policy document that describes how the third party provider collects, uses, retains, and discloses personal data.<br/><br/><span class=\"tablenote\"><b>Note:</b> Only HTTPS URLs are supported for <code>policy_uri</code> strings.</span><br/><span class=\"tablenote\"><b>Note:</b> This URL <b>must not</b> point to the eBay Privacy Policy.</span><br/>The value of this field <b>must</b> point to a valid and secure web page.<br/><br/><span class=\"tablenote\"><b>Note:</b> Language tags are not supported. Therefore, <code>policy_uri</code> will be displayed in English.</span>  # noqa: E501

        :return: The policy_uri of this ClientSettings.  # noqa: E501
        :rtype: str
        """
        return self._policy_uri

    @policy_uri.setter
    def policy_uri(self, policy_uri):
        """Sets the policy_uri of this ClientSettings.

        The URL string pointing to a human-readable privacy policy document that describes how the third party provider collects, uses, retains, and discloses personal data.<br/><br/><span class=\"tablenote\"><b>Note:</b> Only HTTPS URLs are supported for <code>policy_uri</code> strings.</span><br/><span class=\"tablenote\"><b>Note:</b> This URL <b>must not</b> point to the eBay Privacy Policy.</span><br/>The value of this field <b>must</b> point to a valid and secure web page.<br/><br/><span class=\"tablenote\"><b>Note:</b> Language tags are not supported. Therefore, <code>policy_uri</code> will be displayed in English.</span>  # noqa: E501

        :param policy_uri: The policy_uri of this ClientSettings.  # noqa: E501
        :type: str
        """

        self._policy_uri = policy_uri

    @property
    def redirect_uris(self):
        """Gets the redirect_uris of this ClientSettings.  # noqa: E501

        An array of redirection URI strings for use in redirect-based flows such as the authorization code and implicit flows.<br/><br/><span class=\"tablenote\"><b>Note:</b> Only the first URI string from the list will be used.</span><span class=\"tablenote\"><b>Note:</b> Each redirection URI <b>must</b> be an absolute URI as defined by [RFC3986] Section 4.3.</span>  # noqa: E501

        :return: The redirect_uris of this ClientSettings.  # noqa: E501
        :rtype: list[str]
        """
        return self._redirect_uris

    @redirect_uris.setter
    def redirect_uris(self, redirect_uris):
        """Sets the redirect_uris of this ClientSettings.

        An array of redirection URI strings for use in redirect-based flows such as the authorization code and implicit flows.<br/><br/><span class=\"tablenote\"><b>Note:</b> Only the first URI string from the list will be used.</span><span class=\"tablenote\"><b>Note:</b> Each redirection URI <b>must</b> be an absolute URI as defined by [RFC3986] Section 4.3.</span>  # noqa: E501

        :param redirect_uris: The redirect_uris of this ClientSettings.  # noqa: E501
        :type: list[str]
        """

        self._redirect_uris = redirect_uris

    @property
    def software_id(self):
        """Gets the software_id of this ClientSettings.  # noqa: E501

        A unique identifier string assigned by the client developer or software publisher to identify the client software being registered.<br/><br/>Unlike <code>client_id</code> which should change between instances, the <CODE>software_id</code> should be the same value for all instances of the client software. That is, the <code>software_id</code> should remain unchanged across multiple updates or versions of the same piece of software. The value of this field is not intended to be human readable and is usually opaque to the client and authorization server.  # noqa: E501

        :return: The software_id of this ClientSettings.  # noqa: E501
        :rtype: str
        """
        return self._software_id

    @software_id.setter
    def software_id(self, software_id):
        """Sets the software_id of this ClientSettings.

        A unique identifier string assigned by the client developer or software publisher to identify the client software being registered.<br/><br/>Unlike <code>client_id</code> which should change between instances, the <CODE>software_id</code> should be the same value for all instances of the client software. That is, the <code>software_id</code> should remain unchanged across multiple updates or versions of the same piece of software. The value of this field is not intended to be human readable and is usually opaque to the client and authorization server.  # noqa: E501

        :param software_id: The software_id of this ClientSettings.  # noqa: E501
        :type: str
        """

        self._software_id = software_id

    @property
    def software_statement(self):
        """Gets the software_statement of this ClientSettings.  # noqa: E501

        The Software Statement Assertion (SSA) that has been issued by the OpenBanking identifier.<br/><br/><span class=\"tablenote\"><b>Note:</b> This value <i>must be</i> <b>Base64</b> encoded and not plain JSON.</span>Refer to <a href=\"https://datatracker.ietf.org/doc/html/rfc7591#section-2.3 \" target= \"_blank \">RFC 7591 - OAuth 2.0 Dynamic Client Registration Protocol</a> for complete information.  # noqa: E501

        :return: The software_statement of this ClientSettings.  # noqa: E501
        :rtype: str
        """
        return self._software_statement

    @software_statement.setter
    def software_statement(self, software_statement):
        """Sets the software_statement of this ClientSettings.

        The Software Statement Assertion (SSA) that has been issued by the OpenBanking identifier.<br/><br/><span class=\"tablenote\"><b>Note:</b> This value <i>must be</i> <b>Base64</b> encoded and not plain JSON.</span>Refer to <a href=\"https://datatracker.ietf.org/doc/html/rfc7591#section-2.3 \" target= \"_blank \">RFC 7591 - OAuth 2.0 Dynamic Client Registration Protocol</a> for complete information.  # noqa: E501

        :param software_statement: The software_statement of this ClientSettings.  # noqa: E501
        :type: str
        """

        self._software_statement = software_statement

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
        if issubclass(ClientSettings, dict):
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
        if not isinstance(other, ClientSettings):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
