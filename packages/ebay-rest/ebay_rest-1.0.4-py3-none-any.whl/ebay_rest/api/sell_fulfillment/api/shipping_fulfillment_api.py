# coding: utf-8

"""
    Fulfillment API

    Use the Fulfillment API to complete the process of packaging, addressing, handling, and shipping each order on behalf of the seller, in accordance with the payment method and timing specified at checkout.  # noqa: E501

    OpenAPI spec version: v1.20.4
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from ...sell_fulfillment.api_client import ApiClient


class ShippingFulfillmentApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_shipping_fulfillment(self, body, content_type, order_id, **kwargs):  # noqa: E501
        """create_shipping_fulfillment  # noqa: E501

        When you group an order's line items into one or more packages, each package requires a corresponding plan for handling, addressing, and shipping; this is a <i>shipping fulfillment</i>. For each package, execute this call once to generate a shipping fulfillment associated with that package. <br><br> <span class=\"tablenote\"><strong>Note:</strong> A single line item in an order can consist of multiple units of a purchased item, and one unit can consist of multiple parts or components. Although these components might be provided by the manufacturer in separate packaging, the seller must include all components of a given line item in the same package.</span> <br><br>Before using this call for a given package, you must determine which line items are in the package. If the package has been shipped, you should provide the date of shipment in the request. If not provided, it will default to the current date and time.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_shipping_fulfillment(body, content_type, order_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ShippingFulfillmentDetails body: fulfillment payload (required)
        :param str content_type: This header indicates the format of the request body provided by the client. Its value should be set to <b>application/json</b>. <br><br> For more information, refer to <a href=\"/api-docs/static/rest-request-components.html#HTTP\" target=\"_blank \">HTTP request headers</a>. (required)
        :param str order_id: This path parameter is used to specify the unique identifier of the order associated with the shipping fulfillment being created.<br><br> Use the <a href=\"/api-docs/sell/fulfillment/resources/order/methods/getOrders\" target=\"_blank \">getOrders</a> method to retrieve order IDs. (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.create_shipping_fulfillment_with_http_info(body, content_type, order_id, **kwargs)  # noqa: E501
        else:
            (data) = self.create_shipping_fulfillment_with_http_info(body, content_type, order_id, **kwargs)  # noqa: E501
            return data

    def create_shipping_fulfillment_with_http_info(self, body, content_type, order_id, **kwargs):  # noqa: E501
        """create_shipping_fulfillment  # noqa: E501

        When you group an order's line items into one or more packages, each package requires a corresponding plan for handling, addressing, and shipping; this is a <i>shipping fulfillment</i>. For each package, execute this call once to generate a shipping fulfillment associated with that package. <br><br> <span class=\"tablenote\"><strong>Note:</strong> A single line item in an order can consist of multiple units of a purchased item, and one unit can consist of multiple parts or components. Although these components might be provided by the manufacturer in separate packaging, the seller must include all components of a given line item in the same package.</span> <br><br>Before using this call for a given package, you must determine which line items are in the package. If the package has been shipped, you should provide the date of shipment in the request. If not provided, it will default to the current date and time.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_shipping_fulfillment_with_http_info(body, content_type, order_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param ShippingFulfillmentDetails body: fulfillment payload (required)
        :param str content_type: This header indicates the format of the request body provided by the client. Its value should be set to <b>application/json</b>. <br><br> For more information, refer to <a href=\"/api-docs/static/rest-request-components.html#HTTP\" target=\"_blank \">HTTP request headers</a>. (required)
        :param str order_id: This path parameter is used to specify the unique identifier of the order associated with the shipping fulfillment being created.<br><br> Use the <a href=\"/api-docs/sell/fulfillment/resources/order/methods/getOrders\" target=\"_blank \">getOrders</a> method to retrieve order IDs. (required)
        :return: object
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body', 'content_type', 'order_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_shipping_fulfillment" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'body' is set
        if ('body' not in params or
                params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `create_shipping_fulfillment`")  # noqa: E501
        # verify the required parameter 'content_type' is set
        if ('content_type' not in params or
                params['content_type'] is None):
            raise ValueError("Missing the required parameter `content_type` when calling `create_shipping_fulfillment`")  # noqa: E501
        # verify the required parameter 'order_id' is set
        if ('order_id' not in params or
                params['order_id'] is None):
            raise ValueError("Missing the required parameter `order_id` when calling `create_shipping_fulfillment`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'order_id' in params:
            path_params['orderId'] = params['order_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'content_type' in params:
            header_params['Content-Type'] = params['content_type']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_auth']  # noqa: E501

        return self.api_client.call_api(
            '/order/{orderId}/shipping_fulfillment', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='object',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_shipping_fulfillment(self, fulfillment_id, order_id, **kwargs):  # noqa: E501
        """get_shipping_fulfillment  # noqa: E501

        Use this call to retrieve the contents of a fulfillment based on its unique identifier, <b>fulfillmentId</b> (combined with the associated order's <b>orderId</b>). The <b>fulfillmentId</b> value was originally generated by the <b>createShippingFulfillment</b> call, and is returned by the <b>getShippingFulfillments</b> call in the <b>members.fulfillmentId</b> field.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_shipping_fulfillment(fulfillment_id, order_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fulfillment_id: This path parameter is used to specify the unique identifier of the shipping fulfillment being retrieved.<br><br>Use the <a href=\"/api-docs/sell/fulfillment/resources/order/shipping_fulfillment/methods/getShippingFulfillments\" target=\"_blank \">getShippingFulfillments</a> method to retrieved fulfillment IDs. (required)
        :param str order_id: This path parameter is used to specify the unique identifier of the order associated with the shipping fulfillment being retrieved.<br><br> Use the <a href=\"/api-docs/sell/fulfillment/resources/order/methods/getOrders\" target=\"_blank \">getOrders</a> method to retrieve order IDs. Order ID values are also shown in My eBay/Seller Hub. (required)
        :return: ShippingFulfillment
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_shipping_fulfillment_with_http_info(fulfillment_id, order_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_shipping_fulfillment_with_http_info(fulfillment_id, order_id, **kwargs)  # noqa: E501
            return data

    def get_shipping_fulfillment_with_http_info(self, fulfillment_id, order_id, **kwargs):  # noqa: E501
        """get_shipping_fulfillment  # noqa: E501

        Use this call to retrieve the contents of a fulfillment based on its unique identifier, <b>fulfillmentId</b> (combined with the associated order's <b>orderId</b>). The <b>fulfillmentId</b> value was originally generated by the <b>createShippingFulfillment</b> call, and is returned by the <b>getShippingFulfillments</b> call in the <b>members.fulfillmentId</b> field.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_shipping_fulfillment_with_http_info(fulfillment_id, order_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str fulfillment_id: This path parameter is used to specify the unique identifier of the shipping fulfillment being retrieved.<br><br>Use the <a href=\"/api-docs/sell/fulfillment/resources/order/shipping_fulfillment/methods/getShippingFulfillments\" target=\"_blank \">getShippingFulfillments</a> method to retrieved fulfillment IDs. (required)
        :param str order_id: This path parameter is used to specify the unique identifier of the order associated with the shipping fulfillment being retrieved.<br><br> Use the <a href=\"/api-docs/sell/fulfillment/resources/order/methods/getOrders\" target=\"_blank \">getOrders</a> method to retrieve order IDs. Order ID values are also shown in My eBay/Seller Hub. (required)
        :return: ShippingFulfillment
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['fulfillment_id', 'order_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_shipping_fulfillment" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'fulfillment_id' is set
        if ('fulfillment_id' not in params or
                params['fulfillment_id'] is None):
            raise ValueError("Missing the required parameter `fulfillment_id` when calling `get_shipping_fulfillment`")  # noqa: E501
        # verify the required parameter 'order_id' is set
        if ('order_id' not in params or
                params['order_id'] is None):
            raise ValueError("Missing the required parameter `order_id` when calling `get_shipping_fulfillment`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'fulfillment_id' in params:
            path_params['fulfillmentId'] = params['fulfillment_id']  # noqa: E501
        if 'order_id' in params:
            path_params['orderId'] = params['order_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_auth']  # noqa: E501

        return self.api_client.call_api(
            '/order/{orderId}/shipping_fulfillment/{fulfillmentId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShippingFulfillment',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_shipping_fulfillments(self, order_id, **kwargs):  # noqa: E501
        """get_shipping_fulfillments  # noqa: E501

        Use this call to retrieve the contents of all fulfillments currently defined for a specified order based on the order's unique identifier, <b>orderId</b>. This value is returned in the <b>getOrders</b> call's <b>members.orderId</b> field when you search for orders by creation date or shipment status.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_shipping_fulfillments(order_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str order_id: This path parameter is used to specify the unique identifier of the order associated with the shipping fulfillments being retrieved.<br><br>Use the <a href=\"/api-docs/sell/fulfillment/resources/order/methods/getOrders\" target=\"_blank \">getOrders</a> method to retrieve order IDs. Order ID values are also shown in My eBay/Seller Hub. (required)
        :return: ShippingFulfillmentPagedCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_shipping_fulfillments_with_http_info(order_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_shipping_fulfillments_with_http_info(order_id, **kwargs)  # noqa: E501
            return data

    def get_shipping_fulfillments_with_http_info(self, order_id, **kwargs):  # noqa: E501
        """get_shipping_fulfillments  # noqa: E501

        Use this call to retrieve the contents of all fulfillments currently defined for a specified order based on the order's unique identifier, <b>orderId</b>. This value is returned in the <b>getOrders</b> call's <b>members.orderId</b> field when you search for orders by creation date or shipment status.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_shipping_fulfillments_with_http_info(order_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str order_id: This path parameter is used to specify the unique identifier of the order associated with the shipping fulfillments being retrieved.<br><br>Use the <a href=\"/api-docs/sell/fulfillment/resources/order/methods/getOrders\" target=\"_blank \">getOrders</a> method to retrieve order IDs. Order ID values are also shown in My eBay/Seller Hub. (required)
        :return: ShippingFulfillmentPagedCollection
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['order_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_shipping_fulfillments" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'order_id' is set
        if ('order_id' not in params or
                params['order_id'] is None):
            raise ValueError("Missing the required parameter `order_id` when calling `get_shipping_fulfillments`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'order_id' in params:
            path_params['orderId'] = params['order_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_auth']  # noqa: E501

        return self.api_client.call_api(
            '/order/{orderId}/shipping_fulfillment', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ShippingFulfillmentPagedCollection',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
