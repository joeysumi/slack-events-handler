import datetime as dt

from . import SlackEventApiHandler


def slack_event_callback(request):
    headers = dict(request.headers)
    data = {}

    if not is_request_timestamp_valid(headers["X-Slack-Request-Timestamp"]):
        data["status"] = "failed"
        data["message"] = "The request timestamp has expired."

    request_data = request.get_json(force=True)

    request_type = request_data.get("type")

    event_handler = SlackEventApiHandler()

    if request_type == "url_verification":
        data = event_handler.respond_to_url_verification(request_data)
    elif request_type == "event_callback":
        data = {"response": "received"}
        try:
            event_handler.handle_slack_event(request_data)
        except Exception as err:
            print(err)
    else:
        data = {"message": "Received no event type."}

    print(data)


def is_request_timestamp_valid(timestamp):
    return (int(timestamp) - int(dt.datetime.now().timestamp())) < 60 * 5
