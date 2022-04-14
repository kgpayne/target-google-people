"""Class to interact with the Google People API.

https://developers.google.com/resources/api-libraries/documentation/people/v1/python/latest/index.html
"""
from pathlib import Path
from pprint import pprint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/contacts'
]


class GooglePeopleService:

    def __init__(self, client_secrets_path=None, token_path=None):
        self.client_secrets_path = (
            Path(client_secrets_path) if client_secrets_path
            else Path("client_secrets.json").resolve()
        )
        self.token_path = (
            Path(token_path) if token_path
            else Path("token.json").resolve()
        )
        self.service = self.get_people_service()

    def get_credentials(self):
        """Get credentials to access the Google People API."""
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.client_secrets_path), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        return creds

    def get_people_service(self):
        credentials = self.get_credentials()
        return build('people', 'v1', credentials=credentials)

    def list_contact_groups(self):
        contact_groups = []
        request = self.service.contactGroups().list()
        response = request.execute()
        contact_groups.extend(response.get('contactGroups', []))
        while response.get("nextPageToken"):
            request = (
                self.service.contactGroups().list_next(
                    previous_request=request,
                    previous_response=response
                )
            )
            response = request.execute()
            contact_groups.extend(response.get("contactGroups", []))
        return contact_groups

    def get_contact_group(self, name=None, resource_name=None):
        if not resource_name:
            contact_groups = self.list_contact_groups()
            found = None
            for contact_group in contact_groups:
                if contact_group["name"] == name:
                    found = contact_group
            return found
        else:
            return (
                self.service.contactGroups()
                .get(resourceName=resource_name)
                .execute()
            )

    def create_contact_group(self, name, exists_ok=True):
        contact_group = self.get_contact_group(name=name)
        if contact_group:
            if exists_ok:
                return contact_group
            else:
                raise KeyError(
                    f"Contact Group called '{name}' already exists."
                )
        else:
            body = {  # A request to create a new contact group.
                "contactGroup": {  # A contact group. # Required. The contact group to create.
                    "name": name,  # The contact group name set by the group owner or a system provided name
                }
            }
            response = self.service.contactGroups().create(body=body).execute()
            return response

    def delete_contact_group(self, name, not_exists_ok=True):
        contact_group = self.get_contact_group(name=name)
        if contact_group:
            response = (
                self.service.contactGroups()
                .delete(resourceName=contact_group["resourceName"])
                .execute()
            )
            return response
        else:
            if not_exists_ok:
                return {}
            else:
                raise KeyError(
                    f"Contact Group called '{name}' does not exist."
                )

    def create_contact(self, first_name, last_name, email_address, contact_group_name=None):
        contact_group = self.get_contact_group(name=contact_group_name)
        if not contact_group:
            contact_group = self.create_contact_group(name=contact_group_name)
        body = {
            "names": [
                {
                    "givenName": first_name,
                    "familyName": last_name,
                }
            ],
            "emailAddresses": [
                {
                    "value": email_address
                }
            ]
        }
        if contact_group_name:
            resource_name = contact_group.get("resourceName")
            body["memberships"] = [
                {
                    "contactGroupMembership": {
                        "contactGroupResourceName": resource_name
                    }
                }
            ]
        return self.service.people().createContact(body=body).execute()

    def list_contacts(self):
        contacts = []
        request = (
            self.service.people().connections()
            .list(
                resourceName="people/me",
                personFields="names,addresses,memberships"
            )
        )
        response = request.execute()
        contacts.extend(response.get('connections', []))
        while response.get("nextPageToken"):
            request = (
                self.service.people().connections()
                .list_next(
                    previous_request=request,
                    previous_response=response
                )
            )
            response = request.execute()
            contacts.extend(response.get("connections", []))
        return contacts
