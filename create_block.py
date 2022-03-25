import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def create_blocks(block_id: str):
    # This is just an example, take a look at the documentation to see what kind of blocks you can create
    # https://developers.notion.com/reference/block
    payload = {
        'children': [
            {
                'object': 'block',
                'type': 'heading_3',
                'heading_3': {
                    'text': [{'type': 'text', 'text': {'content': 'Instructions'}}]
                }
            },
            {
                'object': 'block',
                'type': 'heading_3',
                'heading_3': {
                    'text': [{'type': 'text', 'text': {'content': 'Resources'}}]
                }
            },
            {
                'object': 'block',
                'type': 'embed',
                'embed': {
                    'url': "https://drive.google.com/file/d/1q289LBOC2VphRg__l8PV_4XPJC8EvHVX/view?usp=drive_web&authuser=1"
                },
                "created_by": {
                "object": "user",
                "id": "ebb357fa-0943-4d4a-b62e-b1e755e677f8"
                },
            },
            {
                'object': 'block',
                'type': 'heading_3',
                'heading_3': {
                    'text': [{'type': 'text', 'text': {'content': 'Attachments'}}]
                }
            },
            {
                'object': 'block',
                'type': 'heading_3',
                'heading_3': {
                    'text': [{'type': 'text', 'text': {'content': 'Personal comments'}}]
                }
            }
        ]
    }

    # The actual API request
    response = requests.patch('https://api.notion.com/v1/blocks/{}/children'.format(block_id), json=payload, headers={
        'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2021-08-16'})

   # If the request was not successful, we print the error and return
    if not response.ok:
        print('Error:', response.status_code)
        print('Error:', response.content)
        return

    # Parse response as JSON and return
    data = response.json()
    return data


if __name__ == "__main__":

    # Id of your Block. Looks like this: f1f5071d-8d2a-47aa-9ddc-02b8aad3f6bc
    # A Page (or Database Row) is also a Block
    # Blocks get appendend to the end of a page
    block_id = '8f52fed9-9ae5-4615-a43d-1e2ca8116ae3'

    # Create a row in database
    data = create_blocks(block_id)
    if data is not None:
        print(json.dumps(data, indent=4))