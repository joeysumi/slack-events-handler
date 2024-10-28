from callback_functions import slack_events_url_endpoint_google_cloud_function, slack_events_url_endpoint_aws_lambda


def slack_events_callback(*args):
    return slack_events_callback_factory(*args)


def slack_events_callback_factory(*args):
    if len(args) == 1:
        return slack_events_url_endpoint_google_cloud_function(*args)
    elif len(args) == 2:
        return slack_events_url_endpoint_aws_lambda(*args)
    else:  # more than two arguments returned
        raise NotImplementedError("Expected only one or two arguments passed.")
