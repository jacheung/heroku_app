import streamlit as st
from scipy import stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():

    """
    # Structure Research - Singapore February 2020 Newsletter
    ### A dynamic data visualization newsletter for our customers.
    """

    sum_df = pd.read_pickle('/Users/jonathancheung/Documents/GitHub/heroku_app/Dataframes/singapore_sum_df')
    map_df = pd.read_pickle('/Users/jonathancheung/Documents/GitHub/heroku_app/Dataframes/singapore_map_df')
    ranking_df = pd.read_pickle('/Users/jonathancheung/Documents/GitHub/heroku_app/Dataframes/singapore_rank_df')


    '##  Map of online data centers'
    years_to_observe = st.slider('Year to view ', 2000, 2030, 2000)
    '##### note that year 2000 datapoint is for clients who have not disclosed their online dates'
    map_data = map_df.loc[map_df['year built'] <= years_to_observe, ['latitude', 'longitude']]
    map_data = map_data[pd.to_numeric(map_data.iloc[:, 0], errors='coerce').notnull()] #selecting only non empty datapoints
    stats.zscore(np.array(map_data['latitude'], dtype=np.float64))
    map_data = map_data[stats.zscore(np.array(map_data['latitude'], dtype=np.float64)) < 1] # removing outlier points due to localization error
    st.map(map_data)

    eval_years = np.linspace(2000, 2030, 7)
    num_data_centers = np.zeros((len(eval_years), 1))
    for i in range(len(eval_years)):
        num_data_centers[i] = len(map_df.loc[map_df['year built'] <= eval_years[i]])

    plt.plot(eval_years, num_data_centers)
    plt.xlabel('Year')
    plt.ylabel('Number of data centers')
    plt.title('Singapore datacenters across time')
    st.pyplot()

    if st.checkbox('Show dataframe for all data centers'):
        map_df

    """
    ## Three metrics of internet infrastructure market
    #### Revenue - total revenue generated by all companies in USD
    #### Power - power consumption via MW
    #### Space - square footage (Sqft) or racks in servers (Rack)
    """
    sum_packets = {}
    sum_packets['Revenue'] = sum_df[['WS Rev', 'Retail Rev', 'Colocation Revenue']]
    sum_packets['Power'] = sum_df[['Contracted MW', 'Critical MW']]
    sum_packets['Space - Sqft'] = sum_df[['Utilized Rack sqft.',  'Rack sqft.']]
    sum_packets['Space - Rack'] = sum_df[['Racks Leased',  'Rack Capacity']]

    feature = st.selectbox('select feature to observe', list(sum_packets.keys()))
    sum_packets[feature].plot(kind='bar')
    plt.xlabel('year')
    plt.ylabel(feature)
    plt.tight_layout()
    st.pyplot()

    """
    ## Market dominance (revenue) across years
    #### Below is a CDF of revenue generated by each company. Click a year to view!
    """
    columns = st.multiselect(
        label='Which years to view?', options=ranking_df.columns.to_list(), default=[2015, 2020, 2025])
    plt.plot(ranking_df[columns])
    plt.xlabel('companies sorted by revenue generated')
    plt.ylabel('proportion of total revenue (USD)')
    plt.legend(columns)
    plt.tight_layout()
    st.pyplot()
    #  st.line_chart(ranking_df[columns])


if __name__ == '__main__':
    main()



