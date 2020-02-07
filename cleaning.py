import requests
import pandas as pd
import numpy as np

'''this file cleans and prepares a final csv for our database'''

#first we have to get the strain api data
#connect
key = 'QsLigX4'
url = 'https://strainapi.evanbusse.com/{}/strains/search/all'.format(key)
r = requests.request('GET', url=url)

#put into df and create index
json = r.json()
df = pd.DataFrame.from_dict(json).T.reset_index()
df = df.rename(columns={'index':'name'})


#divides the features within effects
positive = []
negative = []
medical = []
for index, row in df.iterrows():
    positive.append(row['effects']['positive'])
    negative.append(row['effects']['negative'])
    medical.append(row['effects']['medical'])
df['positive'] = positive
df['negative'] = negative
df['medical'] = medical

#the effects column is now just extra
df = df.drop('effects', axis=1)
df_strain = df.copy()

#now we will get and clean the kaggle data

df_kag = pd.read_csv(r'C:\Users\Emma\Desktop\cannabis-strains-features\Cannabis_Strains_Features.csv')
#this is where you can download the file
#https://www.kaggle.com/nvisagan/cannabis-strains-features          

#make column names and name column same as df_strain
df_kag = df_kag.rename(columns={'Strain':'name', 'Type':'race'})
df_kag['name'] = df_kag['name'].apply(lambda x: x.strip().replace('-',' '))

#merge dataframes so that all new rows are kept
merged = pd.merge(df_strain, df_kag, how='outer')

#fill in na values with empty string so the for loop can work with them


merged['Flavor'] = merged.Flavor.fillna('')
merged['flavors'] = merged.flavors.fillna(pd.Series([[]]*len(merged)))
merged['Effects'] = merged.Effects.fillna('')
merged['positive'] = merged.positive.fillna(pd.Series([[]]*len(merged)))

#The flavors in the kaggle dataset can have any new flavors added to the list from the strain api
for index, row in merged.iterrows():
    for flav in row['Flavor'].split(','):
        #import pdb; pdb.set_trace()
        if flav not in row['flavors']:
            row['flavors'].append(flav)

merged = merged.drop('Flavor', axis=1)


#The kaggle dataset only lists positive effects, so we can append any effects that are new to the list of positive effects
for index, row in merged.iterrows():
    for effect in row['Effects'].split(','):
        if effect not in row['positive']:
            row['positive'].append(effect) 

#effects column now useless, set id as index      
merged = merged.drop('Effects', axis=1)
merged = merged.set_index('id')

print(merged.tail())
print(merged.columns)
print(merged.shape)

#merged.to_csv(r'C:\Users\Emma\Desktop\Datascience-master (1)\best_merge.csv')

#after saving the CSV, open in excel, go to index 1972 and fill following index values
#use the same method to clear the flavors and effects column from that index down. 
#now you have a clean and accurate database
