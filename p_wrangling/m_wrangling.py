import pandas as pd


def clean_age(df):
    print(" Cleaning Age column and updating Ages to 2020")
    age_ok = []
    for item in df['age']:
        if "years old" in item:
            age_ok.append(int(item[0:2]))
        elif len(item) >= 4:
            age_ok.append(2016 - int(item))

    df["age"] = age_ok
    # Now we need to update ages to 2020
    df["age"] = df["age"] + 4
    return df


def merged_data(df_countries, df, df_jobs_api):
    print("Merging all data frames...")
    merge1 = df.merge(df_countries, how="left", on="country_code")
    merge2 = merge1.merge(df_jobs_api, how="left", on="normalized_job_code")
    merge2["title"].fillna("No Job", inplace=True)
    merge3 = merge2[["country_code","country_name","title","age", "uuid"]]
    merge3.rename(columns={"country_code":"Country_code","country_name":"Country","title":"Job Title","age":"Age","uuid":"Quantity"},inplace=True)
    merge4 = pd.DataFrame(merge3)
    merge4.to_csv(f"/Users/claracarbo/Desktop/Bootcamp/ih_datamadpt1120_project_m1/data/merged_data.csv", index=False)
    return merge4
