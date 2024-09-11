"""
Type annotations for mediaconvert service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediaconvert.client import MediaConvertClient
    from types_aiobotocore_mediaconvert.paginator import (
        DescribeEndpointsPaginator,
        ListJobTemplatesPaginator,
        ListJobsPaginator,
        ListPresetsPaginator,
        ListQueuesPaginator,
        SearchJobsPaginator,
    )

    session = get_session()
    with session.create_client("mediaconvert") as client:
        client: MediaConvertClient

        describe_endpoints_paginator: DescribeEndpointsPaginator = client.get_paginator("describe_endpoints")
        list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_presets_paginator: ListPresetsPaginator = client.get_paginator("list_presets")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
        search_jobs_paginator: SearchJobsPaginator = client.get_paginator("search_jobs")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeEndpointsRequestDescribeEndpointsPaginateTypeDef,
    DescribeEndpointsResponseTypeDef,
    ListJobsRequestListJobsPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesRequestListJobTemplatesPaginateTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListPresetsRequestListPresetsPaginateTypeDef,
    ListPresetsResponseTypeDef,
    ListQueuesRequestListQueuesPaginateTypeDef,
    ListQueuesResponseTypeDef,
    SearchJobsRequestSearchJobsPaginateTypeDef,
    SearchJobsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeEndpointsPaginator",
    "ListJobTemplatesPaginator",
    "ListJobsPaginator",
    "ListPresetsPaginator",
    "ListQueuesPaginator",
    "SearchJobsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeEndpointsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.DescribeEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#describeendpointspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeEndpointsRequestDescribeEndpointsPaginateTypeDef]
    ) -> AsyncIterator[DescribeEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.DescribeEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#describeendpointspaginator)
        """


class ListJobTemplatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListJobTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobtemplatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobTemplatesRequestListJobTemplatesPaginateTypeDef]
    ) -> AsyncIterator[ListJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListJobTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobtemplatespaginator)
        """


class ListJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListJobsRequestListJobsPaginateTypeDef]
    ) -> AsyncIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listjobspaginator)
        """


class ListPresetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListPresets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listpresetspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPresetsRequestListPresetsPaginateTypeDef]
    ) -> AsyncIterator[ListPresetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListPresets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listpresetspaginator)
        """


class ListQueuesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listqueuespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListQueuesRequestListQueuesPaginateTypeDef]
    ) -> AsyncIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.ListQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#listqueuespaginator)
        """


class SearchJobsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.SearchJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#searchjobspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[SearchJobsRequestSearchJobsPaginateTypeDef]
    ) -> AsyncIterator[SearchJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediaconvert.html#MediaConvert.Paginator.SearchJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediaconvert/paginators/#searchjobspaginator)
        """
