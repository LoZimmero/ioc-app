import pandas as pd

#Threshold for reliability classes
THRESHOLD_IOC_HIGH=0.9
THRESHOLD_IOC_MEDIUM=0.6

#Di seguito le funzioni utilizzate per ricavare dati aggregati richiesti nelle specifiche e calcolare la reliability

#Calcolo della reliability in base ai criteri definiti nelle specifiche e alle costanti di threshold
def reliability(row):
    iocmatchedperc=row['num_ver_matches']/row['total_num_IoC']
    if (row['taxonomy']=="enthusiast"):
        if(iocmatchedperc>=THRESHOLD_IOC_MEDIUM):
            return "medium"
        else:
            return "low"
    elif(row['taxonomy']=="bot"):
            return "low"
    elif((row['taxonomy']=="corpo")|(row['taxonomy']=="expert")):
        if(iocmatchedperc>=THRESHOLD_IOC_HIGH):
            return "high"
        elif(iocmatchedperc>=THRESHOLD_IOC_MEDIUM):
            return "medium"
        else:
            return "low"
    elif(row['taxonomy']=="removed"):
        return "account removed"
    return "None"

def nmatches(row):
    matches=0
    if row['alienvault_date']!='None':
        matches+=1
    if row['hashlookup_date']!='None':
        matches += 1
    if row['kaspersky_date']!='None':
        matches += 1
    if row['mwbazar_date']!='None':
        matches += 1
    if row['misp_date']!='None':
        matches += 1
    if row['urlhaus_date']!='None':
        matches += 1
    if row['virustotal_date']!='None':
        matches += 1
    return matches

def addnumplatforms(name):
    df= pd.read_csv(name)
    df['n_matches']=df.apply(lambda row: nmatches(row),axis=1)
    df.to_csv('resultwithmatches.csv',index=False)

#Genera il file users.csv, che mostra dati aggregati per ogni utente presente nei dati di partenza
def generateuserscsv(name):

    df = pd.read_csv(name)
    df_botsandusers=pd.read_csv("userslist.csv")

    df3 = df[(df.alienvault_date != "None") | (df.hashlookup_date != "None") |(df.kaspersky_date != "None") |
    (df.mwbazar_date != "None") |(df.misp_date != "None") |(df.urlhaus_date != "None") |(df.virustotal_date != "None") ]

    print (df3)

    df2 = df3.groupby(['user'])['user'].count().reset_index(name='num_ver_matches')
    print(df2.dtypes)

    df4 = df.groupby(['user'])['user'].count().reset_index(name='total_num_IoC')
    df5 = df.groupby('user')['n_matches'].sum().reset_index(name='num_platform_matches')
    print(df4.dtypes)
    print(df5)

    joineddf=pd.merge(df2,df4,how="inner",on="user")
    joineddf=pd.merge(joineddf,df5,how="inner",on="user")
    joineddf['potential_platform_matches']=joineddf["total_num_IoC"]*7
    joineddf=pd.merge(joineddf,df_botsandusers,how="inner",on="user")

    joineddf['estimated_reliability']=joineddf.apply(lambda row: reliability(row),axis=1)

    joineddf.to_csv('users.csv',index=False)

if __name__ == '__main__':
    #uncomment if needed
    '''addnumplatforms('result.csv')'''
    generateuserscsv('resultwithmatches.csv')
