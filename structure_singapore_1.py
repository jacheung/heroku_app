import streamlit as st
from scipy import stats
import numpy as np
import pandas as pd


def main():

    sum_df = pd.read_pickle('/Users/jonathancheung/Documents/GitHub/heroku_app/Dataframes/singapore_sum_df')
    map_df = pd.read_pickle('/Users/jonathancheung/Documents/GitHub/heroku_app/Dataframes/singapore_map_df')
    ranking_df = pd.read_pickle('/Users/jonathancheung/Documents/GitHub/heroku_app/Dataframes/singapore_rank_df')

    """
    # Structure Research - Singapore 2020
    ### A dynamic data visualization tool for our customers:
    """
    '##  Map of online data centers'
    years_to_observe = st.slider('Year to view ', 2000, 2030, 2000)
    '##### note that year 2000 datapoint is for clients who have not disclosed their online dates'
    map_data = map_df.loc[map_df['year built'] <= years_to_observe, ['latitude', 'longitude']]
    map_data = map_data[pd.to_numeric(map_data.iloc[:, 0], errors='coerce').notnull()] #selecting only non empty datapoints
    stats.zscore(np.array(map_data['latitude'], dtype=np.float64))
    map_data = map_data[stats.zscore(np.array(map_data['latitude'], dtype=np.float64)) < 1] # removing outlier points due to localization error
    st.map(map_data)

    if st.checkbox('Show dataframe for all data centers'):
        map_df

    '## Three metrics of internet infrastructure market'
    sum_packets = {}
    sum_packets['Revenue'] = sum_df[['WS Rev', 'Retail Rev', 'Colocation Revenue']]
    sum_packets['Power'] = sum_df[['Contracted MW', 'Critical MW']]
    sum_packets['Space - Sqft'] = sum_df[['Utilized Rack sqft.',  'Rack sqft.']]
    sum_packets['Space - Rack'] = sum_df[['Racks Leased',  'Rack Capacity']]

    feature = st.selectbox('select feature to observe', list(sum_packets.keys()))
    sum_packets[feature].plot(kind='bar')
    st.pyplot()

    """
    ## Market dominance (revenue) across years
    #### Below is a CDF of revenue generated by each company. Click a year to view!
    """
    columns = st.multiselect(
        label='Which years to view?',options=ranking_df.columns)
    st.line_chart(ranking_df[columns])


if __name__ == '__main__':
    main()



