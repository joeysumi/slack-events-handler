from flask import request

from callback_functions import slack_events_url_endpoint_google_cloud_function, slack_events_url_endpoint_aws_lambda


def slack_events_callback_factory(*args):
    if isinstance(args[0], request):
        return slack_events_url_endpoint_google_cloud_function(*args)
    else:
        return slack_events_url_endpoint_aws_lambda(*args)
