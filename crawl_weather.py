import requests

def get_weather(locationName):
    url  ="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    token = "CWB-C66BAF53-A26D-4472-89E4-60A009E06D16"

    payload = {"Authorization":token,
               "locationName":locationName,
               }
    r = requests.get(url, params=payload)
    json_data = r.json()["records"]["location"] 

    if not json_data:
        return None

    wea_ele = json_data[0]["weatherElement"]

    pop = [i['time'] for i in wea_ele if i["elementName"]=="PoP"][0]
    period_list = [[p["startTime"],p["endTime"],p['parameter']['parameterName']] for p in pop]

    mint = [i['time'] for i in wea_ele if i["elementName"]=="MinT"][0]
    for i,item in enumerate(period_list):
        for m in mint:
            if (m["startTime"]==item[0])&(m["endTime"]==item[1]):
                period_list [i].append(m["parameter"]["parameterName"])
                
    maxt = [i['time'] for i in wea_ele if i["elementName"]=="MaxT"][0]
    for i,item in enumerate(period_list ):
        for m in maxt:
            if (m["startTime"]==item[0])&(m["endTime"]==item[1]):
                period_list[i].append(m["parameter"]["parameterName"])

    #簡化時間
    for period in period_list:
        period[0] = period[0][5:-3]
        period[1] = period[1][5:-3]

    return period_list