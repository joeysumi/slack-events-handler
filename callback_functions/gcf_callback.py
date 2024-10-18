import functions_framework

from callback_functions import slack_events_receive_callback


@functions_framework.http
def slack_events_url_endpoint_google_cloud_function(request):
    """HTTP Cloud Function for Google Cloud Function
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    return slack_events_receive_callback(request)
