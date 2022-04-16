import pytest

from target_google_people.google_people_service import GooglePeopleService


class TestGooglePeopleService:

    def test_add_contact(self):
        gps = GooglePeopleService()
        example_contact = {
            "first_name": "Jack",
            "last_name": "Sparrow",
            "email_address": "jack@sparrow.com",
            "contact_group_name": "Test"
        }
        created_contact = gps.create_contact(**example_contact)
        fetched_contact = gps.get_contact(resource_name=created_contact["resourceName"])
        assert (
            created_contact["names"] == fetched_contact["names"]
        )
        assert (
            created_contact["emailAddresses"] == fetched_contact["emailAddresses"]
        )
        assert (
            created_contact["memberships"] == fetched_contact["memberships"]
        )
        gps.delete_contact(resource_name=fetched_contact["resourceName"])

    def test_upsert_contact(self):
        gps = GooglePeopleService()
        example_contact = {
            "first_name": "Captain",
            "last_name": "Sparrow",
            "email_address": "jack@sparrow.com",
            "contact_group_name": "TestChanged"
        }
        upserted_contact = gps.upsert_contact(**example_contact)
        assert True
