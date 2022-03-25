import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')

title = 'Tarea generada por python'
def create_row(parent_id: str):
    """Create a page (row) in a database

    Args:
        parent_id (str): ID of parent database
    """
    # The payload is for the same database format as in recurring_task. Make sure that you have the same columns, otherwise this will fail
    payload = {
        # This specifies in which database our row gets added
        'parent': {'database_id': parent_id},
        'properties': {  # These are our columns
            # Read the documentation to see what values you can use, I can't explain it better:)
            # https://developers.notion.com/reference/page#property-value-object
            "Status": {
                    "id": "%3E~A%3E",
                    "type": "select",
                    "select": {
                        "id": "1",
                        "name": "Not started",
                        "color": "red"
                    }
            },

            "priority": {
                    "id": "%5C%3E%7DZ",
                    "type": "select",
                    "select": {
                        "id": "d4d9c4a7-24f8-454e-b0b8-238d686d9632",
                        "name": "normal",
                        "color": "yellow"
                    }
            },
            
            "due date": {
                    "id": "%5DEHZ",
                    "type": "date",
                    "date": {
                        "start": "2022-03-18",
                    }
            },

            "assign": {
                    "id": "bOiu",
                    "type": "people",
                    "people": [
                        {
                            "object": "user",
                            "id": "ebb357fa-0943-4d4a-b62e-b1e755e677f8",
                            "name": "Toto Rios",
                            "avatar_url": "https://s3-us-west-2.amazonaws.com/public.notion-static.com/09471ae6-a6db-470c-b0f0-e3f712870b18/IMG_0222.jpeg",
                            "type": "person",
                            "person": {
                                "email": "joseantonio_ra@live.com"
                            }
                        }
                    ]
            },

            "subject": {
                    "id": "l~~%3C",
                    "type": "relation",
                    "relation": [
                        {
                            "id": "b6583683-ce9e-4741-b979-c327911471cc"
                        }
                    ]
            },

            "type": {
                    "id": "~%3D%3FB",
                    "type": "multi_select",
                    "multi_select": [
                        {
                            "id": "5827d8eb-ffa5-4dc4-844c-0e8b4dcb872c",
                            "name": "Activity",
                            "color": "blue"
                        },
                        {
                            "id": "1ea8773b-630c-420c-85e1-d1a56975d2bb",
                            "name": "to deliver",
                            "color": "green"
                        }
                    ]
            },

            "Name": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": "{}".format(title),
                        },
                        "plain_text": "{}".format(title),
                    }
                ]
            }
        }
    }

    # The actual API request
    response = requests.post('https://api.notion.com/v1/pages/', json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

   # If the request was not successful, we print the error and return
    if not response.ok:
        print('Error:', response.status_code)
        print('Error:', response.content)
        return

    # Parse response as JSON and return
    data = response.json()
    return data

    # The actual API request
    response = requests.post('https://api.notion.com/v1/pages/', json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2022-02-22'})

   # If the request was not successful, we print the error and return
    if not response.ok:
        print('Error:', response.status_code)
        print('Error:', response.content)
        return

    # Parse response as JSON and return
    data = response.json()
    return data


if __name__ == "__main__":

    # Id of your Database. Looks like this: f1f5071d-8d2a-47aa-9ddc-02b8aad3f6bc
    # Use list_databases.py to get the id of your database
    # Your database should look like this: https://safelyy.notion.site/f1f5071d8d2a47aa9ddc02b8aad3f6bc
    # You can duplicate it, create one manually or try to create one with the API. See create_database.py for an example!
    database_id = '438e5ef3-19e8-4e31-9ba6-d2eda2899ea8'

    # Create a row in database
    data = create_row(database_id)
    if data is not None:
        # print(json.dumps(data, indent=4))
        print('New row available here: {}'.format(data['url']))

    page_parent_id = '1085ccbf-f898-47b9-8444-d88697cad81b'

    # Create a normal page

    # page_data = create_page(page_parent_id)
    # if page_data is not None:
    #     # print(json.dumps(data, indent=4))
    #     print('New page available here: {}'.format(page_data['url']))