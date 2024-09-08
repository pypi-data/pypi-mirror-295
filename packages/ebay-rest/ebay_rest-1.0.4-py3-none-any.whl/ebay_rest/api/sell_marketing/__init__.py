# coding: utf-8

# flake8: noqa

"""
    Marketing API

    <p>The <i>Marketing API </i> offers two platforms that sellers can use to promote and advertise their products:</p> <ul><li><b>Promoted Listings</b> is an eBay ad service that lets sellers set up <i>ad campaigns </i> for the products they want to promote. eBay displays the ads in search results and in other marketing modules as <b>SPONSORED</b> listings. If an item in a Promoted Listings campaign sells, the seller is assessed a Promoted Listings fee, which is a seller-specified percentage applied to the sales price. For complete details, refer to the <a href=\"/api-docs/sell/static/marketing/pl-landing.html\">Promoted Listings playbook</a>.</li><li><b>Promotions Manager</b> gives sellers a way to offer discounts on specific items as a way to attract buyers to their inventory. Sellers can set up discounts (such as \"20% off\" and other types of offers) on specific items or on an entire customer order. To further attract buyers, eBay prominently displays promotion <i>teasers</i> throughout buyer flows. For complete details, see <a href=\"/api-docs/sell/static/marketing/promotions-manager.html\">Promotions Manager</a>.</li></ul>  <p><b>Marketing reports</b>, on both the Promoted Listings and Promotions Manager platforms, give sellers information that shows the effectiveness of their marketing strategies. The data gives sellers the ability to review and fine tune their marketing efforts.</p><p><b>Store Email Campaign</b> allows sellers to create and send email campaigns to customers who have signed up to receive their newsletter. For more information on email campaigns, see <a href=\"/api-docs/sell/static/marketing/store-email-campaigns.html#email-campain-types\" target=\"_blank\">Store Email Campaigns</a>.<p class=\"tablenote\"><b>Important!</b> Sellers must have an active eBay Store subscription, and they must accept the <b>Terms and Conditions</b> before they can make requests to these APIs in the Production environment. There are also site-specific listings requirements and restrictions associated with these marketing tools, as listed in the \"requirements and restrictions\" sections for <a href=\"/api-docs/sell/marketing/static/overview.html#PL-requirements\">Promoted Listings</a> and <a href=\"/api-docs/sell/marketing/static/overview.html#PM-requirements\">Promotions Manager</a>.</p> <p>The table below lists all the Marketing API calls grouped by resource.</p>  # noqa: E501

    OpenAPI spec version: v1.22.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import apis into sdk package
from ..sell_marketing.api.ad_api import AdApi
from ..sell_marketing.api.ad_group_api import AdGroupApi
from ..sell_marketing.api.ad_report_api import AdReportApi
from ..sell_marketing.api.ad_report_metadata_api import AdReportMetadataApi
from ..sell_marketing.api.ad_report_task_api import AdReportTaskApi
from ..sell_marketing.api.campaign_api import CampaignApi
from ..sell_marketing.api.email_campaign_api import EmailCampaignApi
from ..sell_marketing.api.item_price_markdown_api import ItemPriceMarkdownApi
from ..sell_marketing.api.item_promotion_api import ItemPromotionApi
from ..sell_marketing.api.keyword_api import KeywordApi
from ..sell_marketing.api.negative_keyword_api import NegativeKeywordApi
from ..sell_marketing.api.promotion_api import PromotionApi
from ..sell_marketing.api.promotion_report_api import PromotionReportApi
from ..sell_marketing.api.promotion_summary_report_api import PromotionSummaryReportApi
# import ApiClient
from ..sell_marketing.api_client import ApiClient
from ..sell_marketing.configuration import Configuration
# import models into sdk package
from ..sell_marketing.models.ad import Ad
from ..sell_marketing.models.ad_group import AdGroup
from ..sell_marketing.models.ad_group_paged_collection_response import AdGroupPagedCollectionResponse
from ..sell_marketing.models.ad_ids import AdIds
from ..sell_marketing.models.ad_paged_collection_response import AdPagedCollectionResponse
from ..sell_marketing.models.ad_reference import AdReference
from ..sell_marketing.models.ad_references import AdReferences
from ..sell_marketing.models.ad_response import AdResponse
from ..sell_marketing.models.ad_update_response import AdUpdateResponse
from ..sell_marketing.models.ad_update_status_by_listing_id_response import AdUpdateStatusByListingIdResponse
from ..sell_marketing.models.ad_update_status_response import AdUpdateStatusResponse
from ..sell_marketing.models.additional_info import AdditionalInfo
from ..sell_marketing.models.additional_info_data import AdditionalInfoData
from ..sell_marketing.models.ads import Ads
from ..sell_marketing.models.alert import Alert
from ..sell_marketing.models.alert_details import AlertDetails
from ..sell_marketing.models.alert_dimension import AlertDimension
from ..sell_marketing.models.amount import Amount
from ..sell_marketing.models.aspect import Aspect
from ..sell_marketing.models.base_response import BaseResponse
from ..sell_marketing.models.bid_preference import BidPreference
from ..sell_marketing.models.budget import Budget
from ..sell_marketing.models.budget_recommendation_response import BudgetRecommendationResponse
from ..sell_marketing.models.budget_request import BudgetRequest
from ..sell_marketing.models.bulk_ad_response import BulkAdResponse
from ..sell_marketing.models.bulk_ad_update_response import BulkAdUpdateResponse
from ..sell_marketing.models.bulk_ad_update_status_by_listing_id_response import BulkAdUpdateStatusByListingIdResponse
from ..sell_marketing.models.bulk_ad_update_status_response import BulkAdUpdateStatusResponse
from ..sell_marketing.models.bulk_create_ad_request import BulkCreateAdRequest
from ..sell_marketing.models.bulk_create_ads_by_inventory_reference_request import BulkCreateAdsByInventoryReferenceRequest
from ..sell_marketing.models.bulk_create_ads_by_inventory_reference_response import BulkCreateAdsByInventoryReferenceResponse
from ..sell_marketing.models.bulk_create_keyword_request import BulkCreateKeywordRequest
from ..sell_marketing.models.bulk_create_keyword_response import BulkCreateKeywordResponse
from ..sell_marketing.models.bulk_create_negative_keyword_request import BulkCreateNegativeKeywordRequest
from ..sell_marketing.models.bulk_create_negative_keyword_response import BulkCreateNegativeKeywordResponse
from ..sell_marketing.models.bulk_delete_ad_request import BulkDeleteAdRequest
from ..sell_marketing.models.bulk_delete_ad_response import BulkDeleteAdResponse
from ..sell_marketing.models.bulk_delete_ads_by_inventory_reference_request import BulkDeleteAdsByInventoryReferenceRequest
from ..sell_marketing.models.bulk_delete_ads_by_inventory_reference_response import BulkDeleteAdsByInventoryReferenceResponse
from ..sell_marketing.models.bulk_update_ad_status_by_listing_id_request import BulkUpdateAdStatusByListingIdRequest
from ..sell_marketing.models.bulk_update_ad_status_request import BulkUpdateAdStatusRequest
from ..sell_marketing.models.bulk_update_ads_by_inventory_reference_response import BulkUpdateAdsByInventoryReferenceResponse
from ..sell_marketing.models.bulk_update_keyword_request import BulkUpdateKeywordRequest
from ..sell_marketing.models.bulk_update_keyword_response import BulkUpdateKeywordResponse
from ..sell_marketing.models.bulk_update_negative_keyword_request import BulkUpdateNegativeKeywordRequest
from ..sell_marketing.models.bulk_update_negative_keyword_response import BulkUpdateNegativeKeywordResponse
from ..sell_marketing.models.campaign import Campaign
from ..sell_marketing.models.campaign_audience import CampaignAudience
from ..sell_marketing.models.campaign_budget import CampaignBudget
from ..sell_marketing.models.campaign_budget_request import CampaignBudgetRequest
from ..sell_marketing.models.campaign_criterion import CampaignCriterion
from ..sell_marketing.models.campaign_dto import CampaignDTO
from ..sell_marketing.models.campaign_paged_collection_response import CampaignPagedCollectionResponse
from ..sell_marketing.models.campaigns import Campaigns
from ..sell_marketing.models.clone_campaign_request import CloneCampaignRequest
from ..sell_marketing.models.coupon_configuration import CouponConfiguration
from ..sell_marketing.models.create_ad_group_request import CreateAdGroupRequest
from ..sell_marketing.models.create_ad_request import CreateAdRequest
from ..sell_marketing.models.create_ads_by_inventory_reference_request import CreateAdsByInventoryReferenceRequest
from ..sell_marketing.models.create_ads_by_inventory_reference_response import CreateAdsByInventoryReferenceResponse
from ..sell_marketing.models.create_campaign_request import CreateCampaignRequest
from ..sell_marketing.models.create_email_campaign_request import CreateEmailCampaignRequest
from ..sell_marketing.models.create_email_campaign_response import CreateEmailCampaignResponse
from ..sell_marketing.models.create_keyword_request import CreateKeywordRequest
from ..sell_marketing.models.create_negative_keyword_request import CreateNegativeKeywordRequest
from ..sell_marketing.models.create_report_task import CreateReportTask
from ..sell_marketing.models.delete_ad_request import DeleteAdRequest
from ..sell_marketing.models.delete_ad_response import DeleteAdResponse
from ..sell_marketing.models.delete_ads_by_inventory_reference_request import DeleteAdsByInventoryReferenceRequest
from ..sell_marketing.models.delete_ads_by_inventory_reference_response import DeleteAdsByInventoryReferenceResponse
from ..sell_marketing.models.delete_email_campaign_response import DeleteEmailCampaignResponse
from ..sell_marketing.models.dimension import Dimension
from ..sell_marketing.models.dimension_key_annotation import DimensionKeyAnnotation
from ..sell_marketing.models.dimension_metadata import DimensionMetadata
from ..sell_marketing.models.discount_benefit import DiscountBenefit
from ..sell_marketing.models.discount_rule import DiscountRule
from ..sell_marketing.models.discount_specification import DiscountSpecification
from ..sell_marketing.models.dynamic_ad_rate_preference import DynamicAdRatePreference
from ..sell_marketing.models.error import Error
from ..sell_marketing.models.error_parameter import ErrorParameter
from ..sell_marketing.models.funding_strategy import FundingStrategy
from ..sell_marketing.models.get_email_campaign_audiences_response import GetEmailCampaignAudiencesResponse
from ..sell_marketing.models.get_email_campaign_response import GetEmailCampaignResponse
from ..sell_marketing.models.get_email_campaigns_response import GetEmailCampaignsResponse
from ..sell_marketing.models.get_email_preview_response import GetEmailPreviewResponse
from ..sell_marketing.models.get_email_report_response import GetEmailReportResponse
from ..sell_marketing.models.inventory_criterion import InventoryCriterion
from ..sell_marketing.models.inventory_item import InventoryItem
from ..sell_marketing.models.inventory_reference import InventoryReference
from ..sell_marketing.models.item_basis import ItemBasis
from ..sell_marketing.models.item_markdown_status import ItemMarkdownStatus
from ..sell_marketing.models.item_price_markdown import ItemPriceMarkdown
from ..sell_marketing.models.item_promotion import ItemPromotion
from ..sell_marketing.models.item_promotion_response import ItemPromotionResponse
from ..sell_marketing.models.items_paged_collection import ItemsPagedCollection
from ..sell_marketing.models.keyword import Keyword
from ..sell_marketing.models.keyword_paged_collection_response import KeywordPagedCollectionResponse
from ..sell_marketing.models.keyword_request import KeywordRequest
from ..sell_marketing.models.keyword_response import KeywordResponse
from ..sell_marketing.models.listing_detail import ListingDetail
from ..sell_marketing.models.max_cpc import MaxCpc
from ..sell_marketing.models.metric_metadata import MetricMetadata
from ..sell_marketing.models.negative_keyword import NegativeKeyword
from ..sell_marketing.models.negative_keyword_paged_collection_response import NegativeKeywordPagedCollectionResponse
from ..sell_marketing.models.negative_keyword_response import NegativeKeywordResponse
from ..sell_marketing.models.price_range import PriceRange
from ..sell_marketing.models.promotion_detail import PromotionDetail
from ..sell_marketing.models.promotion_report_detail import PromotionReportDetail
from ..sell_marketing.models.promotions_paged_collection import PromotionsPagedCollection
from ..sell_marketing.models.promotions_report_paged_collection import PromotionsReportPagedCollection
from ..sell_marketing.models.proposed_bid import ProposedBid
from ..sell_marketing.models.quick_setup_request import QuickSetupRequest
from ..sell_marketing.models.report_metadata import ReportMetadata
from ..sell_marketing.models.report_metadatas import ReportMetadatas
from ..sell_marketing.models.report_task import ReportTask
from ..sell_marketing.models.report_task_paged_collection import ReportTaskPagedCollection
from ..sell_marketing.models.rule_criteria import RuleCriteria
from ..sell_marketing.models.selected_inventory_discount import SelectedInventoryDiscount
from ..sell_marketing.models.selection_rule import SelectionRule
from ..sell_marketing.models.suggest_budget_response import SuggestBudgetResponse
from ..sell_marketing.models.suggest_max_cpc_request import SuggestMaxCpcRequest
from ..sell_marketing.models.suggest_max_cpc_response import SuggestMaxCpcResponse
from ..sell_marketing.models.suggested_bids import SuggestedBids
from ..sell_marketing.models.suggested_keywords import SuggestedKeywords
from ..sell_marketing.models.summary_report_response import SummaryReportResponse
from ..sell_marketing.models.targeted_ads_paged_collection import TargetedAdsPagedCollection
from ..sell_marketing.models.targeted_bid_request import TargetedBidRequest
from ..sell_marketing.models.targeted_bids_paged_collection import TargetedBidsPagedCollection
from ..sell_marketing.models.targeted_keyword_request import TargetedKeywordRequest
from ..sell_marketing.models.targeted_keywords_paged_collection import TargetedKeywordsPagedCollection
from ..sell_marketing.models.targeting_items import TargetingItems
from ..sell_marketing.models.update_ad_group_request import UpdateAdGroupRequest
from ..sell_marketing.models.update_ad_status_by_listing_id_request import UpdateAdStatusByListingIdRequest
from ..sell_marketing.models.update_ad_status_request import UpdateAdStatusRequest
from ..sell_marketing.models.update_adrate_strategy_request import UpdateAdrateStrategyRequest
from ..sell_marketing.models.update_ads_by_inventory_reference_response import UpdateAdsByInventoryReferenceResponse
from ..sell_marketing.models.update_bid_percentage_request import UpdateBidPercentageRequest
from ..sell_marketing.models.update_bidding_strategy_request import UpdateBiddingStrategyRequest
from ..sell_marketing.models.update_campaign_budget_request import UpdateCampaignBudgetRequest
from ..sell_marketing.models.update_campaign_identification_request import UpdateCampaignIdentificationRequest
from ..sell_marketing.models.update_campaign_request import UpdateCampaignRequest
from ..sell_marketing.models.update_email_campaign_response import UpdateEmailCampaignResponse
from ..sell_marketing.models.update_keyword_by_keyword_id_request import UpdateKeywordByKeywordIdRequest
from ..sell_marketing.models.update_keyword_request import UpdateKeywordRequest
from ..sell_marketing.models.update_keyword_response import UpdateKeywordResponse
from ..sell_marketing.models.update_negative_keyword_id_request import UpdateNegativeKeywordIdRequest
from ..sell_marketing.models.update_negative_keyword_request import UpdateNegativeKeywordRequest
from ..sell_marketing.models.update_negative_keyword_response import UpdateNegativeKeywordResponse
