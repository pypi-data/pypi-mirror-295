import json
import boto3
import boto3.session
from botocore.exceptions import ClientError


class SecretsFetcher:
    def __init__(self):
        region_name = "us-east-1"
        session = boto3.session.Session()
        self.client = session.client(
            service_name="secretsmanager", region_name=region_name
        )

    def get_db_creds(self, db_env: str):
        secret_name = (
            "rds!db-16a90c6b-d685-4667-a32f-5c3aff6a2d41"
            if db_env == "dev"
            else "Invalid environment"
        )

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        secret = json.loads(get_secret_value_response["SecretString"])
        return secret.get("username"), secret.get("password")

    def get_email_creds(self):
        secret_name = "anybyte/auto-email/credentials"

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        secret = json.loads(get_secret_value_response["SecretString"])
        return secret

    def get_google_oauth_id(self):
        secret_name = "anybyte/google/oauth/clientid"

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        secret = json.loads(get_secret_value_response["SecretString"])
        return secret.get("client_id")

    def get_gemini_api_key(self):
        secret = "anybyte/llm_api_keys"

        try:
            get_secret_value_response = self.client.get_secret_value(SecretId=secret)
        except ClientError as e:
            raise e

        secret = json.loads(get_secret_value_response["SecretString"])
        return secret.get("gemini_api_key")
