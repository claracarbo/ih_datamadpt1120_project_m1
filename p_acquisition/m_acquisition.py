import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from sqlalchemy import create_engine
import lxml


# Importing data base
def raw_data(path):
    print("Taking data from data base...")
    db_path = path
    conn_str = f'sqlite:///{db_path}'
    engine = create_engine(conn_str)
    table_query = """SELECT personal_info.uuid, country_info.country_code, 
    career_info.normalized_job_code, 
    personal_info.age
    FROM personal_info
    JOIN career_info ON personal_info.uuid = career_info.uuid
    JOIN country_info ON personal_info.uuid = country_info.uuid
    JOIN poll_info ON personal_info.uuid = poll_info.uuid
    """
    df = pd.read_sql_query(table_query, engine)
    return df


def job_id(df):
    jobs_id = list(df.normalized_job_code.unique())
    print("Taking the job id...")
    return jobs_id


# Api function
def get_jobs_api(jobs_id):
    print("Connecting to Api...")
    jobs_api = []
    for i in jobs_id:
        response = requests.get(f'http://api.dataatwork.org/v1/jobs/{i}')
        jobs_json = response.json()
        jobs_api.append(jobs_json)

    jobs = pd.DataFrame(jobs_api)
    jobs = jobs.rename(columns={"uuid": "normalized_job_code"})
    df_jobs_api = jobs[["normalized_job_code","title","normalized_job_title" ]]
    return df_jobs_api


# Web Scraping function

def get_country_codes(url):
    print("Web scraping...")
    r = requests.get(url).content
    soup = bs(r, "lxml")
    table = soup.find("table")
    list_ok = []
    table_rows = table.find_all("tr")
    for tr in table_rows:
        element = tr.find_all("td")
        for td in element:
            list_ok.append(td.text)
    country_list = []
    for i in list_ok:
        f = i.replace('\n', '').replace('(', '').replace(')', '')
        country_list.append(f)
    row_split = 2
    rows_refactored = [country_list[x:x + row_split] for x in range(0, len(country_list), row_split)]
    df_countries = pd.DataFrame(rows_refactored, columns={"country_name", "country_code"})
    df_countries["country_code"].replace({"EL": "GR"}, inplace=True)
    return df_countries



