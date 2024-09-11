"""
Type annotations for billingconductor service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_billingconductor.client import BillingConductorClient
    from types_aiobotocore_billingconductor.paginator import (
        ListAccountAssociationsPaginator,
        ListBillingGroupCostReportsPaginator,
        ListBillingGroupsPaginator,
        ListCustomLineItemVersionsPaginator,
        ListCustomLineItemsPaginator,
        ListPricingPlansPaginator,
        ListPricingPlansAssociatedWithPricingRulePaginator,
        ListPricingRulesPaginator,
        ListPricingRulesAssociatedToPricingPlanPaginator,
        ListResourcesAssociatedToCustomLineItemPaginator,
    )

    session = get_session()
    with session.create_client("billingconductor") as client:
        client: BillingConductorClient

        list_account_associations_paginator: ListAccountAssociationsPaginator = client.get_paginator("list_account_associations")
        list_billing_group_cost_reports_paginator: ListBillingGroupCostReportsPaginator = client.get_paginator("list_billing_group_cost_reports")
        list_billing_groups_paginator: ListBillingGroupsPaginator = client.get_paginator("list_billing_groups")
        list_custom_line_item_versions_paginator: ListCustomLineItemVersionsPaginator = client.get_paginator("list_custom_line_item_versions")
        list_custom_line_items_paginator: ListCustomLineItemsPaginator = client.get_paginator("list_custom_line_items")
        list_pricing_plans_paginator: ListPricingPlansPaginator = client.get_paginator("list_pricing_plans")
        list_pricing_plans_associated_with_pricing_rule_paginator: ListPricingPlansAssociatedWithPricingRulePaginator = client.get_paginator("list_pricing_plans_associated_with_pricing_rule")
        list_pricing_rules_paginator: ListPricingRulesPaginator = client.get_paginator("list_pricing_rules")
        list_pricing_rules_associated_to_pricing_plan_paginator: ListPricingRulesAssociatedToPricingPlanPaginator = client.get_paginator("list_pricing_rules_associated_to_pricing_plan")
        list_resources_associated_to_custom_line_item_paginator: ListResourcesAssociatedToCustomLineItemPaginator = client.get_paginator("list_resources_associated_to_custom_line_item")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListAccountAssociationsInputListAccountAssociationsPaginateTypeDef,
    ListAccountAssociationsOutputTypeDef,
    ListBillingGroupCostReportsInputListBillingGroupCostReportsPaginateTypeDef,
    ListBillingGroupCostReportsOutputTypeDef,
    ListBillingGroupsInputListBillingGroupsPaginateTypeDef,
    ListBillingGroupsOutputTypeDef,
    ListCustomLineItemsInputListCustomLineItemsPaginateTypeDef,
    ListCustomLineItemsOutputTypeDef,
    ListCustomLineItemVersionsInputListCustomLineItemVersionsPaginateTypeDef,
    ListCustomLineItemVersionsOutputTypeDef,
    ListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef,
    ListPricingPlansAssociatedWithPricingRuleOutputTypeDef,
    ListPricingPlansInputListPricingPlansPaginateTypeDef,
    ListPricingPlansOutputTypeDef,
    ListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef,
    ListPricingRulesAssociatedToPricingPlanOutputTypeDef,
    ListPricingRulesInputListPricingRulesPaginateTypeDef,
    ListPricingRulesOutputTypeDef,
    ListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef,
    ListResourcesAssociatedToCustomLineItemOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAccountAssociationsPaginator",
    "ListBillingGroupCostReportsPaginator",
    "ListBillingGroupsPaginator",
    "ListCustomLineItemVersionsPaginator",
    "ListCustomLineItemsPaginator",
    "ListPricingPlansPaginator",
    "ListPricingPlansAssociatedWithPricingRulePaginator",
    "ListPricingRulesPaginator",
    "ListPricingRulesAssociatedToPricingPlanPaginator",
    "ListResourcesAssociatedToCustomLineItemPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccountAssociationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListAccountAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listaccountassociationspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListAccountAssociationsInputListAccountAssociationsPaginateTypeDef]
    ) -> AsyncIterator[ListAccountAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListAccountAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listaccountassociationspaginator)
        """

class ListBillingGroupCostReportsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListBillingGroupCostReports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listbillinggroupcostreportspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListBillingGroupCostReportsInputListBillingGroupCostReportsPaginateTypeDef
        ],
    ) -> AsyncIterator[ListBillingGroupCostReportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListBillingGroupCostReports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listbillinggroupcostreportspaginator)
        """

class ListBillingGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListBillingGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listbillinggroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListBillingGroupsInputListBillingGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListBillingGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListBillingGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listbillinggroupspaginator)
        """

class ListCustomLineItemVersionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListCustomLineItemVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listcustomlineitemversionspaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[ListCustomLineItemVersionsInputListCustomLineItemVersionsPaginateTypeDef],
    ) -> AsyncIterator[ListCustomLineItemVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListCustomLineItemVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listcustomlineitemversionspaginator)
        """

class ListCustomLineItemsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListCustomLineItems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listcustomlineitemspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListCustomLineItemsInputListCustomLineItemsPaginateTypeDef]
    ) -> AsyncIterator[ListCustomLineItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListCustomLineItems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listcustomlineitemspaginator)
        """

class ListPricingPlansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingPlans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingplanspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPricingPlansInputListPricingPlansPaginateTypeDef]
    ) -> AsyncIterator[ListPricingPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingPlans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingplanspaginator)
        """

class ListPricingPlansAssociatedWithPricingRulePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingPlansAssociatedWithPricingRule)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingplansassociatedwithpricingrulepaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListPricingPlansAssociatedWithPricingRuleInputListPricingPlansAssociatedWithPricingRulePaginateTypeDef
        ],
    ) -> AsyncIterator[ListPricingPlansAssociatedWithPricingRuleOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingPlansAssociatedWithPricingRule.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingplansassociatedwithpricingrulepaginator)
        """

class ListPricingRulesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingrulespaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListPricingRulesInputListPricingRulesPaginateTypeDef]
    ) -> AsyncIterator[ListPricingRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingrulespaginator)
        """

class ListPricingRulesAssociatedToPricingPlanPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingRulesAssociatedToPricingPlan)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingrulesassociatedtopricingplanpaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListPricingRulesAssociatedToPricingPlanInputListPricingRulesAssociatedToPricingPlanPaginateTypeDef
        ],
    ) -> AsyncIterator[ListPricingRulesAssociatedToPricingPlanOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListPricingRulesAssociatedToPricingPlan.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingrulesassociatedtopricingplanpaginator)
        """

class ListResourcesAssociatedToCustomLineItemPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListResourcesAssociatedToCustomLineItem)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listresourcesassociatedtocustomlineitempaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListResourcesAssociatedToCustomLineItemInputListResourcesAssociatedToCustomLineItemPaginateTypeDef
        ],
    ) -> AsyncIterator[ListResourcesAssociatedToCustomLineItemOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Paginator.ListResourcesAssociatedToCustomLineItem.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listresourcesassociatedtocustomlineitempaginator)
        """
