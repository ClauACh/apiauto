"""
(c) Copyright Jalasoft. 2023

tasks.py
    tests for tasks
"""
import logging
import unittest

import requests

from api.todo_base import TodoBase
from api.validate_response import ValidateResponse
from config.config import HEADERS
from utils.logger import get_logger
from utils.rest_client import RestClient

LOGGER = get_logger(__name__, logging.DEBUG)


class Tasks(unittest.TestCase):
    """
    Class for tasks endpoint
    """
    @classmethod
    def setUpClass(cls):
        cls.url_tasks = "https://api.todoist.com/rest/v2/tasks"
        cls.session = requests.Session()

        cls.project_id = TodoBase().get_all_projects()["body"][1]["id"]
        cls.section_id = TodoBase().get_all_sections()["body"][1]["id"]
        cls.task_id = TodoBase().get_all_tasks()["body"][1]["id"]

    def test_create_task(self):
        """
        Test create a task
        :return:
        """
        response = self.create_task()
        ValidateResponse().validate_response(actual_response=response, method="post",
                                             expected_status_code=200,
                                             feature="task")

    def test_create_task_with_project_id(self):
        """
        Test to create a task in a project
        :return:
        """
        project_id = self.project_id
        response = self.create_task(project_id=project_id)
        ValidateResponse().validate_response(actual_response=response, method="post",
                                             expected_status_code=200,
                                             feature="task")

    def test_create_task_with_section_id(self):
        """
        Test to create a task in a section
        :return:
        """
        section_id = self.section_id
        response = self.create_task(section_id=section_id)
        ValidateResponse().validate_response(actual_response=response, method="post",
                                             expected_status_code=200,
                                             feature="task")

    def test_get_all_tasks(self):
        """
        Test to get all the tasks
        :return:
        """
        response = TodoBase().get_all_tasks()
        LOGGER.info("Number of tasks returned: %s", len(response["body"]))
        ValidateResponse().validate_response(actual_response=response, method="get",
                                             expected_status_code=200,
                                             feature="tasks")

    def test_get_task_by_id(self):
        """
        Test to get a task by id
        :return:
        """
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)
        url_task = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("get", session=self.session, headers=HEADERS,
                                             url=url_task)

        ValidateResponse().validate_response(actual_response=response, method="get",
                                             expected_status_code=200,
                                             feature="task")

    def test_close_task(self):
        """
        Test to close a task
        :return:
        """
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)
        url_task_close = f"{self.url_tasks}/{task_id}/close"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_close)

        ValidateResponse().validate_response(actual_response=response, method="close",
                                             expected_status_code=204,
                                             feature="task")

    def test_reopen_task(self):
        """
        Test of reopening a task
        :return
        """
        # valid task open
        task_id = self.create_task()["body"]["id"]

        # close
        url_task_close = f"{self.url_tasks}/{task_id}/close"
        response_close = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                                   url=url_task_close)

        # assert response_close.status_code == 204

        LOGGER.info("Task Id: %s", task_id)
        url_task_reopen = f"{self.url_tasks}/{task_id}/reopen"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task_reopen)

        ValidateResponse().validate_response(actual_response=response, method="reopen",
                                             expected_status_code=204,
                                             feature="task")

    def create_task(self, project_id=None, section_id=None):
        """
            Test for creating a task
        """
        data = {
            "content": "Task inside section",
            "due_string": "tomorrow at 12:00",
            "due_lang": "en",
            "priority": 4
        }
        if project_id:
            data["project_id"] = project_id
        if section_id:
            data["section_id"] = section_id

        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=self.url_tasks, data=data)

        return response

    def test_update_task(self):
        """
            Test to update a Task
        :return:
        """
        data = {
            "content": "UPDATE task",
            "due_string": "tomorrow at 12:00",
            "due_lang": "en",
            "priority": 4
        }
        response = TodoBase().get_all_tasks()
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)
        url_task = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("post", session=self.session, headers=HEADERS,
                                             url=url_task, data=data)

        ValidateResponse().validate_response(actual_response=response, method="post",
                                             expected_status_code=200, feature="task")

    def test_delete_task(self):
        """
        Test to delete session
        :return:
        """
        task_id = self.task_id
        LOGGER.info("Task Id: %s", task_id)
        url_task = f"{self.url_tasks}/{task_id}"
        response = RestClient().send_request("delete", session=self.session, url=url_task,
                                                 headers=HEADERS)
        ValidateResponse().validate_response(actual_response=response, method="delete",
                                             expected_status_code=204,
                                             feature="task")

    @classmethod
    def tearDownClass(cls):
        print("tearDown Class")
