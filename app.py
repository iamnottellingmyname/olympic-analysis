import streamlit as st
import pandas as pd
import  preprocessor,calculations
import plotly.express as px
import plotly.figure_factory as ff

df=pd.read_csv(r'https://raw.githubusercontent.com/iamnottellingmyname/olympic-analysis/master/athlete_events.csv')
region_df=pd.read_csv(r'https://raw.githubusercontent.com/iamnottellingmyname/olympic-analysis/master/noc_regions.csv')

st.sidebar.image("https://stillmed.olympics.com/media/Images/OlympicOrg/IOC/The_Organisation/The-Olympic-Rings/Olympic_rings_TM_c_IOC_All_rights_reserved_1.jpg?im=Resize=(600,250),aspect=fill")
st.sidebar.title('Olympic Analysis')
selected_season=st.sidebar.selectbox("Select Season",['Overall','Summer','Winter'])
df=preprocessor.preprocess(df,region_df,selected_season)
user_menu=st.sidebar.radio('Select an Option',
                 ('Medal Tally','Overall Analysis','Country wise Analysis','Athelete wise Analysis'))


if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    countries,years=calculations.country_year(df)
    selected_country=st.sidebar.selectbox('Select Country',countries)
    selected_year=st.sidebar.selectbox("Select Year",years)
    if selected_country=='Overall' and selected_year=='Overall':
        st.title('Overall Tally')
    elif selected_country=='Overall' and selected_year!='Overall':
        st.title(f'Medal Tally in {selected_year} Olympics')
    elif selected_country != 'Overall' and selected_year == 'Overall':
        st.title(f'{selected_country} Overall Medal Tally')
    else:
        st.title(f'{selected_country} Medal Tally in {selected_year} Olympics')
    medal_tally=calculations.fetch_medal_tally(df,selected_country,selected_year)
    st.table(medal_tally)

elif user_menu=='Overall Analysis':
    result=calculations.overall_analysis(df)
    st.title('Top Statistics')
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(result[0])
    with col2:
        st.header('Cities')
        st.title(result[1])
    with col3:
        st.header('Sports')
        st.title(result[2])

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header('Events')
        st.title(result[3])
    with col5:
        st.header('Athletes')
        st.title(result[4])
    with col6:
        st.header('Nations')
        st.title(result[5])

    nations_over_time=calculations.data_over_time(df,'Region','Number of Countries')
    st.markdown("***")
    st.title("Participating Nations Over The Years")
    fig1=px.line(nations_over_time,x='Years',y='Number of Countries',width=700, height=500)
    st.plotly_chart(fig1)

    events_over_time = calculations.data_over_time(df, 'Event', 'Number of Events')
    st.markdown("***")
    st.title("Events Over The Years")
    fig2=px.line(events_over_time, x='Years', y='Number of Events',width=700, height=500)
    st.plotly_chart(fig2)

    events_over_time = calculations.data_over_time(df, 'Name', 'Number of Athletes')
    st.markdown("***")
    st.title("Athletes Over The Years")
    fig3=px.line(events_over_time, x='Years', y='Number of Athletes',width=700, height=500)
    st.plotly_chart(fig3)

    st.markdown("***")
    st.title("Number Of Events Over Time( Per Every Sport)")
    fig4 = px.imshow(calculations.reshape_for_heatmap(df), width=700, height=700)
    st.plotly_chart(fig4)

    st.markdown("***")
    st.title("Most Successful Athletes")
    sports_list=['Overall']+sorted(df['Sport'].unique())
    selected_sport=st.selectbox('Select Sport',sports_list)
    players=calculations.get_most_successfull(df,selected_sport)
    st.table(players)

elif user_menu=='Country wise Analysis':
    st.sidebar.title('Country wise Analysis')
    unique_countries=sorted(df['Region'].dropna().unique())
    selected_country=st.sidebar.selectbox('Choose a Country',unique_countries)
    country_df=calculations.yearwise_medal_tally(df,selected_country)
    fig5=px.line(country_df,x='Year',y='Medal',width=700, height=500)
    st.title(f"{selected_country} Medal Tally Over The Years")
    st.plotly_chart(fig5)

    st.markdown("***")
    st.title(f"{selected_country} Excells In the following Sports")
    fig6 = px.imshow(calculations.reshape_for_countrywise_heatmap(df,selected_country), width=700, height=500)
    st.plotly_chart(fig6)

    st.markdown("***")
    st.title(f"Top 10 Athletes of {selected_country}")
    top_10=calculations.get_most_successfull_countrywise(df,selected_country)
    st.table(top_10)

else:
    age_dist=calculations.get_age_distribution(df)
    st.title("Distribution of Age")
    fig7=ff.create_distplot(age_dist[0] ,age_dist[1],show_hist=False, show_rug=False)
    fig7.update_layout(autosize=False,width=700, height=500)
    st.plotly_chart(fig7)

    st.markdown("***")
    st.title("Distribution of Age wrt Sport(Gold Medalist)")
    famous_sport=calculations.get_famous_sports(df)
    fig8=ff.create_distplot(famous_sport[0],famous_sport[1],show_hist=False, show_rug=False)
    fig8.update_layout(autosize=False,width=700, height=500)
    st.plotly_chart(fig8)

    st.markdown("***")
    st.title("Height vs Weight")
    sport_list=sorted(df['Sport'].dropna().unique())
    current_sport=st.sidebar.selectbox("Select Sport",sport_list)
    h_vs_w=calculations.weight_vs_height(df,current_sport)
    fig9=px.scatter(data_frame=h_vs_w,x='Weight',y='Height',color='Medal',facet_col="Sex")
    fig9.update_layout(autosize=False, width=700, height=500)
    st.plotly_chart(fig9)

    st.markdown("***")
    st.title("Men vs Women Participation")
    m_vs_w=calculations.men_vs_women(df)
    fig10=px.line(m_vs_w, 'Year', ['Male', 'Female'],width=700, height=500)
    st.plotly_chart(fig10)
