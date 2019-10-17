
import os, requests, pandas as pd

year='2017'
dsource='acs'
dsource2='acs5'
dname='profile'
#cols=['DP02_0001E','DP02_0001M','DP02_0001PE','DP02_0001PM']
state='11'
geo='public use microdata area'

sheet1 = pd.read_excel(os.path.join('inputs','acs_master_working.xlsx'),sheet_name='acs1')

#cols=sheet1.loc[sheet1['census_var_new'].str.startswith('DP02'),'census_var_new'].tolist()

cols=sheet1['census_var_new'].tolist()

base_url = f'https://api.census.gov/data/{year}/{dsource}/{dsource2}/{dname}'


newd={}
dps=['DP02','DP03','DP04','DP05']
for p in dps:
    vars_url = f'https://api.census.gov/data/{year}/{dsource}/{dsource2}/{dname}/groups/{p}.json'
    response=requests.get(vars_url)
    var_data=response.json()
    newd.update(var_data['variables'])
    
#keys=['label','predicateType']
#for vid in cols:
#    for key in keys:
#        print(vid,var_data['variables'][vid][key])
#        
dfvars = pd.DataFrame.from_dict(newd,columns=['label','predicateType'],orient='index')
dfvars_selected=dfvars.loc[dfvars.index.isin(cols)]

#def chunks(l, n):
#    # For item i in a range that is a length of l,
#    for i in range(0, len(l), n):
#        # Create an index range for l of n items:
#        yield l[i:i+n]
#
#test=list(chunks(cols,46))
#test[0].append('GEO_ID')
#test[0].append('NAME')
#
#
#newlist=[]
#
#for i in test:
#    batchcols=','.join(i)
#    data_url = f'{base_url}?get={batchcols}&for={geo}:*&in=state:{state}'
#    response=requests.get(data_url)
#    data=response.json()
#    for j in data:
#        newlist.append(j)
    



