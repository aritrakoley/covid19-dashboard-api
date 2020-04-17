import requests as req
import pandas as pd
import json

def get_sources():
    data_sources = [
        {
            'title': 'MoHW [Govt. of India]',
            'url': 'https://www.mohfw.gov.in/'
        }
    ] 
    return data_sources

def get_helplines():
    helplines = { "helplines": [
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
    }
    
    return helplines



def scrape(data_source):
    page_html = req.get(data_source['url']).text
    ts = page_html.find("<table")
    te = page_html.find("</table>", ts) + 8

    page_table = page_html[ts:te]

    main_df = pd.read_html(page_table)[0].iloc[:-3, 1:]
    columns = ['State', 'Confirmed', 'Recovered', 'Deceased']
    main_df.columns = columns
    for i in range(1, 4):
        main_df.iloc[:, i] = main_df.iloc[:, i].astype('int64')
    return main_df

def get_formatted_data(src_index):
    main_df = scrape(get_sources()[src_index])
    
    data_sources = get_sources()
    helplines = get_helplines()

    states = main_df['State'].to_list()
    confirmed = main_df['Confirmed'].to_list()
    recovered = main_df['Recovered'].to_list()
    deceased = main_df['Deceased'].to_list()

    total_confirmed = sum(confirmed)
    total_recovered = sum(recovered)
    total_deceased = sum(deceased)

    data = {
        'sources': data_sources,
        'helplines': helplines,
        'states': states,
        'confirmed': confirmed,
        'recovered': recovered,
        'deceased': deceased,
        'total_confirmed': total_confirmed,
        'total_recovered': total_recovered,
        'total_deceased': total_deceased
    }

    return data

if __name__ == "__main__":
    main_df = scrape(get_sources()[0])
    json_data = make_json(0)

    json.dump(json_data, open('json_data.json', 'w'))
    print(main_df)
    print(main_df.dtypes)
