import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import date

today = date.today()
print("Today's date:", today)

url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Python%20Developer&location=United%20States"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

job_postings_html = soup.find_all("li")

job_ids = []

jobs = []

for job in job_postings_html:
    base_card_div = job.find("div", {"class" : "base-card"})
    job_id = base_card_div.get("data-entity-urn").split(":")[3]
    job_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    job_response = requests.get(job_url)
    if job_response.status_code == 200:
        job_soup = BeautifulSoup(job_response.text, "html.parser")
        entry = {}
        
        job_title = job_soup.find("h2", {"class" : "top-card-layout__title"}).text      # Job Title
        
        a_tag = job_soup.find("a", {"class" : "topcard__link"})
        job_link = a_tag.get("href")                                                    # Job Link
        
        company_name = job_soup.find("a", {"class" : "topcard__org-name-link"}).text.strip(' \n\t')    # Company Name
        
        location = job_soup.find("span", {"class" : "topcard__flavor topcard__flavor--bullet"}).text.strip(' \n\t') # Location
        
        salary = job_soup.find("div", {"class" : "salary compensation__salary"})        # Assigns Salary to salary_text
        if salary:
            salary_text = salary.text.strip(' \n\t')
        else:
            salary_text = "None provided"
        
        posted_time = job_soup.find("span", {"class" : "posted-time-ago__text"}).text.strip(' \n\t')    # Posted Time

        num_applicants = job_soup.find("figcaption", {"class" : "num-applicants__caption"})     # Assigns # of Applicants to num_applicants_text
        if num_applicants:
            num_applicants_text = num_applicants.text.strip(' \n\t')
        else:
            num_applicants_text =  "None provided"
        
        entry["Company Name"] = company_name
        entry["Job Title"] = job_title
        entry["Location"] = location
        entry["Salary"] = salary_text
        entry["Posted Time"] = posted_time
        entry["# of Applicants"] = num_applicants_text
        entry["Job Link"] = job_link

        jobs.append(entry)

    time.sleep(0.3)

df = pd.DataFrame(jobs)

df.to_csv(f"JobPosting_{today}.csv", mode="w", index=False)