#!/usr/bin/env python3
import dvc_pandas
import pandas as pd

# import logging
# logging.basicConfig(level=logging.DEBUG)

BAU_HISTORICAL_UNTIL_YEAR = 2018


def extract_scenario(df, scenario):
    df_scenario = df[df.Scenario == scenario].copy()
    df_scenario['Forecast'] = df_scenario['Year'] > BAU_HISTORICAL_UNTIL_YEAR
    df_scenario = df_scenario.set_index('Year').drop(columns=['Scenario'])
    return df_scenario


def store(df, identifier):
    repo = dvc_pandas.Repository(repo_url='git@github.com:kausaltech/dvctest.git', dvc_remote='kausal-s3')
    repo.pull_datasets()
    dataset = dvc_pandas.Dataset(df, identifier)
    repo.push_dataset(dataset)


df = pd.read_excel('Scenario tool structure and content.xlsx', sheet_name='Emissions', header=2)
for scenario in ('BAU', 'diff'):
    df_scenario = extract_scenario(df, scenario)
    store(df_scenario, f'tampere/scenarios/emissions/{scenario.lower()}')


df = pd.read_excel('Scenario tool structure and content.xlsx', sheet_name='Emission factors', header=2)
for scenario in ('BAU',):
    df_scenario = extract_scenario(df, scenario)
    store(df_scenario, f'tampere/scenarios/emission_factors/{scenario.lower()}')


df = pd.read_excel('Scenario tool structure and content.xlsx', sheet_name='Activity', header=2)
for scenario in ('BAU',):
    df_scenario = extract_scenario(df, scenario)
    store(df_scenario, f'tampere/scenarios/activity/{scenario.lower()}')
