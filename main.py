from bs4 import BeautifulSoup
import requests

def get_url(position, location):
    '''Get the indeed url specific to that position and location'''
    raw = 'https://ca.indeed.com/jobs?q={}&l={}'
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    url = raw.format(position, location)
    return url

def getJobInfo(job, f):
    '''Get job information'''
    # title
    job_info = job.findAll('span')
    jobTitle = job_info[0].text
    if jobTitle == 'new':
        title = job_info[1].text
    else:
        title = jobTitle
    # company name
    company_name = job.find('span', class_='companyName').text
    # salary
    if job.find('span', class_='salary-snippet') != None:
        salary = job.find('span', class_='salary-snippet').text
    else:
        salary = 'None'
    # company location
    location = job.find('div', class_='companyLocation').text
    # urgency
    if job.find('div', class_='urgentlyHiring') != None:
        urgency = job.find('div', class_='urgentlyHiring').text
    else:
        urgency = 'None'
    # date posted
    date = job.find('span', class_='date').text
    # description
    description = job.find('div', class_='job-snippet')
    description = description.findAll('li')
    description = description[0].text

    # Write in csv
    f.write(title.replace(',', '|') + ',' + company_name.replace(',', '|') + ','
            + salary.replace(',', '|') + ',' + location.replace(',', '|') + ',' +
            urgency.replace(',', '|') + ',' + date.replace(',', '|') + ',' +
            description.replace(',', '|') + '\n')


def main(position, location):
    url = get_url(position, location)

    # Write headers of csv
    filename = "indeed_jobs.csv"
    f = open(filename, 'w')
    headers = 'title, company_name, salary, location, urgency, date_posted, job_description\n'
    f.write(headers)

    while True:
        indeed_data_job = requests.get(url)
        soup = BeautifulSoup(indeed_data_job.text, 'lxml')
        jobs = soup.findAll('div', class_='job_seen_beacon')

        for job in jobs:
            getJobInfo(job, f)

        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
        except AttributeError:
            break
    f.close()


if __name__ == "__main__":
    main('tutor', 'vancouver')

