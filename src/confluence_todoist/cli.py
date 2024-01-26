import tqdm
import json
import click
import os
from dotenv import load_dotenv
from confluence_todoist.confluence import Confluence, task_to_text
from confluence_todoist.todoist import TodoistConfluence
import os
import time


def atlassian_user_id_from_dotenv():
    load_dotenv()
    return os.getenv("ATLASSIAN_USER_ID")


def get_timestamp(since):
    if since:
        since_timestamp = int(since.timestamp())
    else:
        last_execution_file = os.path.expanduser(
            "~/.config/confluence_todoist/timestamp"
        )
        if os.path.exists(last_execution_file):
            with open(last_execution_file, "r") as file:
                since_timestamp = int(file.read().strip())
        else:
            since_timestamp = 0

    return since_timestamp


def save_timestamp():
    last_execution_file = os.path.expanduser(
        "~/.config/confluence_todoist/timestamp"
    )

    os.makedirs(os.path.dirname(last_execution_file), exist_ok=True)

    timestamp = int(time.time())

    with open(last_execution_file, "w") as file:
        file.write(str(timestamp))


@click.command()
@click.option("--since", type=click.DateTime(), help="since when to get tasks")
def main(since):
    since_timestamp = get_timestamp(since)

    confluence = Confluence.from_dotenv()
    todoist = TodoistConfluence.from_dotenv()

    tasks = confluence.get_tasks(
        assigned_to=atlassian_user_id_from_dotenv(),
        status="incomplete",
        body_format="atlas_doc_format",
        created_at_from=since_timestamp * 1000,
    )

    print(f"Got {len(tasks)} tasks from Confluence. Will now add them to Todoist.")

    for task in tqdm.tqdm(tasks):
        task_body = task["body"]["atlas_doc_format"]["value"]
        task_body_json = json.loads(task_body)
        task_text = task_to_text(task_body_json)
        page = confluence.get_page_by_id(task["pageId"])
        page_title = page["title"]
        page_link = page["_links"]["base"] + page["_links"]["webui"]
        full_task_text = f"{task_text} [{page_title}]({page_link})"
        tqdm.tqdm.write(full_task_text)
        todoist.add_confluence_task(full_task_text)
    save_timestamp()


if __name__ == "__main__":
    main()
