from google.auth.transport.requests import Request
from google.oauth2 import service_account

key_path = "C:\\Users\\akash\\Downloads\\faqtranslate-449517-3da377db3057.json"
credentials = service_account.Credentials.from_service_account_file(key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"])
credentials.refresh(Request())
access_token = credentials.token
print(f"Access Token: {access_token}")
