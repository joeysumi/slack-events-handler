from callback_functions import slack_events_receive_callback


class AWSRequestFromEvents:
    """ Mimics flask.request in such a way that 'slack_events_receive_callback' understands
    """

    def __init__(self, *, headers=None, params=None, body=None):
        self.headers = headers
        self.params = params
        self.body = body

    def get_json(self, *args):
        return self.body


def slack_events_url_endpoint_aws_lambda(event, context):
    headers = event.get("headers")
    params = event.get("queryStringParameters")
    body = event.get("body")
    request = AWSRequestFromEvents(headers=headers, params=params, body=body)
    return slack_events_receive_callback(request)
