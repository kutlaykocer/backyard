"""The analysis result for SpiderFoot."""
import json
import time
import sys

import pandas as pd
import spacy

nlpEN = spacy.load('en')
nlpDE = spacy.load('de')

def getModuleDummy(name):
    module = {}
    module['Module'] = name
    return module

def isGermanName(name):
    #name-like entries, e.g. "Kostenlose Service-Hotline" should return false
    humanName = False
   
    doc = nlpDE(name)
    endIndex = 0
    for ent in doc.ents:
        #print(ent.text, ent.start_char, ent.end_char, ent.label_)
        humanName = True
        endIndex = ent.end_char
        if(ent.label_ != "PER"):
            humanName = False
            break
    
    if(humanName and endIndex < len(name)):
        #including unprocessed part
        humanName = False
    
    return humanName

# NOT used
def isEnglishName(name):
    #name-like entries, e.g. "Kostenlose Service-Hotline" should return false
    humanName = False
    
    doc = nlpEN(name)
    endIndex = 0
    for ent in doc.ents:
        #print(ent.text, ent.start_char, ent.end_char, ent.label_)
        humanName = True
        if(ent.label_ != "PERSON"):
            humanName = False
            break
            
    if(humanName and endIndex < len(name)):
        #including unprocessed part
        humanName = False
        
    return humanName

def filterNames(nameData):
    removalList = []
    for name, count in nameData.items():
        #name-like entries, e.g. "Kostenlose Service-Hotline" could be removed here
        if(not isGermanName(name)):
            removalList.append(name)
    
    print("Count of names:", len(nameData))
    print("After filtering German Words:", len(nameData)- len(removalList))
    
    for name in removalList:
        nameData = nameData.drop(labels = name)

    return nameData

def getCountsData(df, moduleName, dataType):
    series = df.loc[(df['Module'] == moduleName) & (df['Type'] == dataType)]['Data'].value_counts()
    return series

def getMapData(df, moduleName, dataType, reverse=False):
    data = df.loc[(df['Module'] == moduleName) & (df['Type'] == dataType)]
    
    series = None
    if(not reverse):
        series = pd.Series(data['Data'].tolist(), index=data['Source'])
    else:
        series = pd.Series(data['Source'].tolist(), index=data['Data'])
    
    return series

# the major method defines which data to abstract and how to abstract them
def getData(df, moduleName, dataType):
    data = None
    
    # sfp_names
    if (moduleName == 'sfp_names'):
        # only HUMAN_NAME is handled while no other type exists in current data file
        if (dataType == 'HUMAN_NAME'):
            data = getCountsData(df, moduleName, dataType)
            #name-like entries, e.g. "Kostenlose Service-Hotline" could be removed here
            data = filterNames(data)
    
    # sfp_dnsresolve
    if (moduleName == 'sfp_dnsresolve'):
        if (dataType == 'IP_ADDRESS'):
            data = getMapData(df, moduleName, dataType)
            
        if(dataType == 'AFFILIATE_INTERNET_NAME'):
            #TODO: value from this type looks like a IP-Host mapping but why it is affilicated?
            data = getMapData(df, moduleName, dataType, True)
    
    if(data is not None):
        # dict is automatically serializable
        data = data.to_dict()
        
    return data

def getTypes(df, moduleName):
    return df.loc[df['Module'] == moduleName]['Type'].unique()

def getModule(df, moduleName):
    # get module data if defined
    result = {}
    for dataType in getTypes(df, moduleName):
        data = getData(df, moduleName, dataType)
        if (data is not None):
            result[dataType] = data
    
    if(len(result) == 0):
        # no data exists or defined
        return None
    
    module = getModuleDummy(moduleName)
    module['Result'] = result
    
    return module

def run(data_dir):
    """Call the analysis."""
    print('Opening datafile in ' + data_dir)

    with open(data_dir + '/paths.json') as f:
        json_data = json.load(f)

    csv_file = data_dir + '/' + json_data['data']['file']
    df = pd.read_csv(csv_file, parse_dates=['Last Seen'], engine='python')

    # get data by SpiderFoot modules
    resultName = getModule(df, "sfp_names")
    resultDNS = getModule(df, "sfp_dnsresolve")

    result = json.dumps([resultName, resultDNS], indent=4)
    
    print(json.dumps(result, indent=4))

    return result


if __name__ == '__main__':
    run(sys.argv[1])
