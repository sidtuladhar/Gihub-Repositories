import pandas as pd
import streamlit as st


@st.cache_data(show_spinner="Loading Data...")
def load_data(url):
    data = pd.read_csv(url, usecols=['name', 'created_at', 'licence', 'primary_language', 'stars_count', 'forks_count', 'commit_count', 'pull_requests'])
    return data


if __name__ == '__main__':
    st.title('Github Repositories Data Dashboard')
    st.subheader('By Sid Tuladhar')
    st.divider()

    repo = load_data('data/repository_data.csv')
    col1, col2, col3, col4 = st.columns(4)
    total = repo.shape[0]
    col1.metric('Total Repositories', total)
    col2.metric('Total Languages', repo['primary_language'].nunique())
    col3.metric('Total Licenses', repo['licence'].nunique())
    col4.download_button('Download Data', 'data/repository_data.csv')

    # st.header('Top 10 Most Frequently Used Programming Language on Github')
    # st.bar_chart(repo['primary_language'].value_counts().head(10), color='#eba715')

    st.header('Popularity of the Top 5 Most Used Programming Languages Over Time')
    top_5_lang = repo['primary_language'].value_counts().head(5).index
    top_5_lang_df = (
        repo.loc[repo['primary_language'].isin(top_5_lang)]
        .assign(year=repo['created_at'].str[:4])
        .query('year != "2023"')
        .groupby(['year', 'primary_language'])
        .size()
        .reset_index(name='count')
        .pivot(index='year', columns='primary_language', values='count')
    )
    st.line_chart(top_5_lang_df)

    st.header('Top 10 Most Starred Repositories')
    st.bar_chart(repo[['name', 'stars_count', 'commit_count']]
                 .sort_values('stars_count', ascending=False)
                 .head(10).set_index('name'),
                 y=['stars_count', 'commit_count'])
    #
    # st.header('Top 10 Most Forked Repositories')
    # st.bar_chart(repo[['name', 'forks_count', 'pull_requests']]
    #              .sort_values('forks_count', ascending=False)
    #              .head(10).set_index('name'),
    #              y=['forks_count', 'pull_requests'])
    #
    # st.header('Top 5 Most Used Licenses')
    # top_5_licenses = repo['licence'].value_counts().head(5)
    # st.bar_chart(top_5_licenses, color='#eba715')
    #
    # st.header('Popularity of the Top 5 Most Used Licenses')
    #
    # top_5_licenses_df = (
    #     repo.loc[repo['licence'].isin(top_5_licenses.index)]
    #     .assign(year=repo['created_at'].str[:4])
    #     .query('year != "2023"')
    #     .groupby(['year', 'licence'])
    #     .size()
    #     .reset_index(name='count')
    #     .pivot(index='year', columns='licence', values='count')
    # )
    # st.line_chart(top_5_licenses_df)

    tab1, tab2 = st.tabs(['Yearly', 'Monthly'])
    with tab1:
        st.header('Number of Repositories Made in Each Year')
        repo.loc[:, 'year'] = repo['created_at'].str[:4]
        year_data = repo['year'].value_counts().sort_index()
        st.bar_chart(year_data, color='#ff9a47')
    with tab2:
        st.header("Number of Repositories Made in Each Month")
        repo.loc[:, 'month'] = repo['created_at'].str[5:7]
        month_data = repo['month'].value_counts().sort_index()
        st.bar_chart(month_data, color='#ff4747')
