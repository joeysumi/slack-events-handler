import functions_framework

from slack_event_handler import slack_event_callback


@functions_framework.http
def slack_events_url_endpoint(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    return slack_events_receive_callback(request)


def slack_events_receive_callback(request) -> dict:
    response = slack_event_callback(request)

    return response
