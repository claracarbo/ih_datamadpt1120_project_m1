import pandas as pd


def group_function(df_merged):
    print("Grouping by Country, Job Title and Age...")
    grouped = df_merged.groupby(["Country_code","Country", "Job Title", "Age"], as_index=False).count()
    print("Calculating Percentages for each group...")
    grouped["Percentage"] = grouped["Quantity"].apply(lambda qty:str((qty * 100 / grouped["Quantity"].sum()).round(2))+"%")
    grouped.to_csv(f"/Users/claracarbo/Desktop/Bootcamp/ih_datamadpt1120_project_m1/results/all_countries.csv", index=False)
    print("New csv named all_countries created in the results directory!")
    return grouped


def export_by_country(final_df, country):
    list_countries = final_df["Country"].unique().tolist()
    if country in list_countries:
        final_df_by_country = final_df[final_df["Country"] == f'{country}']
        print("Exporting final csv by country")
        final_df_by_country.to_csv(f'../results/data_{country}.csv', index=False)
        return final_df_by_country