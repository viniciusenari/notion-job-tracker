from notion_api import add_job_application
import datetime


def main():
    company_name = input("Company name: ")
    job_title = input("Job title (separated by commas if multiple): ").split(",")
    location = input("Location (separated by commas if multiple): ").split(",")
    job_posting_url = input("Job posting URL (optional): ")

    add_job_application(
        company_name=company_name,
        stage="Applied",
        job_title=[title.strip() for title in job_title],
        location=[loc.strip() for loc in location],
        application_date=datetime.date.today().isoformat(),
        last_update=None,
        job_posting_url=job_posting_url.strip() if job_posting_url else None,
    )


if __name__ == "__main__":
    main()
