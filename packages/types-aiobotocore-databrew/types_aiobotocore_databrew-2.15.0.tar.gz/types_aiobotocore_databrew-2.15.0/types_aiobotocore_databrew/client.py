"""
Type annotations for databrew service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_databrew.client import GlueDataBrewClient

    session = get_session()
    async with session.create_client("databrew") as client:
        client: GlueDataBrewClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListDatasetsPaginator,
    ListJobRunsPaginator,
    ListJobsPaginator,
    ListProjectsPaginator,
    ListRecipesPaginator,
    ListRecipeVersionsPaginator,
    ListRulesetsPaginator,
    ListSchedulesPaginator,
)
from .type_defs import (
    BatchDeleteRecipeVersionRequestRequestTypeDef,
    BatchDeleteRecipeVersionResponseTypeDef,
    CreateDatasetRequestRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateProfileJobRequestRequestTypeDef,
    CreateProfileJobResponseTypeDef,
    CreateProjectRequestRequestTypeDef,
    CreateProjectResponseTypeDef,
    CreateRecipeJobRequestRequestTypeDef,
    CreateRecipeJobResponseTypeDef,
    CreateRecipeRequestRequestTypeDef,
    CreateRecipeResponseTypeDef,
    CreateRulesetRequestRequestTypeDef,
    CreateRulesetResponseTypeDef,
    CreateScheduleRequestRequestTypeDef,
    CreateScheduleResponseTypeDef,
    DeleteDatasetRequestRequestTypeDef,
    DeleteDatasetResponseTypeDef,
    DeleteJobRequestRequestTypeDef,
    DeleteJobResponseTypeDef,
    DeleteProjectRequestRequestTypeDef,
    DeleteProjectResponseTypeDef,
    DeleteRecipeVersionRequestRequestTypeDef,
    DeleteRecipeVersionResponseTypeDef,
    DeleteRulesetRequestRequestTypeDef,
    DeleteRulesetResponseTypeDef,
    DeleteScheduleRequestRequestTypeDef,
    DeleteScheduleResponseTypeDef,
    DescribeDatasetRequestRequestTypeDef,
    DescribeDatasetResponseTypeDef,
    DescribeJobRequestRequestTypeDef,
    DescribeJobResponseTypeDef,
    DescribeJobRunRequestRequestTypeDef,
    DescribeJobRunResponseTypeDef,
    DescribeProjectRequestRequestTypeDef,
    DescribeProjectResponseTypeDef,
    DescribeRecipeRequestRequestTypeDef,
    DescribeRecipeResponseTypeDef,
    DescribeRulesetRequestRequestTypeDef,
    DescribeRulesetResponseTypeDef,
    DescribeScheduleRequestRequestTypeDef,
    DescribeScheduleResponseTypeDef,
    ListDatasetsRequestRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListJobRunsRequestRequestTypeDef,
    ListJobRunsResponseTypeDef,
    ListJobsRequestRequestTypeDef,
    ListJobsResponseTypeDef,
    ListProjectsRequestRequestTypeDef,
    ListProjectsResponseTypeDef,
    ListRecipesRequestRequestTypeDef,
    ListRecipesResponseTypeDef,
    ListRecipeVersionsRequestRequestTypeDef,
    ListRecipeVersionsResponseTypeDef,
    ListRulesetsRequestRequestTypeDef,
    ListRulesetsResponseTypeDef,
    ListSchedulesRequestRequestTypeDef,
    ListSchedulesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PublishRecipeRequestRequestTypeDef,
    PublishRecipeResponseTypeDef,
    SendProjectSessionActionRequestRequestTypeDef,
    SendProjectSessionActionResponseTypeDef,
    StartJobRunRequestRequestTypeDef,
    StartJobRunResponseTypeDef,
    StartProjectSessionRequestRequestTypeDef,
    StartProjectSessionResponseTypeDef,
    StopJobRunRequestRequestTypeDef,
    StopJobRunResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateDatasetRequestRequestTypeDef,
    UpdateDatasetResponseTypeDef,
    UpdateProfileJobRequestRequestTypeDef,
    UpdateProfileJobResponseTypeDef,
    UpdateProjectRequestRequestTypeDef,
    UpdateProjectResponseTypeDef,
    UpdateRecipeJobRequestRequestTypeDef,
    UpdateRecipeJobResponseTypeDef,
    UpdateRecipeRequestRequestTypeDef,
    UpdateRecipeResponseTypeDef,
    UpdateRulesetRequestRequestTypeDef,
    UpdateRulesetResponseTypeDef,
    UpdateScheduleRequestRequestTypeDef,
    UpdateScheduleResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("GlueDataBrewClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class GlueDataBrewClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GlueDataBrewClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#exceptions)
        """

    async def batch_delete_recipe_version(
        self, **kwargs: Unpack[BatchDeleteRecipeVersionRequestRequestTypeDef]
    ) -> BatchDeleteRecipeVersionResponseTypeDef:
        """
        Deletes one or more versions of a recipe at a time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.batch_delete_recipe_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#batch_delete_recipe_version)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#close)
        """

    async def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a new DataBrew dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_dataset)
        """

    async def create_profile_job(
        self, **kwargs: Unpack[CreateProfileJobRequestRequestTypeDef]
    ) -> CreateProfileJobResponseTypeDef:
        """
        Creates a new job to analyze a dataset and create its data profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_profile_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_profile_job)
        """

    async def create_project(
        self, **kwargs: Unpack[CreateProjectRequestRequestTypeDef]
    ) -> CreateProjectResponseTypeDef:
        """
        Creates a new DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_project)
        """

    async def create_recipe(
        self, **kwargs: Unpack[CreateRecipeRequestRequestTypeDef]
    ) -> CreateRecipeResponseTypeDef:
        """
        Creates a new DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_recipe)
        """

    async def create_recipe_job(
        self, **kwargs: Unpack[CreateRecipeJobRequestRequestTypeDef]
    ) -> CreateRecipeJobResponseTypeDef:
        """
        Creates a new job to transform input data, using steps defined in an existing
        Glue DataBrew recipe See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/databrew-2017-07-25/CreateRecipeJob).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_recipe_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_recipe_job)
        """

    async def create_ruleset(
        self, **kwargs: Unpack[CreateRulesetRequestRequestTypeDef]
    ) -> CreateRulesetResponseTypeDef:
        """
        Creates a new ruleset that can be used in a profile job to validate the data
        quality of a
        dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_ruleset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_ruleset)
        """

    async def create_schedule(
        self, **kwargs: Unpack[CreateScheduleRequestRequestTypeDef]
    ) -> CreateScheduleResponseTypeDef:
        """
        Creates a new schedule for one or more DataBrew jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.create_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#create_schedule)
        """

    async def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestRequestTypeDef]
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes a dataset from DataBrew.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_dataset)
        """

    async def delete_job(
        self, **kwargs: Unpack[DeleteJobRequestRequestTypeDef]
    ) -> DeleteJobResponseTypeDef:
        """
        Deletes the specified DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_job)
        """

    async def delete_project(
        self, **kwargs: Unpack[DeleteProjectRequestRequestTypeDef]
    ) -> DeleteProjectResponseTypeDef:
        """
        Deletes an existing DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_project)
        """

    async def delete_recipe_version(
        self, **kwargs: Unpack[DeleteRecipeVersionRequestRequestTypeDef]
    ) -> DeleteRecipeVersionResponseTypeDef:
        """
        Deletes a single version of a DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_recipe_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_recipe_version)
        """

    async def delete_ruleset(
        self, **kwargs: Unpack[DeleteRulesetRequestRequestTypeDef]
    ) -> DeleteRulesetResponseTypeDef:
        """
        Deletes a ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_ruleset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_ruleset)
        """

    async def delete_schedule(
        self, **kwargs: Unpack[DeleteScheduleRequestRequestTypeDef]
    ) -> DeleteScheduleResponseTypeDef:
        """
        Deletes the specified DataBrew schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.delete_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#delete_schedule)
        """

    async def describe_dataset(
        self, **kwargs: Unpack[DescribeDatasetRequestRequestTypeDef]
    ) -> DescribeDatasetResponseTypeDef:
        """
        Returns the definition of a specific DataBrew dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_dataset)
        """

    async def describe_job(
        self, **kwargs: Unpack[DescribeJobRequestRequestTypeDef]
    ) -> DescribeJobResponseTypeDef:
        """
        Returns the definition of a specific DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_job)
        """

    async def describe_job_run(
        self, **kwargs: Unpack[DescribeJobRunRequestRequestTypeDef]
    ) -> DescribeJobRunResponseTypeDef:
        """
        Represents one run of a DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_job_run)
        """

    async def describe_project(
        self, **kwargs: Unpack[DescribeProjectRequestRequestTypeDef]
    ) -> DescribeProjectResponseTypeDef:
        """
        Returns the definition of a specific DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_project)
        """

    async def describe_recipe(
        self, **kwargs: Unpack[DescribeRecipeRequestRequestTypeDef]
    ) -> DescribeRecipeResponseTypeDef:
        """
        Returns the definition of a specific DataBrew recipe corresponding to a
        particular
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_recipe)
        """

    async def describe_ruleset(
        self, **kwargs: Unpack[DescribeRulesetRequestRequestTypeDef]
    ) -> DescribeRulesetResponseTypeDef:
        """
        Retrieves detailed information about the ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_ruleset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_ruleset)
        """

    async def describe_schedule(
        self, **kwargs: Unpack[DescribeScheduleRequestRequestTypeDef]
    ) -> DescribeScheduleResponseTypeDef:
        """
        Returns the definition of a specific DataBrew schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.describe_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#describe_schedule)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#generate_presigned_url)
        """

    async def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all of the DataBrew datasets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_datasets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_datasets)
        """

    async def list_job_runs(
        self, **kwargs: Unpack[ListJobRunsRequestRequestTypeDef]
    ) -> ListJobRunsResponseTypeDef:
        """
        Lists all of the previous runs of a particular DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_job_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_job_runs)
        """

    async def list_jobs(
        self, **kwargs: Unpack[ListJobsRequestRequestTypeDef]
    ) -> ListJobsResponseTypeDef:
        """
        Lists all of the DataBrew jobs that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_jobs)
        """

    async def list_projects(
        self, **kwargs: Unpack[ListProjectsRequestRequestTypeDef]
    ) -> ListProjectsResponseTypeDef:
        """
        Lists all of the DataBrew projects that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_projects)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_projects)
        """

    async def list_recipe_versions(
        self, **kwargs: Unpack[ListRecipeVersionsRequestRequestTypeDef]
    ) -> ListRecipeVersionsResponseTypeDef:
        """
        Lists the versions of a particular DataBrew recipe, except for `LATEST_WORKING`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_recipe_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_recipe_versions)
        """

    async def list_recipes(
        self, **kwargs: Unpack[ListRecipesRequestRequestTypeDef]
    ) -> ListRecipesResponseTypeDef:
        """
        Lists all of the DataBrew recipes that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_recipes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_recipes)
        """

    async def list_rulesets(
        self, **kwargs: Unpack[ListRulesetsRequestRequestTypeDef]
    ) -> ListRulesetsResponseTypeDef:
        """
        List all rulesets available in the current account or rulesets associated with
        a specific resource
        (dataset).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_rulesets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_rulesets)
        """

    async def list_schedules(
        self, **kwargs: Unpack[ListSchedulesRequestRequestTypeDef]
    ) -> ListSchedulesResponseTypeDef:
        """
        Lists the DataBrew schedules that are defined.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_schedules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_schedules)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all the tags for a DataBrew resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#list_tags_for_resource)
        """

    async def publish_recipe(
        self, **kwargs: Unpack[PublishRecipeRequestRequestTypeDef]
    ) -> PublishRecipeResponseTypeDef:
        """
        Publishes a new version of a DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.publish_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#publish_recipe)
        """

    async def send_project_session_action(
        self, **kwargs: Unpack[SendProjectSessionActionRequestRequestTypeDef]
    ) -> SendProjectSessionActionResponseTypeDef:
        """
        Performs a recipe step within an interactive DataBrew session that's currently
        open.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.send_project_session_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#send_project_session_action)
        """

    async def start_job_run(
        self, **kwargs: Unpack[StartJobRunRequestRequestTypeDef]
    ) -> StartJobRunResponseTypeDef:
        """
        Runs a DataBrew job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.start_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#start_job_run)
        """

    async def start_project_session(
        self, **kwargs: Unpack[StartProjectSessionRequestRequestTypeDef]
    ) -> StartProjectSessionResponseTypeDef:
        """
        Creates an interactive session, enabling you to manipulate data in a DataBrew
        project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.start_project_session)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#start_project_session)
        """

    async def stop_job_run(
        self, **kwargs: Unpack[StopJobRunRequestRequestTypeDef]
    ) -> StopJobRunResponseTypeDef:
        """
        Stops a particular run of a job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.stop_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#stop_job_run)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds metadata tags to a DataBrew resource, such as a dataset, project, recipe,
        job, or
        schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes metadata tags from a DataBrew resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#untag_resource)
        """

    async def update_dataset(
        self, **kwargs: Unpack[UpdateDatasetRequestRequestTypeDef]
    ) -> UpdateDatasetResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_dataset)
        """

    async def update_profile_job(
        self, **kwargs: Unpack[UpdateProfileJobRequestRequestTypeDef]
    ) -> UpdateProfileJobResponseTypeDef:
        """
        Modifies the definition of an existing profile job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_profile_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_profile_job)
        """

    async def update_project(
        self, **kwargs: Unpack[UpdateProjectRequestRequestTypeDef]
    ) -> UpdateProjectResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_project)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_project)
        """

    async def update_recipe(
        self, **kwargs: Unpack[UpdateRecipeRequestRequestTypeDef]
    ) -> UpdateRecipeResponseTypeDef:
        """
        Modifies the definition of the `LATEST_WORKING` version of a DataBrew recipe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_recipe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_recipe)
        """

    async def update_recipe_job(
        self, **kwargs: Unpack[UpdateRecipeJobRequestRequestTypeDef]
    ) -> UpdateRecipeJobResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew recipe job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_recipe_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_recipe_job)
        """

    async def update_ruleset(
        self, **kwargs: Unpack[UpdateRulesetRequestRequestTypeDef]
    ) -> UpdateRulesetResponseTypeDef:
        """
        Updates specified ruleset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_ruleset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_ruleset)
        """

    async def update_schedule(
        self, **kwargs: Unpack[UpdateScheduleRequestRequestTypeDef]
    ) -> UpdateScheduleResponseTypeDef:
        """
        Modifies the definition of an existing DataBrew schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.update_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#update_schedule)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datasets"]) -> ListDatasetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_job_runs"]) -> ListJobRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recipe_versions"]
    ) -> ListRecipeVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_recipes"]) -> ListRecipesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_rulesets"]) -> ListRulesetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_schedules"]) -> ListSchedulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/#get_paginator)
        """

    async def __aenter__(self) -> "GlueDataBrewClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/databrew.html#GlueDataBrew.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/client/)
        """
