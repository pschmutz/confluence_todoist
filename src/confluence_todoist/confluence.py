import logging
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from atlassian import Confluence


class Confluence(Confluence):
    @classmethod
    def from_dotenv(cls):
        load_dotenv("~/.config/confluence_todoist/.env")
        url = os.getenv("ATLASSIAN_URL")
        api_token = os.getenv("ATLASSIAN_API_TOKEN")
        username = os.getenv("ATLASSIAN_USERNAME")
        return cls(
            url=url,
            username=username,
            password=api_token,
            cloud=True,
        )

    @classmethod
    def from_config(cls, config):
        return cls(
            url=config["atlassian_url"],
            username=config["atlassian_username"],
            password=config["atlassian_api_token"],
            cloud=True,
        )

    def get_user(self):
        path = "rest/api/user/current"
        response = self.get(path)
        return response

    def get_tasks(
        self,
        body_format=None,
        include_blank_tasks=True,
        status=None,
        task_id=None,
        space_id=None,
        page_id=None,
        blogpost_id=None,
        created_by=None,
        assigned_to=None,
        completed_by=None,
        created_at_from=None,
        created_at_to=None,
        due_at_from=None,
        due_at_to=None,
        completed_at_from=None,
        completed_at_to=None,
        cursor=None,
    ):
        path = "api/v2/tasks"
        params = {}
        if body_format:
            params["body-format"] = body_format
        params["include-blank-tasks"] = include_blank_tasks
        if status:
            params["status"] = status
        if task_id:
            params["task-id"] = task_id
        if space_id:
            params["space-id"] = space_id
        if page_id:
            params["page-id"] = page_id
        if blogpost_id:
            params["blogpost-id"] = blogpost_id
        if created_by:
            params["created-by"] = created_by
        if assigned_to:
            params["assigned-to"] = assigned_to
        if completed_by:
            params["completed-by"] = completed_by
        if created_at_from:
            params["created-at-from"] = created_at_from
        if created_at_to:
            params["created-at-to"] = created_at_to
        if due_at_from:
            params["due-at-from"] = due_at_from
        if due_at_to:
            params["due-at-to"] = due_at_to
        if completed_at_from:
            params["completed-at-from"] = completed_at_from
        if completed_at_to:
            params["completed-at-to"] = completed_at_to
        if cursor:
            params["cursor"] = cursor
        params["limit"] = 250
        response = self.get(path, params=params)
        return response["results"]


def task_to_md(task):
    content = task.get("content")

    if not content:
        logging.warning(f"Task {task} has no content")
        return ""

    text = ""
    for item in content:
        paragraph = item.get("content")
        if not paragraph:
            continue

        for element in paragraph:
            etype = element["type"]
            if etype == "mention":
                text += element["attrs"].get("text", "")
            elif etype == "inlineCard":
                text += element["attrs"].get("url", "")
            elif etype == "text":
                link = ""
                for mark in element.get("marks", []):
                    if mark["type"] == "link":
                        link = mark["attrs"].get("href", "")
                if link:
                    text += f"[{element['text']}]({link})"
                else:
                    text += element["text"]
    return text
