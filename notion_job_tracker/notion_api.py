import os
import requests
from typing import List, Optional
from dotenv import load_dotenv
import datetime

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

    # data = {
    #     "parent": {"database_id": os.getenv("NOTION_DATABASE_ID", "")},
    #     "properties": {
    #         "Company": {
    #         "title": [
    #             {
    #                 "text": {
    #                     "content": "Company Name"
    #                 }
    #             }
    #         ]
    #     },
    #         "Stage": {"select": {"name": stage}},
    #         "Job title": {
    #             "multi_select": [{"name": job_title[i]} for i in range(len(job_title))]
    #         },
    #         "Location": {
    #             "multi_select": [{"name": location[i]} for i in range(len(location))]
    #         },
    #         "Application Date": {"date": {"start": application_date}},
    #         "Last Update": {"date": {"start": last_update}} if last_update else None,
    #         "Job Posting URL": {"url": job_posting_url},
    #     },
    # }

    data = {
        "parent": {"database_id": os.getenv("NOTION_DATABASE_ID", "")},
        "properties": {
            "Company": {"title": [{"text": {"content": "Company Name"}}]},
            "Stage": {"select": {"name": "Applied"}},
            "Job title": {
                "multi_select": [
                    {"name": "Software Engineer"},
                    {"name": "Frontend Developer"},
                ]
            },
            "Location": {
                "multi_select": [{"name": location[i]} for i in range(len(location))]
            },
            "Application Date": {"date": {"start": application_date}},
            "Last Update": {"date": {"start": last_update}} if last_update else {"date": {"start": application_date}},
            "Job Posting URL": {"url": job_posting_url},
        },
    }

    response = requests.post(
        "https://api.notion.com/v1/pages", headers=headers, json=data
    )

    print(response.text)