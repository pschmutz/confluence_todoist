from todoist_api_python.api import TodoistAPI
from dotenv import load_dotenv
from os import getenv


class TodoistConfluence(TodoistAPI):
    def __init__(self, token, project_name, section_name):
        super().__init__(token)

        self.project_id = self.get_project_id(project_name)
        self.section_id = self.get_section_id(section_name)

    def get_section_id(self, section_name):
        sections = self.get_sections(project_id=self.project_id)
        for section in sections:
            if section.name == section_name:
                return section.id
        raise ValueError(f"Section {section_name} not found")

    def get_project_id(self, project_name):
        projects = self.get_projects()
        for project in projects:
            if project.name == project_name:
                return project.id
        raise ValueError(f"Project {project_name} not found")

    @classmethod
    def from_dotenv(cls):
        load_dotenv()
        todoist_api_token = getenv("TODOIST_API_TOKEN")
        return cls(
            token=todoist_api_token, project_name="Inbox", section_name="Confluence"
        )

    @classmethod
    def from_config(cls, config):
        return cls(
            token=config["todoist_api_token"],
            project_name=config["project_name"],
            section_name=config["section_name"],
        )

    def add_confluence_task(self, text):
        task = self.add_task(
            content=text,
            project_id=self.project_id,
            section_id=self.section_id,
        )
