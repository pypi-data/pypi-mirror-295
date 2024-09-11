"""
Type annotations for fis service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_fis.client import FISClient

    session = get_session()
    async with session.create_client("fis") as client:
        client: FISClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    CreateExperimentTemplateRequestRequestTypeDef,
    CreateExperimentTemplateResponseTypeDef,
    CreateTargetAccountConfigurationRequestRequestTypeDef,
    CreateTargetAccountConfigurationResponseTypeDef,
    DeleteExperimentTemplateRequestRequestTypeDef,
    DeleteExperimentTemplateResponseTypeDef,
    DeleteTargetAccountConfigurationRequestRequestTypeDef,
    DeleteTargetAccountConfigurationResponseTypeDef,
    GetActionRequestRequestTypeDef,
    GetActionResponseTypeDef,
    GetExperimentRequestRequestTypeDef,
    GetExperimentResponseTypeDef,
    GetExperimentTargetAccountConfigurationRequestRequestTypeDef,
    GetExperimentTargetAccountConfigurationResponseTypeDef,
    GetExperimentTemplateRequestRequestTypeDef,
    GetExperimentTemplateResponseTypeDef,
    GetSafetyLeverRequestRequestTypeDef,
    GetSafetyLeverResponseTypeDef,
    GetTargetAccountConfigurationRequestRequestTypeDef,
    GetTargetAccountConfigurationResponseTypeDef,
    GetTargetResourceTypeRequestRequestTypeDef,
    GetTargetResourceTypeResponseTypeDef,
    ListActionsRequestRequestTypeDef,
    ListActionsResponseTypeDef,
    ListExperimentResolvedTargetsRequestRequestTypeDef,
    ListExperimentResolvedTargetsResponseTypeDef,
    ListExperimentsRequestRequestTypeDef,
    ListExperimentsResponseTypeDef,
    ListExperimentTargetAccountConfigurationsRequestRequestTypeDef,
    ListExperimentTargetAccountConfigurationsResponseTypeDef,
    ListExperimentTemplatesRequestRequestTypeDef,
    ListExperimentTemplatesResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetAccountConfigurationsRequestRequestTypeDef,
    ListTargetAccountConfigurationsResponseTypeDef,
    ListTargetResourceTypesRequestRequestTypeDef,
    ListTargetResourceTypesResponseTypeDef,
    StartExperimentRequestRequestTypeDef,
    StartExperimentResponseTypeDef,
    StopExperimentRequestRequestTypeDef,
    StopExperimentResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateExperimentTemplateRequestRequestTypeDef,
    UpdateExperimentTemplateResponseTypeDef,
    UpdateSafetyLeverStateRequestRequestTypeDef,
    UpdateSafetyLeverStateResponseTypeDef,
    UpdateTargetAccountConfigurationRequestRequestTypeDef,
    UpdateTargetAccountConfigurationResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("FISClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class FISClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FISClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#close)
        """

    async def create_experiment_template(
        self, **kwargs: Unpack[CreateExperimentTemplateRequestRequestTypeDef]
    ) -> CreateExperimentTemplateResponseTypeDef:
        """
        Creates an experiment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.create_experiment_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#create_experiment_template)
        """

    async def create_target_account_configuration(
        self, **kwargs: Unpack[CreateTargetAccountConfigurationRequestRequestTypeDef]
    ) -> CreateTargetAccountConfigurationResponseTypeDef:
        """
        Creates a target account configuration for the experiment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.create_target_account_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#create_target_account_configuration)
        """

    async def delete_experiment_template(
        self, **kwargs: Unpack[DeleteExperimentTemplateRequestRequestTypeDef]
    ) -> DeleteExperimentTemplateResponseTypeDef:
        """
        Deletes the specified experiment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.delete_experiment_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#delete_experiment_template)
        """

    async def delete_target_account_configuration(
        self, **kwargs: Unpack[DeleteTargetAccountConfigurationRequestRequestTypeDef]
    ) -> DeleteTargetAccountConfigurationResponseTypeDef:
        """
        Deletes the specified target account configuration of the experiment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.delete_target_account_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#delete_target_account_configuration)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#generate_presigned_url)
        """

    async def get_action(
        self, **kwargs: Unpack[GetActionRequestRequestTypeDef]
    ) -> GetActionResponseTypeDef:
        """
        Gets information about the specified FIS action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.get_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#get_action)
        """

    async def get_experiment(
        self, **kwargs: Unpack[GetExperimentRequestRequestTypeDef]
    ) -> GetExperimentResponseTypeDef:
        """
        Gets information about the specified experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.get_experiment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#get_experiment)
        """

    async def get_experiment_target_account_configuration(
        self, **kwargs: Unpack[GetExperimentTargetAccountConfigurationRequestRequestTypeDef]
    ) -> GetExperimentTargetAccountConfigurationResponseTypeDef:
        """
        Gets information about the specified target account configuration of the
        experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.get_experiment_target_account_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#get_experiment_target_account_configuration)
        """

    async def get_experiment_template(
        self, **kwargs: Unpack[GetExperimentTemplateRequestRequestTypeDef]
    ) -> GetExperimentTemplateResponseTypeDef:
        """
        Gets information about the specified experiment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.get_experiment_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#get_experiment_template)
        """

    async def get_safety_lever(
        self, **kwargs: Unpack[GetSafetyLeverRequestRequestTypeDef]
    ) -> GetSafetyLeverResponseTypeDef:
        """
        Gets information about the specified safety lever.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.get_safety_lever)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#get_safety_lever)
        """

    async def get_target_account_configuration(
        self, **kwargs: Unpack[GetTargetAccountConfigurationRequestRequestTypeDef]
    ) -> GetTargetAccountConfigurationResponseTypeDef:
        """
        Gets information about the specified target account configuration of the
        experiment
        template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.get_target_account_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#get_target_account_configuration)
        """

    async def get_target_resource_type(
        self, **kwargs: Unpack[GetTargetResourceTypeRequestRequestTypeDef]
    ) -> GetTargetResourceTypeResponseTypeDef:
        """
        Gets information about the specified resource type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.get_target_resource_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#get_target_resource_type)
        """

    async def list_actions(
        self, **kwargs: Unpack[ListActionsRequestRequestTypeDef]
    ) -> ListActionsResponseTypeDef:
        """
        Lists the available FIS actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.list_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#list_actions)
        """

    async def list_experiment_resolved_targets(
        self, **kwargs: Unpack[ListExperimentResolvedTargetsRequestRequestTypeDef]
    ) -> ListExperimentResolvedTargetsResponseTypeDef:
        """
        Lists the resolved targets information of the specified experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.list_experiment_resolved_targets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#list_experiment_resolved_targets)
        """

    async def list_experiment_target_account_configurations(
        self, **kwargs: Unpack[ListExperimentTargetAccountConfigurationsRequestRequestTypeDef]
    ) -> ListExperimentTargetAccountConfigurationsResponseTypeDef:
        """
        Lists the target account configurations of the specified experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.list_experiment_target_account_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#list_experiment_target_account_configurations)
        """

    async def list_experiment_templates(
        self, **kwargs: Unpack[ListExperimentTemplatesRequestRequestTypeDef]
    ) -> ListExperimentTemplatesResponseTypeDef:
        """
        Lists your experiment templates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.list_experiment_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#list_experiment_templates)
        """

    async def list_experiments(
        self, **kwargs: Unpack[ListExperimentsRequestRequestTypeDef]
    ) -> ListExperimentsResponseTypeDef:
        """
        Lists your experiments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.list_experiments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#list_experiments)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#list_tags_for_resource)
        """

    async def list_target_account_configurations(
        self, **kwargs: Unpack[ListTargetAccountConfigurationsRequestRequestTypeDef]
    ) -> ListTargetAccountConfigurationsResponseTypeDef:
        """
        Lists the target account configurations of the specified experiment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.list_target_account_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#list_target_account_configurations)
        """

    async def list_target_resource_types(
        self, **kwargs: Unpack[ListTargetResourceTypesRequestRequestTypeDef]
    ) -> ListTargetResourceTypesResponseTypeDef:
        """
        Lists the target resource types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.list_target_resource_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#list_target_resource_types)
        """

    async def start_experiment(
        self, **kwargs: Unpack[StartExperimentRequestRequestTypeDef]
    ) -> StartExperimentResponseTypeDef:
        """
        Starts running an experiment from the specified experiment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.start_experiment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#start_experiment)
        """

    async def stop_experiment(
        self, **kwargs: Unpack[StopExperimentRequestRequestTypeDef]
    ) -> StopExperimentResponseTypeDef:
        """
        Stops the specified experiment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.stop_experiment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#stop_experiment)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Applies the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#untag_resource)
        """

    async def update_experiment_template(
        self, **kwargs: Unpack[UpdateExperimentTemplateRequestRequestTypeDef]
    ) -> UpdateExperimentTemplateResponseTypeDef:
        """
        Updates the specified experiment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.update_experiment_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#update_experiment_template)
        """

    async def update_safety_lever_state(
        self, **kwargs: Unpack[UpdateSafetyLeverStateRequestRequestTypeDef]
    ) -> UpdateSafetyLeverStateResponseTypeDef:
        """
        Updates the specified safety lever state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.update_safety_lever_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#update_safety_lever_state)
        """

    async def update_target_account_configuration(
        self, **kwargs: Unpack[UpdateTargetAccountConfigurationRequestRequestTypeDef]
    ) -> UpdateTargetAccountConfigurationResponseTypeDef:
        """
        Updates the target account configuration for the specified experiment template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client.update_target_account_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/#update_target_account_configuration)
        """

    async def __aenter__(self) -> "FISClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis.html#FIS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/client/)
        """
