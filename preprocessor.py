import pandas as pd

def preprocess(df,region_df,season):
    if season=='Summer':
        df = df.query("Season=='Summer'")
    elif season=='Winter':
        df = df.query("Season=='Winter'")
    else:
        df=df
    df['Region'] = df['NOC'].map(dict(region_df.iloc[:, :2].to_numpy()))
    df = df.drop_duplicates()
    df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
    return  df