from unittest import TestCase
from unittest.mock import patch

from callback_functions import slack_events_url_endpoint_aws_lambda
from callback_functions.aws_callback import AWSRequestFromEvents


class TestAWSCallback(TestCase):

    def setUp(self) -> None:
        self.patch_callback = patch("callback_functions.aws_callback.slack_events_receive_callback")
        self.callback = self.patch_callback.start()

    def tearDown(self) -> None:
        self.patch_callback.stop()

    def test_slack_events_url_endpoint_aws_lambda__creates_the_expected_object_type(self):
        fake_event_data = dict(headers={}, queryStringParameters={}, body={})
        fake_context_data = {}

        slack_events_url_endpoint_aws_lambda(fake_event_data, fake_context_data)
        self.assertEqual(AWSRequestFromEvents, type(self.callback.call_args[0][0]))

    def test_AWSRequestFromEvents__properly_instantiates_params(self):
        fake_data = dict(
            headers={"header_key": "header_value"},
            params={"param_key": "param_value"},
            body={"key_1": "value_1", "key_2": "value_2"},
        )
        actual_object = AWSRequestFromEvents(**fake_data)
        self.assertEqual(fake_data["headers"], actual_object.headers)
        self.assertEqual(fake_data["params"], actual_object.params)
        self.assertEqual(fake_data["body"], actual_object.body)

    def test_AWSRequestFromEvents_obj__get_json__returns_expected(self):
        fake_data = dict(
            headers={"header_key": "header_value"},
            params={"param_key": "param_value"},
            body={"key_1": "value_1", "key_2": "value_2"},
        )
        request_obj = AWSRequestFromEvents(**fake_data)
        self.assertEqual(fake_data["body"], request_obj.get_json())

    def test_AWSRequestFromEvents_obj__string_passed_for_body__returns_json(self):
        expected = {"key_1": "value_1", "key_2": "value_2"}
        fake_data = dict(
            headers={"header_key": "header_value"},
            params={"param_key": "param_value"},
            body='{\"key_1": \"value_1", \"key_2": \"value_2"}',
        )
        request_obj = AWSRequestFromEvents(**fake_data)
        self.assertEqual(expected, request_obj.body)
