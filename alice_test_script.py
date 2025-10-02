
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
# ans: yes 

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

# no columns in shotdetail have NAs:
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

# 'GRID_TYPE' is uninformative and contains the same repeated string value - drop
print(shotdetail['GRID_TYPE'].value_counts())

# 'SHOT_ATTEMPTED_FLAG' is uninformative - drop
shotdetail['SHOT_ATTEMPTED_FLAG'].value_counts()

# 'EVENT_TYPE' is an exact duplicate of 'SHOT_MADE_FLAG' - drop one
shotdetail['SHOT_MADE_FLAG'].value_counts()
shotdetail['EVENT_TYPE'].value_counts()
all(shotdetail[shotdetail['SHOT_MADE_FLAG']==0]['EVENT_TYPE'] == 'Missed Shot')
all(shotdetail[shotdetail['SHOT_MADE_FLAG']==1]['EVENT_TYPE'] == 'Made Shot')

# SHOT_ZONE_RANGE might be just a discretised, categorical version of SHOT_DISTANCE:
print(shotdetail['SHOT_ZONE_RANGE'].value_counts()) 
shotdetail['SHOT_DISTANCE'][shotdetail['SHOT_DISTANCE']>=24]
shotdetail['SHOT_DISTANCE'][shotdetail['SHOT_DISTANCE']<8]
shotdetail[['SHOT_ZONE_BASIC', 'SHOT_ZONE_AREA']].value_counts()

# x and y locations in the datasets, and how they vary:
plt.hist(cdnnba['x'])
plt.show()
print(cdnnba['x'].min(), cdnnba['x'].max())
plt.hist(cdnnba['y'])
plt.show()
print(cdnnba['y'].min(), cdnnba['y'].max())
# x and y in cdnnba range from 0 to 100, for both.

print(shotdetail['LOC_X'].min(), shotdetail['LOC_X'].max())
print(shotdetail['LOC_Y'].min(), shotdetail['LOC_Y'].max())
# in shotdetail, x is in range [-250,250], y is in range [-52,842]

#x legacy: -168
#y legacy: 205
#game id: 22400001
# event id: 7
#x 27.414586
#y 83.578431
# actual x: 25.76971084
#actual y: 41.7892155
shotdetail.iloc[0,]
cdnnba[(cdnnba['gameId']==22400001) & (cdnnba['actionNumber']==7)].iloc[0,]

# investigating shot distances > 80 ft
# why are some of these classed as 'Mid-Range' area, but with shot distance >80 ft? e.g.:
cdnnba[cdnnba['shotDistance']>80].iloc[2,]

# create plot/histogram of shot distance, broken down by each area. 
fig, axs = plt.subplots(2, 3, figsize=(10, 8)) 

df = shotdetail
col = 'SHOT_ZONE_BASIC'
shot_col = 'SHOT_DISTANCE'
axs[0,0].hist(df[df[col]=="Above the Break 3"][shot_col])
axs[0,0].set_title('Above the Break 3')
axs[0,0].set_xlim(0,100)
axs[0,1].hist(df[df[col]=="Restricted Area"][shot_col])
axs[0,1].set_title('Restricted Area')
axs[0,1].set_xlim(0,100)
axs[0,2].hist(df[df[col]=="In The Paint (Non-RA)"][shot_col])
axs[0,2].set_title("In The Paint (Non-RA)")
axs[0,2].set_xlim(0,100)
axs[1,0].hist(df[df[col]=="Mid-Range"][shot_col])
axs[1,0].set_title("Mid-Range")
axs[1,0].set_xlim(0,100)
axs[1,1].hist(df[df[col]=="Left Corner 3"][shot_col])
axs[1,1].set_title("Left Corner 3")
axs[1,1].set_xlim(0,100)
axs[1,2].hist(df[df[col]=="Right Corner 3"][shot_col])
axs[1,2].set_title("Right Corner 3")
axs[1,2].set_xlim(0,100)

plt.tight_layout()
plt.show()

# note: there are two entries which have shot distance that do not make sense
# for an area 'Mid-Range'. Shot distance of 61.83, and 84.71
# these are for the cdnnba dataset
cdnnba[cdnnba['area']=="Mid-Range"]['shotDistance'].value_counts()

# for the shotdetail dataset, it doesn't appear to have this problem:
shotdetail[shotdetail['SHOT_ZONE_BASIC']=="Mid-Range"]['SHOT_DISTANCE'].value_counts()

##################################################
# creating the merged dataset, using a left join:
# for efficiency - drop unnecessary/unused columns before the merge
to_drop_cdnnba = ['orderNumber','period','personId',
                  'teamId','teamTricode','playerName','playerNameI',
                  'personIdsFilter','area','areaDetail','shotDistance',
                  'shotResult','jumpBallRecoveredName', 'jumpBallRecoverdPersonId',
                  'jumpBallWonPlayerName', 'jumpBallWonPersonId',
                  'jumpBallLostPlayerName', 'jumpBallLostPersonId',
                  'blockPlayerName', 'blockPersonId','reboundTotal','reboundDefensiveTotal',
                  'reboundOffensiveTotal', 'officialId','stealPlayerName', 
                  'stealPersonId','foulPersonalTotal', 'foulTechnicalTotal', 
                  'foulDrawnPlayerName','foulDrawnPersonId',
                  'description','subType','qualifiers','descriptor','edited',
                  'isTargetScoreLastPeriod']


to_drop_shotdetail = ['GRID_TYPE','SHOT_ATTEMPTED_FLAG','EVENT_TYPE']

# first rename the join column, so that the join can work
cdnnba_new = cdnnba.rename(columns={'gameId': 'GAME_ID'})
# drop columns, use axis=1 to specify column
cdnnba_new = cdnnba_new.drop(to_drop_cdnnba, axis=1)
shotdetail_new = shotdetail.drop(to_drop_shotdetail, axis=1)

# merge: 
#test1 = pd.merge(shotdetail_new, cdnnba_new, on='GAME_ID', how='left')
#test2 = pd.merge(cdnnba_rename, shotdetail, on='GAME_ID', how='left')
