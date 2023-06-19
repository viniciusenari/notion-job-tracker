import os
import requests
from typing import List, Optional
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()


def add_job_application(
    company_name: str,
    stage: str,
    job_title: List[str],
    location: List[str],
    application_date: Optional[str],
    last_update: Optional[str],
    job_posting_url: str,
) -> None:
    headers = {
        "Authorization": "Bearer " + os.getenv("NOTION_API_KEY", ""),
        "Content-Type": "application/json",
        "Notion-Version": "2021-08-16",
    }

    data = {
        "parent": {"database_id": os.getenv("NOTION_DATABASE_ID", "")},
        "properties": {
            "Company": {"title": [{"text": {"content": company_name}}]},
            "Stage": {"select": {"name": stage}},
            "Position": {
                "multi_select": [{"name": job_title[i]} for i in range(len(job_title))]
            },
            "Location": {
                "multi_select": [{"name": location[i]} for i in range(len(location))]
            },
            "Application Date": {"date": {"start": application_date}},
            "Last Update": {"date": {"start": last_update}}
            if last_update
            else {"date": {"start": application_date}},
            "Posting URL": {"url": job_posting_url},
        },
    }

    response = requests.post(
        "https://api.notion.com/v1/pages", headers=headers, json=data
    )

    return response


def get_job_applications() -> None:
    payload = {"page_size": 100}
    headers = {
        "Authorization": "Bearer " + os.getenv("NOTION_API_KEY", ""),
        "Notion-Version": "2022-06-28",
        "content-type": "application/json",
    }

    response = requests.post(
        f'https://api.notion.com/v1/databases/{os.getenv("NOTION_DATABASE_ID", "")}/query',
        json=payload,
        headers=headers,
    )
    results = response.json()["results"]

    table_data = []

    for i in range(len(results)):
        row_properties = results[i]["properties"]
        row = [
            row_properties["Company"]["title"][0]["text"]["content"],
            row_properties["Stage"]["select"]["name"],
            [pos["name"] for pos in row_properties["Position"]["multi_select"]],
            [
                location["name"]
                for location in row_properties["Location"]["multi_select"]
            ],
            row_properties["Application Date"]["date"]["start"],
            row_properties["Last Update"]["date"]["start"]
            if row_properties["Last Update"]["date"]
            else "N/A",
        ]
        table_data.append(row)

    headers = [
        "Company",
        "Stage",
        "Position",
        "Location",
        "Application Date",
        "Last Update",
    ]

    return tabulate(table_data, headers=headers, tablefmt="pretty")
