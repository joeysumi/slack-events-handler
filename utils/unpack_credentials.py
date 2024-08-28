import json


def get_credential_list(path: str) -> dict:
    with open(path, "r") as cred_file:
        credentials = json.load(cred_file)

    return credentials


def get_app_credentials(app_id: str, path: str) -> dict | None:
    credential_list = get_credential_list(path)
    app_credentials = [credentials for credentials in credential_list if app_id == credentials["slack_app_id"]]
    if app_credentials:
        return app_credentials[0]

