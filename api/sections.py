import logging
import unittest

import requests

from api.todo_base import TodoBase
from api.validate_response import ValidateResponse
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Sections(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url_section = "https://api.todoist.com/rest/v2/sections"
        cls.session = requests.Session()

        cls.project_id = TodoBase().get_all_projects().json()[1]["id"]
        """cls.section_id_update = ""
        cls.sections_list = []"""
    def test_create_session(self):
        """
        Test to create session
        :return:
        """
        data = {
            "project_id": self.project_id,
            "name": "Section 2"
        }
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_section, data=data)
        assert response.status_code == 200
    def test_get_all_sections(self):
        """
        Test to get all sections
        :return:
        """
        response = RestClient().send_request(method_name="get", session=self.session,
                                             url=self.url_section, headers=HEADERS)
        LOGGER.info("Number of sections returned: %s", len(response.json()))
        assert response.status_code == 200

    def test_get_all_sections_by_project(self):
        """
        Test to get all sections by project id
        :return:
        """
        if self.project_id:
            url_section = f"{self.url_section}?project_id={self.project_id}"

        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        LOGGER.info("Number of sections returned: %s", len(response.json()))
        assert response.status_code == 200

    def test_get_section(self):
        response = TodoBase().get_all_sections()
        section_id = response.json()[0]["id"]
        LOGGER.info("Section Id: %s", section_id)
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_section)
        assert response.status_code == 200

    def test_update_section(self):
        """
            Test to update a Section
        :return:
        """
        data = {
            "project_id": self.project_id,
            "name": "Edited Section2"
        }
        response = TodoBase().get_all_sections()
        section_id = response.json()[0]["id"]
        LOGGER.info("Section Id: %s", section_id)
        url_section = f"{self.url_section}/{section_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_section, data=data)
        assert response.status_code == 200


    def test_delete_session(self):
        """
        Test to delete session
        :return:
        """
        response = RestClient().send_request("delete", session=self.session,
                                                 url=self.url_section,
                                                 headers=HEADERS)
        assert response.status_code == 204
