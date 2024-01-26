from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
from os import getenv


class TodoistConfluence(TodoistAPI):
    def __init__(self, token):
        super().__init__(token)
        self.project_id = "2303950124"
        self.section_id = "146024349"

    @classmethod
    def from_dotenv(cls):
        load_dotenv()
        todoist_api_token = getenv("TODOIST_API_TOKEN")
        return cls(token=todoist_api_token)

    def add_confluence_task(self, text):
        task = self.add_task(
            content=text,
            priority=4,
            project_id=self.project_id,
            section_id=self.section_id,
        )
