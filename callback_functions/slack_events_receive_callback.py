import datetime as dt

from config import CREDENTIALS_PATH
from slack_api import SlackEventApiHandler
from slack_api.event_handler_factory import EventHandlerFactory
from utils.unpack_credentials import get_app_credentials


def slack_events_receive_callback(request) -> dict:
    headers = dict(request.headers)
    response = {}

    if not is_request_timestamp_valid(headers["x-slack-request-timestamp"]):
        response["status"] = "failed"
        response["message"] = "The request timestamp has expired."

    request_data = request.get_json(force=True)

    request_type = request_data.get("type")
    if request_type == "url_verification":
        response = SlackEventApiHandler.respond_to_url_verification(request_data)

    elif request_type == "event_callback":
        response = {"response": "received"}
        slack_app_id = request_data["api_app_id"]

        app_credentials = get_app_credentials(slack_app_id, CREDENTIALS_PATH)
        if app_credentials is None:  # no credentials match app_id
            response["status"] = "failed"
            response["message"] = "Slack app not registered in credentials."
        else:
            try:
                handler_factory = EventHandlerFactory()
                event_handler = handler_factory.create(**app_credentials)
                event_handler.handle_slack_event(request_data)
            except Exception as err:
                print(err)

    else:
        response = {"message": "Received no event type."}

    return {"statusCode": 200, "body": response}


def is_request_timestamp_valid(timestamp):
    return (int(timestamp) - int(dt.datetime.now().timestamp())) < 60 * 5
