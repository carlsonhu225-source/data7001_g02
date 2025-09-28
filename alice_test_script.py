
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

cwd = os.getcwd()
data_dir = cwd.replace('data7001_g02','Data')

cdnnba = pd.read_csv(data_dir+'/cdnnba_2024.csv')
shotdetail = pd.read_csv(data_dir+'/shotdetail_2024.csv')

# print column names
cdnnba.columns
shotdetail.columns

# over what range of time does 'shotdetail' cover?
shotdetail['GAME_DATE'].sort_values()
# ans: 22/10/2024 - 13/04/2025

# how many different games does each df cover?
print(len(shotdetail['GAME_ID'].unique()))
print(len(cdnnba['gameId'].unique()))
# ans: 1230 games for both

# are these the same?
all(shotdetail['GAME_ID'].sort_values().unique() == cdnnba['gameId'].sort_values().unique())

# determine the number of NA, for each column, and save this. 
# cdnnba has multiple NAs
attrs = []
numNAs = []
for column in cdnnba.columns:
    if any(cdnnba[column].isna()):
        numNA = sum(cdnnba[column].isna())
        print(f'Attribute {column} has {numNA} NAs')
        attrs.append(column)
        numNAs.append(numNA)
array1 = np.array(attrs)
array2 = np.array(numNAs)
matrix = np.hstack((array1.reshape(-1, 1), array2.reshape(-1, 1)))
filename = 'numNAs.txt'
np.savetxt(filename, matrix, fmt = '%s', delimiter = ',')

# no columns in shotdetail have nas
for column in shotdetail.columns:
    if any(shotdetail[column].isna()):
        print(f'Attribute {column} has {sum(shotdetail[column].isna())} NAs')


# are actionNumber in cdnnba, and GAME_EVENT_ID in shotdetail the same?
print(len(shotdetail['GAME_EVENT_ID'].unique()))
print(len(cdnnba['actionNumber'].unique()))
plt.hist(shotdetail['GAME_EVENT_ID'])
plt.hist(cdnnba['actionNumber'])
plt.show()
# 830 action numbers in shotdetail vs 853 in cdnnba

# Are SHOT_DISTANCE and shotDistance duplicates?
print(shotdetail['SHOT_DISTANCE']) # datatype: int
print(cdnnba['shotDistance']) # datatype: float64
print(sum(cdnnba['shotDistance'].isna())) # 466479
print(sum(shotdetail['SHOT_DISTANCE'].isna())) # 0
# ans: yes

# how are the 'area' values different?
print(cdnnba['area'].value_counts())
print(cdnnba['areaDetail'].value_counts())
print(shotdetail['SHOT_ZONE_BASIC'].value_counts())
print(shotdetail['SHOT_ZONE_AREA'].value_counts())

# 'GRID_TYPE' is uninformative and contains the same repeated string value
print(shotdetail['GRID_TYPE'].value_counts())

# 'SHOT_ATTEMPTED_FLAG' is uninformative
shotdetail['SHOT_ATTEMPTED_FLAG'].value_counts()

# 'EVENT_TYPE' is an exact duplicate of 'SHOT_MADE_FLAG'
shotdetail['SHOT_MADE_FLAG'].value_counts()
shotdetail['EVENT_TYPE'].value_counts()
all(shotdetail[shotdetail['SHOT_MADE_FLAG']==0]['EVENT_TYPE'] == 'Missed Shot')
all(shotdetail[shotdetail['SHOT_MADE_FLAG']==1]['EVENT_TYPE'] == 'Made Shot')

# SHOT_ZONE_RANGE might be just a discretised, categorical version of SHOT_DISTANCE:
print(shotdetail['SHOT_ZONE_RANGE'].value_counts()) 
shotdetail['SHOT_DISTANCE'][shotdetail['SHOT_DISTANCE']>=24]
shotdetail['SHOT_DISTANCE'][shotdetail['SHOT_DISTANCE']<8]


# creating the merged dataset, using a left join

# for efficiency - drop unnecessary/unused columns before the merge


# first rename one column, so that the join can work
cdnnba_rename = cdnnba.rename(columns={'gameId': 'GAME_ID'})

# does the left-join give the same result no matter what order?
#test1 = pd.merge(shotdetail, cdnnba_rename, on='GAME_ID', how='left')
#test2 = pd.merge(cdnnba_rename, shotdetail, on='GAME_ID', how='left')
