import pandas as pd
import streamlit as st

repo = pd.read_csv('data/repository_data.csv')

if __name__ == '__main__':
    st.title('Github Repositories Data Dashboard')
    st.subheader('By Sid Tuladhar')
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    total = repo.shape[0]
    col1.metric('Total Repositories', total)
    col2.metric('Total Languages', repo['primary_language'].nunique())
    col3.metric('Total Licenses', repo['licence'].nunique())
    col4.download_button('Download Data', 'data/repository_data.csv')
    st.header('Top 10 Most Frequently Used Programming Language')
    st.bar_chart(repo['primary_language'].value_counts().head(10))
    st.header('Top 10 Most Starred Repositories')
    st.bar_chart(repo[['name', 'stars_count']].sort_values('stars_count', ascending=False).head(10).set_index('name'))
    st.header('Top 5 Most Used Licenses')
    st.bar_chart(repo['licence'].value_counts().head(5))

