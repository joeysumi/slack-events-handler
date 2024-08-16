import datetime as dt

import functions_framework

from slack_event_api_handler import SlackEventApiHandler

application_password = "BV3y bH2S 2Vmh 79bZ M10y mRlx"


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
    headers = dict(request.headers)
    data = {}

    if not is_request_timestamp_valid(headers["X-Slack-Request-Timestamp"]):
        data["status"] = "failed"
        data["message"] = "The request timestamp has expired."

    request_data = request.get_json(force=True)

    request_type = request_data.get("type")

    event_handler = SlackEventApiHandler(request_data)

    if request_type == "url_verification":
        data = event_handler.respond_to_url_verification()
    elif request_type == "event_callback":
        data = event_handler.handle_slack_event()
    else:
        data = {"message": "Received no event type."}

    print(data)

    return data


def is_request_timestamp_valid(timestamp):
    return (int(timestamp) - int(dt.datetime.now().timestamp())) < 60 * 5
