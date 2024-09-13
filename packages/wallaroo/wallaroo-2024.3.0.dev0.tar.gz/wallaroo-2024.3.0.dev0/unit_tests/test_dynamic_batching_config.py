import json
import unittest

from wallaroo.dynamic_batching_config import DynamicBatchingConfig


class TestDynamicBatchingConfig(unittest.TestCase):
    def setUp(self):
        self.config_dict = {
            'max_batch_delay_ms': 10,
            'batch_size_target': 4,
            'batch_size_limit': 5
        }
        self.config = DynamicBatchingConfig(**self.config_dict)

    def test_init(self):
        self.assertEqual(self.config.max_batch_delay_ms, self.config_dict['max_batch_delay_ms'])
        self.assertEqual(self.config.batch_size_target, self.config_dict['batch_size_target'])
        self.assertEqual(self.config.batch_size_limit, self.config_dict['batch_size_limit'])

    def test_init_wrong_type(self):
        test_cases = [
            {'max_batch_delay_ms': '10', 'batch_size_target': 4, 'batch_size_limit': 5},
            {'max_batch_delay_ms': 10, 'batch_size_target': '4', 'batch_size_limit': 5},
            {'max_batch_delay_ms': 10, 'batch_size_target': 4, 'batch_size_limit': '5'},
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                with self.assertRaises(ValueError):
                    DynamicBatchingConfig(**test_case)

    def test_init_set_wrong_type(self):
        dynamic_batching_config = DynamicBatchingConfig()
        with self.assertRaises(ValueError):
            dynamic_batching_config.max_batch_delay_ms = "hello"

    def test_init_batch_size_limit_none(self):
        dynamic_batching_config = DynamicBatchingConfig(max_batch_delay_ms=10, batch_size_target=4)
        self.assertIsNone(dynamic_batching_config.batch_size_limit)

    def test_from_dict(self):
        config_from_dict = DynamicBatchingConfig.from_dict(self.config_dict)
        self.assertEqual(config_from_dict.max_batch_delay_ms, self.config_dict['max_batch_delay_ms'])
        self.assertEqual(config_from_dict.batch_size_target, self.config_dict['batch_size_target'])
        self.assertEqual(config_from_dict.batch_size_limit, self.config_dict['batch_size_limit'])

    def test_from_dict_wrong_type(self):
        with self.assertRaises(ValueError):
            DynamicBatchingConfig.from_dict({'max_batch_delay_ms': None, 'batch_size_target': 4, 'batch_size_limit': 5})

        with self.assertRaises(ValueError):
            DynamicBatchingConfig.from_dict({'max_batch_delay_ms': 10, 'batch_size_target': '4', 'batch_size_limit': 5})


    def test_to_json(self):
        config_json = self.config.to_json()
        self.assertIsInstance(config_json, dict)
        