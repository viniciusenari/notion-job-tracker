from .notion_api import add_job_application, get_job_applications
import datetime


def cli():
    print("Welcome to the Notion Job Tracker CLI!")
    print("What do you want to do? (type the number)")
    print("1. Add a job application")
    print("2. View all job applications")

    choice = input("Choice: ")

    if choice == "1":
        company_name = input("Company name: ")
        job_title = input("Job title (separated by commas if multiple): ").split(",")
        location = input("Location (separated by commas if multiple): ").split(",")
        job_posting_url = input("Job posting URL (optional): ")

        response = add_job_application(
            company_name=company_name,
            stage="Applied",
            job_title=[title.strip() for title in job_title],
            location=[loc.strip() for loc in location],
            application_date=datetime.date.today().isoformat(),
            last_update=None,
            job_posting_url=job_posting_url.strip() if job_posting_url else None,
        )

        if response.status_code == 200:
            print("Job application successfully added!")
        else:
            print("Error adding job application. Please try again.")
            print(response.json())

    elif choice == "2":
        print("Viewing all job applications")
        print(get_job_applications())


if __name__ == "__main__":
    cli()
