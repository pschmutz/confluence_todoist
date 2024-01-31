from datetime import datetime
import logging
import tqdm
import json
import os
from confluence_todoist.confluence import Confluence, task_to_text
from confluence_todoist.todoist import TodoistConfluence
import os
import time
from dotenv import load_dotenv

def get_config():
    config = {}
    config["ATLASSIAN"] = {
        "URL": os.getenv("ATLASSIAN_URL"),
        "USERNAME": os.getenv("ATLASSIAN_USERNAME"),
        "API_TOKEN": os.getenv("ATLASSIAN_API_TOKEN"),
        "USER_ID": os.getenv("ATLASSIAN_USER_ID"),
    }
    config["TODOIST"] = {
        "API_TOKEN": os.getenv("TODOIST_API_TOKEN"),
        "PROJECT": os.getenv("TODOIST_PROJECT"),
        "SECTION": os.getenv("TODOIST_SECTION"),
    }
    return config

def sync_confluence_todoist(since):
    since_timestamp = since.timestamp()
    config = get_config()

    confluence = Confluence.from_config(config["ATLASSIAN"])
    todoist = TodoistConfluence.from_config(config["TODOIST"])

    logging.info("Getting tasks from Confluence")

    tasks = confluence.get_tasks(
        assigned_to=config["ATLASSIAN"]["USER_ID"],
        status="incomplete",
        body_format="atlas_doc_format",
        created_at_from=int(since_timestamp * 1000),
    )

    print(f"Got {len(tasks)} tasks from Confluence. Will now add them to Todoist.")

    for task in tasks:
        task_body = task["body"]["atlas_doc_format"]["value"]
        task_body_json = json.loads(task_body)
        task_text = task_to_text(task_body_json)
        page = confluence.get_page_by_id(task["pageId"])
        page_title = page["title"]
        page_link = page["_links"]["base"] + page["_links"]["webui"]
        full_task_text = f"{task_text} [{page_title}]({page_link})"
        print(f"IMPORTED: {full_task_text}")
        todoist.add_confluence_task(full_task_text)


if __name__ == "__main__":
    load_dotenv()
    sync_confluence_todoist(datetime(2023, 1, 30))
