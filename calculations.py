def medal_tally(df):

    subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event','Medal']
    medal_tally = df.drop_duplicates(subset=subset)
    medal_tally = (medal_tally.groupby('Region', as_index=False)[['Gold', 'Silver', 'Bronze']].sum()
                              .sort_values('Gold',ascending=False))
    medal_tally['Total Medals'] = medal_tally[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    cols_to_int=['Total Medals','Gold', 'Silver', 'Bronze']
    medal_tally[cols_to_int]=medal_tally[cols_to_int].astype(int)
    return  medal_tally

def country_year(df):
    countries = ['Overall'] + sorted(df['Region'].dropna().unique())
    years = ['Overall'] + sorted(df['Year'].unique())
    return countries,years


def fetch_medal_tally(df, country, year):
    flag = False
    subsets = ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    df = df.drop_duplicates(subset=subsets)
    if country == 'Overall' and year == 'Overall':
        fetched_df = df
    elif country == 'Overall' and year != 'Overall':
        fetched_df = df[df['Year'].eq(year)]
    elif country != 'Overall' and year == 'Overall':
        fetched_df = df[df['Region'].eq(country)]
        flag = True
    else:
        fetched_df = df[(df['Region'].eq(country)) & (df['Year'].eq(year))]

    if flag:
        fetched_df = (fetched_df.groupby('Year', as_index=False)[['Gold', 'Silver', 'Bronze']].sum()
                      .sort_values('Year'))
    else:
        fetched_df = (fetched_df.groupby('Region', as_index=False)[['Gold', 'Silver', 'Bronze']].sum()
                      .sort_values('Gold', ascending=False))

    fetched_df['Total Medals'] = fetched_df[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    conv_to_int = ['Total Medals', 'Gold', 'Silver', 'Bronze']
    fetched_df[conv_to_int] = fetched_df[conv_to_int].astype(int)
    return fetched_df

def overall_analysis(df):
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['Region'].unique().shape[0]
    return  editions,cities,sports,events,athletes,nations

def data_over_time(df,column,name):
    resdf=(df.drop_duplicates(subset=['Year',column])['Year'].value_counts()
                .sort_index().reset_index()
                .rename(columns={'index': 'Years', 'Year': name}))
    return  resdf

def reshape_for_heatmap(df):
    return  (df.drop_duplicates(subset=['Year','Sport','Event'])
               .pivot_table(values='Event',index='Sport',columns='Year',aggfunc='count',fill_value=0))

def get_most_successfull(df,sport):
    df=df.dropna(subset=['Medal'])
    if sport!='Overall':
        df=df[df['Sport'].eq(sport)]
    return (df['Name'].value_counts().reset_index(name='Total Medals')
                      .rename(columns={'index':'Name'}).head(15)
                      .merge(df,on=['Name'],how='left')
                      .loc[:,['Name','Sport','Region','Total Medals']]
                      .drop_duplicates(subset=['Name']))

def yearwise_medal_tally(df,country):
    temp_df=df.dropna(subset=['Medal'])
    subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event','Medal']
    temp_df=temp_df.drop_duplicates(subset=subset)
    new_df=temp_df[temp_df['Region'].eq(country)]
    return new_df.groupby('Year')['Medal'].count().reset_index()

def reshape_for_countrywise_heatmap(df,country):
    temp_df=df.dropna(subset=['Medal'])
    subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event','Medal']
    temp_df=temp_df.drop_duplicates(subset=subset)
    new_df=temp_df[temp_df['Region'].eq(country)]
    return  new_df.pivot_table(values='Medal',index='Sport',columns='Year',fill_value=0,aggfunc='count')

def get_most_successfull_countrywise(df,country):
    df=df.dropna(subset=['Medal'])
    df=df[df['Region'].eq(country)]
    return (df['Name'].value_counts().reset_index(name='Total Medals')
                      .rename(columns={'index':'Name'}).head(15)
                      .merge(df,on=['Name'],how='left')
                      .loc[:,['Name','Sport','Total Medals']]
                      .drop_duplicates(subset=['Name']).head(10))

def get_age_distribution(df):
    athelete_df = df.drop_duplicates(subset=['Name', 'Region'])
    x1 = athelete_df['Age'].dropna()
    x2 = athelete_df.loc[athelete_df['Medal'].eq('Gold'), 'Age'].dropna()
    x3 = athelete_df.loc[athelete_df['Medal'].eq('Silver'), 'Age'].dropna()
    x4 = athelete_df.loc[athelete_df['Medal'].eq('Bronze'), 'Age'].dropna()
    labels=['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist']
    return [[x1,x2,x3,x4],labels]

def get_famous_sports(df):
    subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event','Medal']
    famous_sports=df.drop_duplicates(subset=subset)
    famous_sports = df.groupby('Sport')['Medal'].count().sort_values(ascending=False).head(38).index.tolist()
    athelete_df = df.drop_duplicates(subset=['Name', 'Region'])
    x=[]
    name=[]
    for sport in famous_sports:
        temp_df=athelete_df[athelete_df['Sport']==sport]
        x.append(temp_df.loc[temp_df['Medal'].eq('Gold'),'Age'].dropna())
        name.append(sport)
    return x,name

def weight_vs_height(df,sport):
    athelete_df = df.drop_duplicates(subset=['Name', 'Region']).dropna(subset=['Sport'])
    athelete_df['Medal'] = athelete_df['Medal'].fillna('No Medal')
    return athelete_df.loc[athelete_df['Sport'].eq(sport)]

def men_vs_women(df,sport):
    athelete_df = df.drop_duplicates(subset=['Name', 'Region'])
    athelete_df=athelete_df[athelete_df['Sport'].eq(sport)]
    men=athelete_df[athelete_df['Sex'].eq('M')].groupby('Year')['Name'].count().reset_index()
    women=athelete_df[athelete_df['Sex'].eq('F')].groupby('Year')['Name'].count().reset_index()
    return men.merge(women,on='Year').rename(columns={"Name_x":"Male","Name_y":"Female"})
