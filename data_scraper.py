import requests as req
import pandas as pd
import json
import re


def get_sources():
    data_sources = [
        {
            'title': 'MoHW [Govt. of India]',
            'url': 'https://www.mohfw.gov.in/'
        }
    ] 
    return data_sources

def get_helplines():
    helplines = [
        {
            "title": "WB Helpline 1",
            "phone": "033-24312600",
            "loc": "None",
            "type": "Govt. Helpline"
        },
        {
            "title": "WB Helpline 2",
            "phone": "1800313444222",
            "loc": "None",
            "type": "Govt. Helpline (Toll free)"
        },
        {
            "title": "Beliaghata ID",
            "phone": "033-23032200",
            "loc": "57, Beleghata Main Rd, Subhas Sarobar Park, Phool Bagan, Beleghata, Kolkata 700010",
            "type": "Hospital"
        },
        {
            "title": "PG Hospital",
            "phone": "033-22041101",
            "loc": "1, Harish Mukherjee Rd, Gokhel Road, Bhowanipore, Kolkata 700020",
            "type": "Hospital"
        },
        {
            "title": "RG Kar",
            "phone": "033-25557656",
            "loc": "1, Khudiram Bose Sarani, Bidhan Sarani, Shyam Bazar, Kolkata, West Bengal 700004",
            "type": "Hospital"
        },
        {
            "title": "North Bengal Medical College",
            "phone": "0353 258 5478",
            "loc": "Sushruta Nagar, Siliguri, West Bengal 734012",
            "type": "Hospital"
        }
    ]
    
    return helplines

def extract_num(s): # returns a string
  nums = re.findall(r'\d+', str(s))
  return int(nums[0]) if len(nums) > 0 else 0

def scrape(data_source):
    page_html = req.get(data_source['url']).text

    ts = page_html.find("<table")
    te = page_html.find("<td colspan", ts)
    
    tmp_html = page_html[ts:te]
    te = tmp_html.rfind("</tr>") + 5

    page_table = tmp_html[0:te] + "</table>"

    main_df = pd.read_html(page_table)[0].iloc[0:, 1:]

    columns = ['State', 'Active', 'Recovered', 'Deceased', 'Confirmed']
    main_df.columns = columns

    # Remove Rows with invalid values
    valid =  (main_df['State'].notna()) & (main_df['Active'].notna()) & (main_df['Recovered'].notna()) & (main_df['Deceased'].notna()) & (main_df['Confirmed'].notna())
    main_df = main_df[valid]
    
    # extract numbers from strings (eg: '119#')
    for c in range(1, main_df.shape[1]):
        for r in range(0, main_df.shape[0]):
            main_df.iloc[r, c] = extract_num(main_df.iloc[r, c])
        main_df.iloc[:, c] =  main_df.iloc[:, c].astype('int64')
    
    return main_df

def get_formatted_data(src_index):
    main_df = scrape(get_sources()[src_index])
    main_df = main_df.sort_values(by='Confirmed', ascending=False)
    
    data_sources = get_sources()
    helplines = get_helplines()

    states = main_df['State'].to_list()
    confirmed = main_df['Confirmed'].to_list()
    recovered = main_df['Recovered'].to_list()
    deceased = main_df['Deceased'].to_list()
    active = main_df['Active'].to_list() 

    total_confirmed = sum(confirmed)
    total_recovered = sum(recovered)
    total_deceased = sum(deceased)
    total_active = sum(active)

    data = {
        'sources': data_sources,
        'helplines': helplines,
        'states': states,
        'confirmed': confirmed,
        'recovered': recovered,
        'deceased': deceased,
        'active': active,
        'total_confirmed': total_confirmed,
        'total_recovered': total_recovered,
        'total_deceased': total_deceased,
        'total_active': total_active
    }

    return data


