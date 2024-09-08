# coding: utf-8

# flake8: noqa
"""
    Metadata API

    The Metadata API has operations that retrieve configuration details pertaining to the different eBay marketplaces. In addition to marketplace information, the API also has operations that get information that helps sellers list items on eBay.  # noqa: E501

    OpenAPI spec version: v1.8.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

# import models into model package
from ...sell_metadata.models.automotive_parts_compatibility_policy import AutomotivePartsCompatibilityPolicy
from ...sell_metadata.models.automotive_parts_compatibility_policy_response import AutomotivePartsCompatibilityPolicyResponse
from ...sell_metadata.models.error import Error
from ...sell_metadata.models.error_parameter import ErrorParameter
from ...sell_metadata.models.extended_producer_responsibility import ExtendedProducerResponsibility
from ...sell_metadata.models.extended_producer_responsibility_policy import ExtendedProducerResponsibilityPolicy
from ...sell_metadata.models.extended_producer_responsibility_policy_response import ExtendedProducerResponsibilityPolicyResponse
from ...sell_metadata.models.hazard_statement import HazardStatement
from ...sell_metadata.models.hazardous_material_details_response import HazardousMaterialDetailsResponse
from ...sell_metadata.models.item_condition import ItemCondition
from ...sell_metadata.models.item_condition_descriptor import ItemConditionDescriptor
from ...sell_metadata.models.item_condition_descriptor_constraint import ItemConditionDescriptorConstraint
from ...sell_metadata.models.item_condition_descriptor_value import ItemConditionDescriptorValue
from ...sell_metadata.models.item_condition_descriptor_value_constraint import ItemConditionDescriptorValueConstraint
from ...sell_metadata.models.item_condition_policy import ItemConditionPolicy
from ...sell_metadata.models.item_condition_policy_response import ItemConditionPolicyResponse
from ...sell_metadata.models.listing_structure_policy import ListingStructurePolicy
from ...sell_metadata.models.listing_structure_policy_response import ListingStructurePolicyResponse
from ...sell_metadata.models.negotiated_price_policy import NegotiatedPricePolicy
from ...sell_metadata.models.negotiated_price_policy_response import NegotiatedPricePolicyResponse
from ...sell_metadata.models.pictogram import Pictogram
from ...sell_metadata.models.product_safety_label_pictogram import ProductSafetyLabelPictogram
from ...sell_metadata.models.product_safety_label_statement import ProductSafetyLabelStatement
from ...sell_metadata.models.product_safety_labels_response import ProductSafetyLabelsResponse
from ...sell_metadata.models.regulatory_attribute import RegulatoryAttribute
from ...sell_metadata.models.regulatory_policy import RegulatoryPolicy
from ...sell_metadata.models.regulatory_policy_response import RegulatoryPolicyResponse
from ...sell_metadata.models.return_policy import ReturnPolicy
from ...sell_metadata.models.return_policy_details import ReturnPolicyDetails
from ...sell_metadata.models.return_policy_response import ReturnPolicyResponse
from ...sell_metadata.models.sales_tax_jurisdiction import SalesTaxJurisdiction
from ...sell_metadata.models.sales_tax_jurisdictions import SalesTaxJurisdictions
from ...sell_metadata.models.signal_word import SignalWord
from ...sell_metadata.models.time_duration import TimeDuration
