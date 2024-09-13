import datetime
from io import StringIO
import sys
from unittest import mock
import responses
import unittest
import respx

import wallaroo
from wallaroo.deployment import WaitForDeployError
from wallaroo.deployment_config import DeploymentConfigBuilder
from wallaroo.engine_config import Acceleration, Architecture, InvalidAccelerationError
from wallaroo.model_version import ModelVersion
from wallaroo.model_config import ModelConfig
from wallaroo.pipeline import Pipeline
from wallaroo.pipeline_version import PipelineVersion

from . import status_samples
from . import testutil
from unit_tests.reusable_responders import (
    add_default_workspace_responder,
    add_deploy_responder,
    add_deployment_by_id_responder,
    add_deployment_status_responder,
    add_get_model_by_id_responder,
    add_get_model_config_by_id_responder,
    add_pipeline_variant_by_id_responder,
)


class TestPipelineVersion(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(
                endpoint="http://api-lb:8080/v1/graphql"
            )
        self.test_client = wallaroo.Client(
            request_timeout=2, gql_client=self.gql_client, auth_type="test_auth", api_endpoint="http://api-lb:8080", config={"default_arch": "x86"}
        )

        self.default_model_config = ModelConfig(
            self.test_client,
            data={
                "id": 1,
                "model": {"id": 1, "model_id": "ccfraud", "model_version": "default"},
            },
        )
        self.experiment_model_config = ModelConfig(
            self.test_client,
            data={
                "id": 2,
                "model": {
                    "id": 2,
                    "model_id": "ccfraud",
                    "model_version": "experiment",
                },
            },
        )
        self.variant = PipelineVersion(
            client=self.test_client,
            data={
                "id": 1,
            },
        )

    def add_deploy_test_responders(self):
        workspace_name = "test-logs-workspace"
        add_default_workspace_responder(api_endpoint=self.test_client.api_endpoint, workspace_name=workspace_name)
        add_pipeline_variant_by_id_responder(api_endpoint=self.test_client.api_endpoint)
  
        # ids will be wrong for one of the model config calls, but we're only checking runtime
        add_get_model_config_by_id_responder(api_endpoint=self.test_client.api_endpoint)
        add_deployment_by_id_responder(api_endpoint=self.test_client.api_endpoint, deployment_id=10, deployment_name="foo-deployment")
        add_get_model_by_id_responder(api_endpoint=self.test_client.api_endpoint, model_id=1)
    
    @responses.activate
    def test_init_full_dict(self):
        variant = PipelineVersion(
            client=self.test_client,
            data={
                "id": 2,
                "version": "v1",
                "created_at": self.now.isoformat(),
                "updated_at": self.now.isoformat(),
                "definition": {
                    "id": "test-pipeline",
                    "steps": [
                        {
                            "id": "metavalue_split",
                            "args": ["card_type", "default", "gold", "experiment"],
                            "operation": "map",
                        }
                    ],
                },
                "pipeline": {"id": 1},
                "deployment_pipeline_versions": [],
            },
        )

        self.assertEqual(2, variant.id())
        self.assertEqual("v1", variant.name())
        self.assertEqual(self.now, variant.create_time())
        self.assertEqual(self.now, variant.last_update_time())
        self.assertEqual(
            {
                "id": "test-pipeline",
                "steps": [
                    {
                        "id": "metavalue_split",
                        "args": ["card_type", "default", "gold", "experiment"],
                        "operation": "map",
                    }
                ],
            },
            variant.definition(),
        )
        self.assertIsInstance(variant.pipeline(), Pipeline)
        # TODO: Test deployment_pipeline_versions

    @responses.activate
    def test_rehydrate(self):
        testcases = [
            ("name", "v1"),
            ("create_time", self.now),
            ("last_update_time", self.now),
            (
                "definition",
                {
                    "id": "test-pipeline",
                    "steps": [
                        {
                            "id": "metavalue_split",
                            "args": ["card_type", "default", "gold", "experiment"],
                            "operation": "map",
                        }
                    ],
                },
            )
            # TODO: Test deployments()
        ]
        for method_name, want_value in testcases:
            with self.subTest():
                responses.add(
                    responses.POST,
                    f"{self.test_client.api_endpoint}/v1/graphql",
                    status=200,
                    match=[testutil.query_name_matcher("PipelineVariantById")],
                    json={
                        "data": {
                            "pipeline_version_by_pk": {
                                "id": 2,
                                "created_at": self.now.isoformat(),
                                "updated_at": self.now.isoformat(),
                                "version": "v1",
                                "definition": {
                                    "id": "test-pipeline",
                                    "steps": [
                                        {
                                            "id": "metavalue_split",
                                            "args": [
                                                "card_type",
                                                "default",
                                                "gold",
                                                "experiment",
                                            ],
                                            "operation": "map",
                                        }
                                    ],
                                },
                                "pipeline": {"id": 1},
                                "deployment_pipeline_versions": [],
                            }
                        }
                    },
                )

                variant = PipelineVersion(client=self.test_client, data={"id": 2})

                self.assertEqual(want_value, getattr(variant, method_name)())
                self.assertEqual(1, len(responses.calls))
                # Another call to the same accessor shouldn't trigger any
                # additional GraphQL queries.
                self.assertEqual(want_value, getattr(variant, method_name)())
                self.assertEqual(1, len(responses.calls))
                responses.reset()

    @responses.activate
    @respx.mock(assert_all_called=True)
    def test_deploy_success(self, respx_mock):
        self.add_deploy_test_responders()
        add_deployment_status_responder(api_endpoint=self.test_client.api_endpoint, deployment_name="foo-deployment-10", status=status_samples.RUNNING)
        add_deploy_responder(respx_mock, 10, self.test_client.api_endpoint)

        #default workflow
        deployment = self.variant.deploy(
            "foo-deployment", [self.default_model_config, self.experiment_model_config]
        )

        self.assertEqual(10, deployment.id())
        self.assertEqual("foo-deployment", deployment.name())

    @responses.activate
    @respx.mock(assert_all_called=True)
    def test_deploy_do_not_wait_for_success(self, respx_mock):
        self.add_deploy_test_responders()
        add_deployment_status_responder(api_endpoint=self.test_client.api_endpoint, deployment_name="foo-deployment-10", status=status_samples.RUNNING)
        add_deploy_responder(respx_mock, 10, self.test_client.api_endpoint)
        #With wait_for_status=False
        expected_string = ("Deployment initiated for foo-deployment. Please check pipeline status.\n")
        with mock.patch('sys.stdout', new = StringIO()) as fake_out: 
            deployment = self.variant.deploy(
                "foo-deployment", [self.default_model_config], wait_for_status=False
            )
            self.assertIsNone(deployment)
            self.assertEqual(fake_out.getvalue(), expected_string)


    @responses.activate
    @respx.mock(assert_all_called=True)
    def test_deploy_failure(self, respx_mock):
        self.add_deploy_test_responders()
        add_deploy_responder(respx_mock, 10, self.test_client.api_endpoint)
        # Test Failure case
        add_deployment_status_responder(api_endpoint=self.test_client.api_endpoint, deployment_name="foo-deployment-10", status=status_samples.ERROR)
        with self.assertRaises(WaitForDeployError):
            deployment = self.variant.deploy(
                "foo-deployment", [self.default_model_config, self.experiment_model_config]
            )

    def test_validate_acceleration_empty(self):
        dc = DeploymentConfigBuilder().build()
        new_dc = PipelineVersion._validate_deployment_config(dc, [])
        self.assertEqual(dc, new_dc)

    def test_validate_acceleration_ok(self):
        dc = (
            DeploymentConfigBuilder()
            .arch(Architecture.ARM)
            .accel(Acceleration.CUDA)
            .build()
        )
        new_dc = PipelineVersion._validate_deployment_config(dc, [])
        self.assertEqual(dc, new_dc)

    def test_validate_acceleration_aux_ok(self):
        mv = ModelVersion(
            None,
            {
                "id": "test",
                "name": "test",
                "arch": str(Architecture.ARM),
                "accel": str(Acceleration.CUDA),
            },
            True,
        )
        dc = (
            DeploymentConfigBuilder()
            .sidekick_arch(mv, Architecture.ARM)
            .sidekick_accel(mv, Acceleration.CUDA)
            .build()
        )
        mc = ModelConfig(None, {"id": "test", "model": mv}, True)
        new_dc = PipelineVersion._validate_deployment_config(dc, [mc])
        self.assertEqual(str(Architecture.ARM), new_dc["engine"].get("arch"))
        self.assertEqual(str(Acceleration.CUDA), new_dc["engine"].get("accel"))

    def test_validate_acceleration_err(self):
        dc = DeploymentConfigBuilder().accel(Acceleration.AIO).build()
        with self.assertRaises(InvalidAccelerationError):
            PipelineVersion._validate_deployment_config(dc, [])

    def test_validate_acceleration_aux_err(self):
        mv = ModelVersion(
            None,
            {
                "id": "test",
                "name": "test",
                "arch": None,
                "accel": str(Acceleration.AIO),
            },
            True,
        )
        dc = DeploymentConfigBuilder().sidekick_accel(mv, Acceleration.AIO).build()
        mc = ModelConfig(None, {"id": "test", "model": mv}, True)
        with self.assertRaises(InvalidAccelerationError):
            PipelineVersion._validate_deployment_config(dc, [mc])
