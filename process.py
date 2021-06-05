import pandas as pd
import argparse

class Args():
    def __init__(self, input_path="data.pkl" , output_path="data.csv"):
        
        self.i=input_path
        self.o=output_path
        
    def init_parsearges(self):
        ap = argparse.ArgumentParser()
        
        # Argument of insightface
        ap.add_argument("-i","--i", default=self.i,
                        type=str, help='path to pickle file')
        
        ap.add_argument("-o","--o", default=self.o,
                        type=str, help='path to csv output')
        
        args = ap.parse_args()
        
        return args

def foo(x):
#     print(x)
    dic={}
    for i in x:
#         print(i, i.keys())
        for key in i.keys():
            dic.setdefault(key,[]).append(i[key])
    return dic

def foo2(x):
    string=''
    for i in x:
        string+=i+' '
        
    return string

def open_pkl(path="data.pkl"):
    return pd.read_pickle(path)

def make_csv(input_path,output_path):
    pkl = open_pkl(input_path)
    df=pd.DataFrame()
    df['name']=pkl['name']
    df[['latitude','longtitude']]=pkl['coordinates'].apply(pd.Series)
    df[['address1','address2','address3','city','zip_code','country','state','display_address']]=pkl['location'].apply(pd.Series)
    df[['display_address']]=df['display_address'].apply(foo2)
    df[['alias,title']]=pkl['categories'].apply(foo)
    df[['alias','title']]=df['alias,title'].apply(pd.Series)

    df=df[['name','title','latitude','longtitude','address1','address2','address3','city','zip_code','country','state','display_address']]
    df=df.drop_duplicates(['name','latitude','longtitude','address1','address2','address3','city','zip_code','country','state','display_address'])
    df.to_csv(output_path, index=False)
#     return df

if __name__ == '__main__':
    args=Args(input_path="data.pkl"
             ,output_path="data.csv")
    
    print("[Info] Initializing processes ...")
    args=args.init_parsearges()
    
    make_csv(args.i,args.o)
    print("          DONE          ")
    
    
    
    
    