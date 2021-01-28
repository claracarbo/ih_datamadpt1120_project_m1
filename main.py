import argparse
from p_acquisition import m_acquisition as mac
from p_wrangling import m_wrangling as mwr
from p_analysis import m_analysis as man


def argument_parser():
    parser = argparse.ArgumentParser(description="Indicate path...")
    parser.add_argument("-p", "--path", type=str, help="Indicate path", required=True)
    parser.add_argument("-u", "--url", type=str, help="Indicate url", required=True)
    #parser.add_argument("-c", "--country", type=str, help="Indicate Country", required=True)
    args = parser.parse_args()
    return args


def main(arguments):
    print("Starting project...")
    data_base = mac.raw_data(arguments.path)
    df_countries = mac.get_country_codes(arguments.url)
    jobs = mac.job_id(data_base)
    df_jobs_api = mac.get_jobs_api(jobs)
    df = mwr.clean_age(data_base)
    df_merged = mwr.merged_data(df_countries, df, df_jobs_api)
    final_df = man.group_function(df_merged)
    final_df_by_country = man.export_by_country(final_df, country)
    print("Project finished successfully :)")


if __name__ == "__main__":
    arguments = argument_parser()
    main(arguments)