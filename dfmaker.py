import pandas as pd
import argparse
from tqdm import tqdm
import traceback


def get_states(df):
    return list(set(df['state']))

def get_cities(state, df):
    df1=df[df['state']==state]
    return list(set(df1['city']))

def get_streets(city,df):
    street_col = df[df['city'] == city]['streets']
    street_col = list(street_col)
    out = []
    for i in street_col:
        out.extend(i.split(','))

    return list(set(out))
    

def make_streets(df,output):
    states=get_states(df)
    for (j,state) in enumerate(tqdm(states)):
        cities=get_cities(state, df)
        for city in cities:
            try:
                streets = get_streets(city, df)
                with open(output+state+', '+city+'.txt', 'w') as f:
                    for street in streets:
                        f.write(street+'\n')
            except:
                print(state,",",city)
    
                    
                    
if __name__ == "__main__":
    df = pd.read_csv("street names/street.csv")
    output = 'street names/'
    make_streets(df,output)
    
