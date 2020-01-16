
import os, requests, pandas as pd

year='2017'
dsource='acs'
dsource2='acs5'
dname='profile'
#state='11'
state='36'
#geo='public use microdata area'
geo='zip code tabulation area'

base_url = f'https://api.census.gov/data/{year}/{dsource}/{dsource2}/{dname}'

#This section gets the list of variables from the api, compares it to list
#of variables that we want to retrieve, and checks to make sure nothing is
#missing
##
datadict={}
dps=['DP02','DP03','DP04','DP05']
for p in dps:
    vars_url = f'https://api.census.gov/data/{year}/{dsource}/{dsource2}/{dname}/groups/{p}.json'
    response=requests.get(vars_url)
    var_data=response.json()
    datadict.update(var_data['variables'])
    
dfxl = pd.read_excel(os.path.join('inputs','acs_variables.xlsx'),sheet_name='acs1')
      
dfvars = pd.DataFrame.from_dict(datadict,columns=['label','predicateType'],orient='index')
dfvars_selected=dfvars.loc[dfvars.index.isin(dfxl['census_var'])]

dfvars_count=len(dfvars_selected)
dfxl_count=len(dfxl['census_var'])

if dfvars_count==dfxl_count:
    print('There are an equal number of variables in both lists:', dfvars_count)
else:
    print('There is a mismatch in the number of variables; the api has retrieved', 
          dfvars_count, 'while the original list has',dfxl_count,'. Missing:')
    nomatch=dfxl[~dfxl['census_var'].isin(dfvars_selected.index)]
    print(nomatch)
    
mismatch=dfxl[~dfxl['census_label'].isin(dfvars_selected['label'])]

if len (mismatch) ==0:
    print('All labels match')
else:
    test=pd.merge(mismatch,dfvars_selected, left_on='census_var', right_on=dfvars_selected.index)
    print('These labels do not match:')
    print(test[['census_var','census_label','label']])

#This section takes that list and retrieves the actual data

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

reqvars=list(chunks(dfvars_selected.index.tolist(),46))
reqvars[0].insert(0,'NAME')
reqvars[0].insert(0,'GEO_ID')

datalist=[]

zctas=['10034','10040']

for z in zctas:
    ziplist=[]
    for i, v in enumerate(reqvars):
        batchcols=','.join(v)
        data_url = f'{base_url}?get={batchcols}&for={geo}:{z}'
        response=requests.get(data_url)
        data=response.json()
        for i2, v2 in enumerate(data):
            if i == 0:
                ziplist.append(v2[:-1])
            else:
                for x in v2[:-1]:
                    ziplist[i2].append(x)
    if len(datalist)==0:
        datalist.append(ziplist[0])
        datalist.append(ziplist[1])
    else:
        datalist.append(ziplist[1])

            
