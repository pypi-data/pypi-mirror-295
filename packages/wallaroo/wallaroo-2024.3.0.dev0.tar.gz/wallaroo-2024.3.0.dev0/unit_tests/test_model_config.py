import datetime
import unittest

import responses
import wallaroo
from wallaroo.dynamic_batching_config import DynamicBatchingConfig
from wallaroo.model_config import ModelConfig

from . import testutil


class TestModelConfig(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.gql_client = testutil.new_gql_client(endpoint="http://api-lb/v1/graphql")
        self.test_client = wallaroo.Client(
            gql_client=self.gql_client, auth_type="test_auth", api_endpoint="http://api-lb",config={"default_arch": "x86"}
        )

    @responses.activate
    def test_init_full_dict(self):
        model_config = ModelConfig(
            client=self.test_client,
            data={
                "id": 1,
                "filter_threshold": 0.1234,
                "model": {
                    "id": 2,
                },
                "runtime": "onnx",
                "tensor_fields": ["foo", "bar", "baz"],
                "dynamic_batching_config": {
                    "max_batch_delay_ms": 10,
                    "batch_size_target": 4,
                    "batch_size_limit": 10,
                },
            },
        )

        self.assertEqual(1, model_config.id())
        self.assertEqual(0.1234, model_config.filter_threshold())
        self.assertEqual(2, model_config.model_version().id())
        self.assertEqual("onnx", model_config.runtime())
        self.assertEqual(["foo", "bar", "baz"], model_config.tensor_fields())
        self.assertIsInstance(model_config.dynamic_batching_config(), DynamicBatchingConfig)
        self.assertEqual(10, model_config.dynamic_batching_config().max_batch_delay_ms)

    @responses.activate
    def test_rehydrate(self):
        testcases = [
            ("filter_threshold", 0.1234),
            ("runtime", "onnx"),
            ("tensor_fields", ["foo", "bar"]),
            ("dynamic_batching_config", None),
        ]
        for method_name, want_value in testcases:
            with self.subTest():
                responses.add(
                    responses.POST,
                    "http://api-lb/v1/graphql",
                    status=200,
                    match=[testutil.query_name_matcher("ModelConfigById")],
                    json={
                        "data": {
                            "model_config_by_pk": {
                                "id": 1,
                                "filter_threshold": 0.1234,
                                "model": {
                                    "id": 2,
                                },
                                "runtime": "onnx",
                                "tensor_fields": ["foo", "bar"],
                                "dynamic_batching_config": None
                            },
                        },
                    },
                )

                model_config = ModelConfig(client=self.test_client, data={"id": 1})

                self.assertEqual(want_value, getattr(model_config, method_name)())
                self.assertEqual(1, len(responses.calls))
                # Another call to the same accessor shouldn't trigger any
                # additional GraphQL queries.
                self.assertEqual(want_value, getattr(model_config, method_name)())
                self.assertEqual(1, len(responses.calls))
                responses.reset()
