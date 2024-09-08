# coding: utf-8

"""
    Buy Feed API

    The Feed API provides the ability to download TSV_GZIP feed files containing eBay items and an hourly snapshot file for a specific category, date, and marketplace.<br /><br />In addition to the API, there is an open-source Feed SDK written in Java that downloads, combines files into a single file when needed, and unzips the entire feed file. It also lets you specify field filters to curate the items in the file.  # noqa: E501

    OpenAPI spec version: v1.1.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from ...buy_feed.api_client import ApiClient


class FileApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def download_file(self, file_id, x_ebay_c_marketplace_id, **kwargs):  # noqa: E501
        """download_file  # noqa: E501

        <p>Use the <b>downloadFile</b> method to download a selected TSV_gzip feed file.<br><br><span class=\"tablenote\"><b>Note:</b>The downloaded file will be gzipped automatically, so there is no reason to supply <b>Accept-Encoding:gzip</b> as a header. If this header is supplied, the downloaded file will be compressed twice, and this has no extra benefit.<p>Use the <b>getFiles</b> methods to obtain the <b>file_id</b> of the specific feed file you require.</p> <h3><b>Downloading feed files </b></h3>  <p>The feed files are binary gzip files. If the file is larger than 200 MB, the download must be streamed in chunks. You specify the size of the chunks in bytes using the <a href=\"#s0-1-22-6-7-7-2-9-parameter-name-Range-1\">Range</a> request header. The <a href=\"#content-range\">content-range</a> response header indicates where in the full resource this partial chunk of data belongs and the total number of bytes in the file. For more information about using these headers, see <a href=\"/api-docs/buy/static/api-feed.html#retrieve-gzip\" target=\"_blank\">Retrieving a GZIP feed file</a>.</p><p>In addition to the API, there is an open source <a href=\"https://github.com/eBay/ebay-feedv1-dotnet-sdk\" target=\"_blank\">Feed V1 SDK</a> written in .NET that downloads, combines files into a single file when needed, and unzips the entire feed file. It also lets you specify field filters to curate the items in the file.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.download_file(file_id, x_ebay_c_marketplace_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str file_id: This path parameter specifies the unique identifier of the feed file that you wish to download.<br><br>Use the <a href=\"/api-docs/buy/feed/v1/resources/file/methods/getFiles\" target=\"_blank\">getFiles</a> method to obtain the <b>file_id</b> value for the desired feed file. (required)
        :param str x_ebay_c_marketplace_id: Indicates the unique identifier of the eBay marketplace that the feed file belongs to. <br /><br /><b>Example:</b> <code>X-EBAY-C-MARKETPLACE-ID: EBAY_US</code>.<br /><br />See <a href=\"/api-docs/buy/feed/v1/types/bas:MarketplaceIdEnum\">MarketplaceIdEnum</a> for supported values. (required)
        :param str range: Indicates where in the full resource this partial chunk of data belongs and the total number of bytes in the file.<br /><br /><b>Example:</b> <code>bytes=0-102400</code>.<br /><br />For more information about using this header, see <a href=\"/api-docs/buy/static/api-feed.html#retrieve-gzip\" target=\"_blank\">Retrieving a GZIP feed file</a>.
        :return: OutputStream
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.download_file_with_http_info(file_id, x_ebay_c_marketplace_id, **kwargs)  # noqa: E501
        else:
            (data) = self.download_file_with_http_info(file_id, x_ebay_c_marketplace_id, **kwargs)  # noqa: E501
            return data

    def download_file_with_http_info(self, file_id, x_ebay_c_marketplace_id, **kwargs):  # noqa: E501
        """download_file  # noqa: E501

        <p>Use the <b>downloadFile</b> method to download a selected TSV_gzip feed file.<br><br><span class=\"tablenote\"><b>Note:</b>The downloaded file will be gzipped automatically, so there is no reason to supply <b>Accept-Encoding:gzip</b> as a header. If this header is supplied, the downloaded file will be compressed twice, and this has no extra benefit.<p>Use the <b>getFiles</b> methods to obtain the <b>file_id</b> of the specific feed file you require.</p> <h3><b>Downloading feed files </b></h3>  <p>The feed files are binary gzip files. If the file is larger than 200 MB, the download must be streamed in chunks. You specify the size of the chunks in bytes using the <a href=\"#s0-1-22-6-7-7-2-9-parameter-name-Range-1\">Range</a> request header. The <a href=\"#content-range\">content-range</a> response header indicates where in the full resource this partial chunk of data belongs and the total number of bytes in the file. For more information about using these headers, see <a href=\"/api-docs/buy/static/api-feed.html#retrieve-gzip\" target=\"_blank\">Retrieving a GZIP feed file</a>.</p><p>In addition to the API, there is an open source <a href=\"https://github.com/eBay/ebay-feedv1-dotnet-sdk\" target=\"_blank\">Feed V1 SDK</a> written in .NET that downloads, combines files into a single file when needed, and unzips the entire feed file. It also lets you specify field filters to curate the items in the file.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.download_file_with_http_info(file_id, x_ebay_c_marketplace_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str file_id: This path parameter specifies the unique identifier of the feed file that you wish to download.<br><br>Use the <a href=\"/api-docs/buy/feed/v1/resources/file/methods/getFiles\" target=\"_blank\">getFiles</a> method to obtain the <b>file_id</b> value for the desired feed file. (required)
        :param str x_ebay_c_marketplace_id: Indicates the unique identifier of the eBay marketplace that the feed file belongs to. <br /><br /><b>Example:</b> <code>X-EBAY-C-MARKETPLACE-ID: EBAY_US</code>.<br /><br />See <a href=\"/api-docs/buy/feed/v1/types/bas:MarketplaceIdEnum\">MarketplaceIdEnum</a> for supported values. (required)
        :param str range: Indicates where in the full resource this partial chunk of data belongs and the total number of bytes in the file.<br /><br /><b>Example:</b> <code>bytes=0-102400</code>.<br /><br />For more information about using this header, see <a href=\"/api-docs/buy/static/api-feed.html#retrieve-gzip\" target=\"_blank\">Retrieving a GZIP feed file</a>.
        :return: OutputStream
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['file_id', 'x_ebay_c_marketplace_id', 'range']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method download_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'file_id' is set
        if ('file_id' not in params or
                params['file_id'] is None):
            raise ValueError("Missing the required parameter `file_id` when calling `download_file`")  # noqa: E501
        # verify the required parameter 'x_ebay_c_marketplace_id' is set
        if ('x_ebay_c_marketplace_id' not in params or
                params['x_ebay_c_marketplace_id'] is None):
            raise ValueError("Missing the required parameter `x_ebay_c_marketplace_id` when calling `download_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_id' in params:
            path_params['file_id'] = params['file_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'range' in params:
            header_params['Range'] = params['range']  # noqa: E501
        if 'x_ebay_c_marketplace_id' in params:
            header_params['X-EBAY-C-MARKETPLACE-ID'] = params['x_ebay_c_marketplace_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/octet-stream'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_auth']  # noqa: E501

        return self.api_client.call_api(
            '/file/{file_id}/download', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='OutputStream',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_file(self, file_id, x_ebay_c_marketplace_id, **kwargs):  # noqa: E501
        """get_file  # noqa: E501

        Use the <b>getFile</b> method to fetch the details of a feed file available to download, as specified by the file's <b>file_id</b>.</p><p>Details in the response include: the feed's <b>file_id</b>, the date it became available, eBay categories that support the feed, its frequency, the time span it covers, its feed type, its format (currently only TSV is available), its size in bytes, the schema under which it was pulled, and the marketplaces it applies to.</p>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file(file_id, x_ebay_c_marketplace_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str file_id: This path parameter specifies the unique identifier of the feed file that you wish to retrieve.<br><br>Use the <a href=\"/api-docs/buy/feed/v1/resources/file/methods/getFiles\" target=\"_blank\">getFiles</a> method to obtain the <b>fileId</b> value for the desired feed file. (required)
        :param str x_ebay_c_marketplace_id: Indicates the unique identifier of the eBay marketplace on which the feed file exists. <br /><br /><b>Example:</b> <code>X-EBAY-C-MARKETPLACE-ID: EBAY_US</code>.<br /><br />See <a href=\"/api-docs/buy/feed/v1/types/bas:MarketplaceIdEnum\">MarketplaceIdEnum</a> for supported values. (required)
        :return: FileMetadata
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_file_with_http_info(file_id, x_ebay_c_marketplace_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_file_with_http_info(file_id, x_ebay_c_marketplace_id, **kwargs)  # noqa: E501
            return data

    def get_file_with_http_info(self, file_id, x_ebay_c_marketplace_id, **kwargs):  # noqa: E501
        """get_file  # noqa: E501

        Use the <b>getFile</b> method to fetch the details of a feed file available to download, as specified by the file's <b>file_id</b>.</p><p>Details in the response include: the feed's <b>file_id</b>, the date it became available, eBay categories that support the feed, its frequency, the time span it covers, its feed type, its format (currently only TSV is available), its size in bytes, the schema under which it was pulled, and the marketplaces it applies to.</p>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_file_with_http_info(file_id, x_ebay_c_marketplace_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str file_id: This path parameter specifies the unique identifier of the feed file that you wish to retrieve.<br><br>Use the <a href=\"/api-docs/buy/feed/v1/resources/file/methods/getFiles\" target=\"_blank\">getFiles</a> method to obtain the <b>fileId</b> value for the desired feed file. (required)
        :param str x_ebay_c_marketplace_id: Indicates the unique identifier of the eBay marketplace on which the feed file exists. <br /><br /><b>Example:</b> <code>X-EBAY-C-MARKETPLACE-ID: EBAY_US</code>.<br /><br />See <a href=\"/api-docs/buy/feed/v1/types/bas:MarketplaceIdEnum\">MarketplaceIdEnum</a> for supported values. (required)
        :return: FileMetadata
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['file_id', 'x_ebay_c_marketplace_id']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_file" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'file_id' is set
        if ('file_id' not in params or
                params['file_id'] is None):
            raise ValueError("Missing the required parameter `file_id` when calling `get_file`")  # noqa: E501
        # verify the required parameter 'x_ebay_c_marketplace_id' is set
        if ('x_ebay_c_marketplace_id' not in params or
                params['x_ebay_c_marketplace_id'] is None):
            raise ValueError("Missing the required parameter `x_ebay_c_marketplace_id` when calling `get_file`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'file_id' in params:
            path_params['file_id'] = params['file_id']  # noqa: E501

        query_params = []

        header_params = {}
        if 'x_ebay_c_marketplace_id' in params:
            header_params['X-EBAY-C-MARKETPLACE-ID'] = params['x_ebay_c_marketplace_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_auth']  # noqa: E501

        return self.api_client.call_api(
            '/file/{file_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileMetadata',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_files(self, feed_type_id, x_ebay_c_marketplace_id, **kwargs):  # noqa: E501
        """get_files  # noqa: E501

        <p>The <b>getFiles</b> method provides a list of the feed files available for download.</p><p>Details for each feed returned include the date the feed was generated, the frequency with which it is pulled, its feed type, its <b>fileId</b>, its format (currently only TSV is supported), the eBay marketplaces it applies to, the schema version under which it was generated, its size in bytes, and the time span it covers (in hours).</p><p>You can limit your search results by feed type, marketplace, scope, eBay L1 category, and how far back in time from the present the feed was made available. Set the <a href=\"/api-docs/buy/feed/v1/resources/file/methods/getFiles#uri.look_back\">look_back</a> field to control exactly how many feeds from the past are retrieved.</p><h3><b>Restrictions </b></h3><p>For a list of supported sites and other restrictions, see <a href=\"/api-docs/buy/feed/overview.html#API\">API Restrictions</a>.</p>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_files(feed_type_id, x_ebay_c_marketplace_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str feed_type_id: This query parameter specifies the unique identifier for the feed type to be used as a search filter.<br /><br />Use the <a href=\"/api-docs/buy/feed/v1/resources/feed_type/methods/getFeedTypes\" target=\"_blank\">getFeedTypes</a> method to identify available feed types.<br /><br /><span class=\"tablenote\"><span style=\"color:#004680\"><strong>Note:</strong></span> Refer to <a href=\"/api-docs/buy/feed/v1/static/overview.html#feed-types\" target=\"_blank\">Supported feed types</a> to learn more about the feed types supported by the Feed API.</span> (required)
        :param str x_ebay_c_marketplace_id: Indicates the unique identifier of the eBay marketplace on which to search for feed files. <br /><br /><b>Example:</b> <code>X-EBAY-C-MARKETPLACE-ID: EBAY_US</code>.<br /><br />See <a href=\"/api-docs/buy/feed/v1/types/bas:MarketplaceIdEnum\">MarketplaceIdEnum</a> for supported values. (required)
        :param str category_ids: This query parameter is used to specify one or more eBay L1 category IDs.<br><br>If this filter is used, only feed files that are supported for the specified category (or categories) will be returned in the response. Each category ID value must be delimited by a comma.<br><br>For details, see <a href=\"/api-docs/buy/buy-categories.html\" target=\"_blank\">Get Categories for Buy APIs.</a><br /><br /><b>Max:</b> 20 values
        :param str continuation_token: The server returns this token to the web client when the responses received require multiple pages to display. The web client sends this token back to the server to get the next page of results.
        :param str feed_scope: This query parameter specifies the frequency with which the feed file is made available (<code>HOURLY</code>, <code>DAILY</code>, <code>WEEKLY</code>).<br><br><span class=\"tablenote\"><b>Note:</b> Currently only <code>DAILY</code> and <code>HOURLY</code> are supported.</span>
        :param str limit: Indicates the number of records to show in the response.<br /><br /><b>Default:</b> 20<br /><br /><b>Minimum:</b> 20<br /><br /><b>Maximum:</b> 100
        :param str look_back: This filter controls how far back from the current time to limit the returned feed files and is specified in minutes. The returned feed files will be those generated between the current time and the look-back time.<br /><br /><b>Example:</b> A value of <code>120</code> will limit the returned feed files to those generated in the past 2 hours (120 minutes). If 3 feed files have been generated in the past 2 hours, those 3 files will be returned. A feed file generated 4 hours earlier will not be returned.<br><br><div class=\"msgbox_important\"><p class=\"msgbox_importantInDiv\" data-mc-autonum=\"&lt;b&gt;&lt;span style=&quot;color: #dd1e31;&quot; class=&quot;mcFormatColor&quot;&gt;Important! &lt;/span&gt;&lt;/b&gt;\"><span class=\"autonumber\"><span><b><span style=\"color: #dd1e31;\" class=\"mcFormatColor\">Important!</span></b></span></span> Unless the <b>look_back</b> filter is used, available files generated approximately within the last 48 hours are returned in the response. The <b>look_back</b> filter can be used to increase or decrease this time frame. The maximum (minutes) value set for this parameter should not exceed the <b>lookBack</b> threshold for the feed type returned in <a href=\"/api-docs/buy/feed/v1/resources/feed_type/methods/getFeedType\">getFeedType</a>/<a href=\"/api-docs/buy/feed/v1/resources/feed_type/methods/getFeedTypes\">getFeedTypes</a>.</p></div>
        :return: FileMetadataSearchResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.get_files_with_http_info(feed_type_id, x_ebay_c_marketplace_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_files_with_http_info(feed_type_id, x_ebay_c_marketplace_id, **kwargs)  # noqa: E501
            return data

    def get_files_with_http_info(self, feed_type_id, x_ebay_c_marketplace_id, **kwargs):  # noqa: E501
        """get_files  # noqa: E501

        <p>The <b>getFiles</b> method provides a list of the feed files available for download.</p><p>Details for each feed returned include the date the feed was generated, the frequency with which it is pulled, its feed type, its <b>fileId</b>, its format (currently only TSV is supported), the eBay marketplaces it applies to, the schema version under which it was generated, its size in bytes, and the time span it covers (in hours).</p><p>You can limit your search results by feed type, marketplace, scope, eBay L1 category, and how far back in time from the present the feed was made available. Set the <a href=\"/api-docs/buy/feed/v1/resources/file/methods/getFiles#uri.look_back\">look_back</a> field to control exactly how many feeds from the past are retrieved.</p><h3><b>Restrictions </b></h3><p>For a list of supported sites and other restrictions, see <a href=\"/api-docs/buy/feed/overview.html#API\">API Restrictions</a>.</p>  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_files_with_http_info(feed_type_id, x_ebay_c_marketplace_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str feed_type_id: This query parameter specifies the unique identifier for the feed type to be used as a search filter.<br /><br />Use the <a href=\"/api-docs/buy/feed/v1/resources/feed_type/methods/getFeedTypes\" target=\"_blank\">getFeedTypes</a> method to identify available feed types.<br /><br /><span class=\"tablenote\"><span style=\"color:#004680\"><strong>Note:</strong></span> Refer to <a href=\"/api-docs/buy/feed/v1/static/overview.html#feed-types\" target=\"_blank\">Supported feed types</a> to learn more about the feed types supported by the Feed API.</span> (required)
        :param str x_ebay_c_marketplace_id: Indicates the unique identifier of the eBay marketplace on which to search for feed files. <br /><br /><b>Example:</b> <code>X-EBAY-C-MARKETPLACE-ID: EBAY_US</code>.<br /><br />See <a href=\"/api-docs/buy/feed/v1/types/bas:MarketplaceIdEnum\">MarketplaceIdEnum</a> for supported values. (required)
        :param str category_ids: This query parameter is used to specify one or more eBay L1 category IDs.<br><br>If this filter is used, only feed files that are supported for the specified category (or categories) will be returned in the response. Each category ID value must be delimited by a comma.<br><br>For details, see <a href=\"/api-docs/buy/buy-categories.html\" target=\"_blank\">Get Categories for Buy APIs.</a><br /><br /><b>Max:</b> 20 values
        :param str continuation_token: The server returns this token to the web client when the responses received require multiple pages to display. The web client sends this token back to the server to get the next page of results.
        :param str feed_scope: This query parameter specifies the frequency with which the feed file is made available (<code>HOURLY</code>, <code>DAILY</code>, <code>WEEKLY</code>).<br><br><span class=\"tablenote\"><b>Note:</b> Currently only <code>DAILY</code> and <code>HOURLY</code> are supported.</span>
        :param str limit: Indicates the number of records to show in the response.<br /><br /><b>Default:</b> 20<br /><br /><b>Minimum:</b> 20<br /><br /><b>Maximum:</b> 100
        :param str look_back: This filter controls how far back from the current time to limit the returned feed files and is specified in minutes. The returned feed files will be those generated between the current time and the look-back time.<br /><br /><b>Example:</b> A value of <code>120</code> will limit the returned feed files to those generated in the past 2 hours (120 minutes). If 3 feed files have been generated in the past 2 hours, those 3 files will be returned. A feed file generated 4 hours earlier will not be returned.<br><br><div class=\"msgbox_important\"><p class=\"msgbox_importantInDiv\" data-mc-autonum=\"&lt;b&gt;&lt;span style=&quot;color: #dd1e31;&quot; class=&quot;mcFormatColor&quot;&gt;Important! &lt;/span&gt;&lt;/b&gt;\"><span class=\"autonumber\"><span><b><span style=\"color: #dd1e31;\" class=\"mcFormatColor\">Important!</span></b></span></span> Unless the <b>look_back</b> filter is used, available files generated approximately within the last 48 hours are returned in the response. The <b>look_back</b> filter can be used to increase or decrease this time frame. The maximum (minutes) value set for this parameter should not exceed the <b>lookBack</b> threshold for the feed type returned in <a href=\"/api-docs/buy/feed/v1/resources/feed_type/methods/getFeedType\">getFeedType</a>/<a href=\"/api-docs/buy/feed/v1/resources/feed_type/methods/getFeedTypes\">getFeedTypes</a>.</p></div>
        :return: FileMetadataSearchResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['feed_type_id', 'x_ebay_c_marketplace_id', 'category_ids', 'continuation_token', 'feed_scope', 'limit', 'look_back']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_files" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'feed_type_id' is set
        if ('feed_type_id' not in params or
                params['feed_type_id'] is None):
            raise ValueError("Missing the required parameter `feed_type_id` when calling `get_files`")  # noqa: E501
        # verify the required parameter 'x_ebay_c_marketplace_id' is set
        if ('x_ebay_c_marketplace_id' not in params or
                params['x_ebay_c_marketplace_id'] is None):
            raise ValueError("Missing the required parameter `x_ebay_c_marketplace_id` when calling `get_files`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'category_ids' in params:
            query_params.append(('category_ids', params['category_ids']))  # noqa: E501
        if 'continuation_token' in params:
            query_params.append(('continuation_token', params['continuation_token']))  # noqa: E501
        if 'feed_scope' in params:
            query_params.append(('feed_scope', params['feed_scope']))  # noqa: E501
        if 'feed_type_id' in params:
            query_params.append(('feed_type_id', params['feed_type_id']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'look_back' in params:
            query_params.append(('look_back', params['look_back']))  # noqa: E501

        header_params = {}
        if 'x_ebay_c_marketplace_id' in params:
            header_params['X-EBAY-C-MARKETPLACE-ID'] = params['x_ebay_c_marketplace_id']  # noqa: E501

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_auth']  # noqa: E501

        return self.api_client.call_api(
            '/file', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='FileMetadataSearchResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
