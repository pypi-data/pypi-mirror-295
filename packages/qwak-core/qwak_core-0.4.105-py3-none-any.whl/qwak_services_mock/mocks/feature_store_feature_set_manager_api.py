import uuid

import grpc
from _qwak_proto.qwak.feature_store.features.feature_set_pb2 import (
    DeployedModelInUseLink,
    FeatureSet,
    FeatureSetDefinition,
    FeatureSetList,
    FeatureSetMetadata,
    FeaturesetSchedulingState,
    FeatureSetSpec,
    FeatureStatus,
)
from _qwak_proto.qwak.feature_store.features.feature_set_service_pb2 import (
    DeleteFeatureSetResponse,
    GetEnvToFeatureSetsMappingResponse,
    GetFeatureSetByNameResponse,
    GetFeaturesetSchedulingStateResponse,
    ListFeatureSetsResponse,
    RegisterFeatureSetResponse,
    UpdateFeatureSetResponse,
)
from _qwak_proto.qwak.feature_store.features.feature_set_service_pb2_grpc import (
    FeatureSetServiceServicer,
)

CURRENT_ENV_NAME = "env_name"


class FeatureSetServiceMock(FeatureSetServiceServicer):
    def __init__(self):
        self._features_spec = {}
        # this mapping is used to test the GetEnvToFeatureSetsMapping API. Note that the populated features sets may not be aligned with the self._features_spec featuresets
        self._env_to_features_spec = (
            {}
        )  # env_name -> {featureset_name -> featureset_definition}

    def reset_features(self):
        self._features_spec.clear()
        self._env_to_features_spec.clear()

    def setup_empty_env(self, env_name):
        self._env_to_features_spec[env_name] = {}

    def register_featureset_to_env_to_features_map(
        self, env_name, featureset_spec: FeatureSetSpec
    ):
        fs_id = str(uuid.uuid4())
        self._env_to_features_spec[env_name] = self._env_to_features_spec.get(
            env_name, {}
        )
        feature_set_definition = FeatureSetDefinition(
            feature_set_id=fs_id,
            feature_set_spec=featureset_spec,
            status=FeatureStatus.VALID,
        )
        self._env_to_features_spec[env_name][
            featureset_spec.name
        ] = feature_set_definition

    def RegisterFeatureSet(self, request, context):
        fs_id = str(uuid.uuid4())
        self._features_spec[fs_id] = request.feature_set_spec
        return RegisterFeatureSetResponse(
            feature_set=FeatureSet(
                feature_set_definition=FeatureSetDefinition(
                    feature_set_id=fs_id, feature_set_spec=request.feature_set_spec
                )
            )
        )

    def UpdateFeatureSet(self, request, context):
        fs_id: str = request.feature_set_id
        self._features_spec[fs_id] = request.feature_set_spec
        return UpdateFeatureSetResponse(
            feature_set=FeatureSet(
                feature_set_definition=FeatureSetDefinition(
                    feature_set_id=fs_id, feature_set_spec=request.feature_set_spec
                )
            )
        )

    def DeleteFeatureSet(self, request, context):
        if request.feature_set_id in self._features_spec:
            self._features_spec.pop(request.feature_set_id)
            return DeleteFeatureSetResponse()

        context.set_details(f"Feature set ID {request.feature_set_id} doesn't exist'")
        context.set_code(grpc.StatusCode.NOT_FOUND)

    def GetFeatureSetByName(self, request, context):
        feature_sets = [
            (fs_id, fs_spec)
            for (fs_id, fs_spec) in self._features_spec.items()
            if fs_spec.name == request.feature_set_name
        ]
        if feature_sets:
            fs_id, fs_spec = feature_sets[0]
            return GetFeatureSetByNameResponse(
                feature_set=FeatureSet(
                    feature_set_definition=FeatureSetDefinition(
                        feature_set_id=fs_id,
                        feature_set_spec=fs_spec,
                        status=FeatureStatus.VALID,
                    ),
                    metadata=FeatureSetMetadata(),
                    deployed_models_in_use_link=[DeployedModelInUseLink()],
                )
            )

        context.set_details(
            f"Feature set named {request.feature_set_name} doesn't exist'"
        )
        context.set_code(grpc.StatusCode.NOT_FOUND)

    def ListFeatureSets(self, request, context):
        return ListFeatureSetsResponse(
            feature_families=[
                FeatureSet(
                    feature_set_definition=FeatureSetDefinition(
                        feature_set_spec=feature_spec, status=FeatureStatus.VALID
                    ),
                    metadata=FeatureSetMetadata(),
                    deployed_models_in_use_link=[DeployedModelInUseLink()],
                )
                for feature_spec in self._features_spec.values()
            ]
        )

    def GetFeaturesetSchedulingState(self, request, context):
        return GetFeaturesetSchedulingStateResponse(
            state=FeaturesetSchedulingState.SCHEDULING_STATE_ENABLED
        )

    def GetEnvToFeatureSetsMapping(self, request, context):
        env_to_featuresets_mapping = {}

        for env_name, featureset_df_dict in self._env_to_features_spec.items():
            env_to_featuresets_mapping[env_name] = FeatureSetList(
                feature_sets=[
                    FeatureSet(
                        feature_set_definition=fs_definition,
                        metadata=FeatureSetMetadata(),
                        deployed_models_in_use_link=[DeployedModelInUseLink()],
                    )
                    for fs_name, fs_definition in featureset_df_dict.items()
                ]
            )

        return GetEnvToFeatureSetsMappingResponse(
            env_to_feature_set_mapping=env_to_featuresets_mapping
        )
