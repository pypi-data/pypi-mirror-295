import boto3


def get_bearer_token(region_name, client_id, username, password, auth_flow="USER_PASSWORD_AUTH"):
    client = boto3.client('cognito-idp', region_name=region_name)
    resp = client.initiate_auth(
        ClientId=client_id,
        AuthFlow=auth_flow,
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password}
    )
    return resp
