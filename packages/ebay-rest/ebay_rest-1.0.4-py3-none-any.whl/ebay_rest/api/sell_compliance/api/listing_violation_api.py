# coding: utf-8

"""
    Compliance API

    Service for providing information to sellers about their listings being non-compliant, or at risk for becoming non-compliant, against eBay listing policies.  # noqa: E501

    OpenAPI spec version: 1.4.3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from ...sell_compliance.api_client import ApiClient


class ListingViolationApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_listing_violations(self, x_ebay_c_marketplace_id, compliance_type, **kwargs):  # noqa: E501
        """get_listing_violations  # noqa: E501

        This call returns specific listing violations for the supported listing compliance types. Only one compliance type can be passed in per call, and the response will include all the listing violations for this compliance type, and listing violations are grouped together by eBay listing ID. See <a href=\"/api-docs/sell/compliance/types/com:ComplianceTypeEnum\">ComplianceTypeEnum</a> for more information on the supported listing compliance types. This method also has pagination control. <br /><br /> <span class=\"tablenote\"><strong>Note:</strong> A maximum of 2000 listing violations will be returned in a result set. If the seller has more than 2000 listing violations, some/all of those listing violations must be corrected before additional listing violations will be retrieved. The user should pay attention to the <strong>total</strong> value in the response. If this value is '2000', it is possible that the seller has more than 2000 listing violations, but this field maxes out at 2000. </span> <br /><span class=\"tablenote\"><strong>Note:</strong> In a future release of this API, the seller will be able to pass in a specific eBay listing ID as a query parameter to see if this specific listing has any violations. </span><br /> <span class=\"tablenote\"><strong>Note:</strong> Only mocked non-compliant listing data will be returned for this call in the Sandbox environment, and not specific to the seller. However, the user can still use this mock data to experiment with the compliance type filters and pagination control.</span>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_listing_violations(x_ebay_c_marketplace_id, compliance_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_ebay_c_marketplace_id: This header identifies the seller's eBay marketplace. <br><br>Supported values for this header can be found in the <a href=\"/api-docs/sell/compliance/types/bas:MarketplaceIdEnum\">MarketplaceIdEnum</a> type definition. (required)
        :param str compliance_type: This query parameter specifies the compliance type of the listing violations being retrieved. Only one compliance type value can be specified. <br> <br>See <a href=\"/api-docs/sell/compliance/types/com:ComplianceTypeEnum\">ComplianceTypeEnum</a> for more information on supported compliance types. (required)
        :param str offset: The integer value input into this field controls the first listing violation in the result set that will be displayed at the top of the response. The <strong>offset</strong> and <strong>limit</strong> query parameters are used to control the pagination of the output. For example, if <strong>offset</strong> is set to <code>10</code> and <strong>limit</strong> is set to <code>10</code>, the call retrieves listing violations 11 thru 20 from the resulting set of violations. <br /><br /> <span class=\"tablenote\"><strong>Note:</strong> This feature employs a zero-based index, where the first item in the list has an offset of <code>0</code>. If the <strong>listing_id</strong> parameter is included in the request, this parameter will be ignored.</span><br/><br/> <strong>Default: </strong> <code>0</code> {zero)
        :param str listing_id: <span class=\"tablenote\"><strong>Note:</strong> This query parameter is not yet supported for the Compliance API.</span>
        :param str limit: This query parameter is used if the user wants to set a limit on the number of listing violations that are returned on one page of the result set. This parameter is used in conjunction with the <strong>offset</strong> parameter to control the pagination of the output.<br /><br />For example, if <strong>offset</strong> is set to <code>10</code> and <strong>limit</strong> is set to <code>10</code>, the call retrieves listing violations 11 thru 20 from the collection of listing violations that match the value set in the <strong>compliance_type</strong> parameter.<br /><br /><span class=\"tablenote\"><strong>Note:</strong> This feature employs a zero-based index, where the first item in the list has an offset of <code>0</code>. If the <strong>listing_id</strong> parameter is included in the request, this parameter will be ignored.</span><br/><br/><strong>Default:</strong> <code>100</code><br/> <strong>Maximum:</strong> <code>200</code>
        :param str filter: This filter allows a user to retrieve only listings that are currently out of compliance, or only listings that are at risk of becoming out of compliance.<br><br> Although other filters may be added in the future, <code>complianceState</code> is the only supported filter type at this time. See the <a href=\"/api-docs/sell/compliance/types/com:ComplianceStateEnum\">ComplianceStateEnum</a> type for a list of supported values.<br><br>Below is an example of how to set up this compliance state filter. Notice that the filter type and filter value are separated with a colon (:) character, and the filter value is wrapped with curly brackets.<br><br> <code>filter=complianceState:{OUT_OF_COMPLIANCE}</code>
        :return: PagedComplianceViolationCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_listing_violations_with_http_info(x_ebay_c_marketplace_id, compliance_type, **kwargs)  # noqa: E501
        else:
            (data) = self.get_listing_violations_with_http_info(x_ebay_c_marketplace_id, compliance_type, **kwargs)  # noqa: E501
            return data

    def get_listing_violations_with_http_info(self, x_ebay_c_marketplace_id, compliance_type, **kwargs):  # noqa: E501
        """get_listing_violations  # noqa: E501

        This call returns specific listing violations for the supported listing compliance types. Only one compliance type can be passed in per call, and the response will include all the listing violations for this compliance type, and listing violations are grouped together by eBay listing ID. See <a href=\"/api-docs/sell/compliance/types/com:ComplianceTypeEnum\">ComplianceTypeEnum</a> for more information on the supported listing compliance types. This method also has pagination control. <br /><br /> <span class=\"tablenote\"><strong>Note:</strong> A maximum of 2000 listing violations will be returned in a result set. If the seller has more than 2000 listing violations, some/all of those listing violations must be corrected before additional listing violations will be retrieved. The user should pay attention to the <strong>total</strong> value in the response. If this value is '2000', it is possible that the seller has more than 2000 listing violations, but this field maxes out at 2000. </span> <br /><span class=\"tablenote\"><strong>Note:</strong> In a future release of this API, the seller will be able to pass in a specific eBay listing ID as a query parameter to see if this specific listing has any violations. </span><br /> <span class=\"tablenote\"><strong>Note:</strong> Only mocked non-compliant listing data will be returned for this call in the Sandbox environment, and not specific to the seller. However, the user can still use this mock data to experiment with the compliance type filters and pagination control.</span>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_listing_violations_with_http_info(x_ebay_c_marketplace_id, compliance_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str x_ebay_c_marketplace_id: This header identifies the seller's eBay marketplace. <br><br>Supported values for this header can be found in the <a href=\"/api-docs/sell/compliance/types/bas:MarketplaceIdEnum\">MarketplaceIdEnum</a> type definition. (required)
        :param str compliance_type: This query parameter specifies the compliance type of the listing violations being retrieved. Only one compliance type value can be specified. <br> <br>See <a href=\"/api-docs/sell/compliance/types/com:ComplianceTypeEnum\">ComplianceTypeEnum</a> for more information on supported compliance types. (required)
        :param str offset: The integer value input into this field controls the first listing violation in the result set that will be displayed at the top of the response. The <strong>offset</strong> and <strong>limit</strong> query parameters are used to control the pagination of the output. For example, if <strong>offset</strong> is set to <code>10</code> and <strong>limit</strong> is set to <code>10</code>, the call retrieves listing violations 11 thru 20 from the resulting set of violations. <br /><br /> <span class=\"tablenote\"><strong>Note:</strong> This feature employs a zero-based index, where the first item in the list has an offset of <code>0</code>. If the <strong>listing_id</strong> parameter is included in the request, this parameter will be ignored.</span><br/><br/> <strong>Default: </strong> <code>0</code> {zero)
        :param str listing_id: <span class=\"tablenote\"><strong>Note:</strong> This query parameter is not yet supported for the Compliance API.</span>
        :param str limit: This query parameter is used if the user wants to set a limit on the number of listing violations that are returned on one page of the result set. This parameter is used in conjunction with the <strong>offset</strong> parameter to control the pagination of the output.<br /><br />For example, if <strong>offset</strong> is set to <code>10</code> and <strong>limit</strong> is set to <code>10</code>, the call retrieves listing violations 11 thru 20 from the collection of listing violations that match the value set in the <strong>compliance_type</strong> parameter.<br /><br /><span class=\"tablenote\"><strong>Note:</strong> This feature employs a zero-based index, where the first item in the list has an offset of <code>0</code>. If the <strong>listing_id</strong> parameter is included in the request, this parameter will be ignored.</span><br/><br/><strong>Default:</strong> <code>100</code><br/> <strong>Maximum:</strong> <code>200</code>
        :param str filter: This filter allows a user to retrieve only listings that are currently out of compliance, or only listings that are at risk of becoming out of compliance.<br><br> Although other filters may be added in the future, <code>complianceState</code> is the only supported filter type at this time. See the <a href=\"/api-docs/sell/compliance/types/com:ComplianceStateEnum\">ComplianceStateEnum</a> type for a list of supported values.<br><br>Below is an example of how to set up this compliance state filter. Notice that the filter type and filter value are separated with a colon (:) character, and the filter value is wrapped with curly brackets.<br><br> <code>filter=complianceState:{OUT_OF_COMPLIANCE}</code>
        :return: PagedComplianceViolationCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['x_ebay_c_marketplace_id', 'compliance_type', 'offset', 'listing_id', 'limit', 'filter']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_listing_violations" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'x_ebay_c_marketplace_id' is set
        if ('x_ebay_c_marketplace_id' not in params or
                params['x_ebay_c_marketplace_id'] is None):
            raise ValueError("Missing the required parameter `x_ebay_c_marketplace_id` when calling `get_listing_violations`")  # noqa: E501
        # verify the required parameter 'compliance_type' is set
        if ('compliance_type' not in params or
                params['compliance_type'] is None):
            raise ValueError("Missing the required parameter `compliance_type` when calling `get_listing_violations`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'compliance_type' in params:
            query_params.append(('compliance_type', params['compliance_type']))  # noqa: E501
        if 'offset' in params:
            query_params.append(('offset', params['offset']))  # noqa: E501
        if 'listing_id' in params:
            query_params.append(('listing_id', params['listing_id']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'filter' in params:
            query_params.append(('filter', params['filter']))  # noqa: E501

        header_params = {}
        if 'x_ebay_c_marketplace_id' in params:
            header_params['X-EBAY-C-MARKETPLACE-ID'] = params['x_ebay_c_marketplace_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json;charset=UTF-8'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_auth']  # noqa: E501

        return self.api_client.call_api(
            '/listing_violation', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='PagedComplianceViolationCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
