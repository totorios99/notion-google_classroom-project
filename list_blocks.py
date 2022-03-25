import requests
import json
import os
from dotenv import load_dotenv
# Load the .env file
load_dotenv()

# TODO: Make sure that you have a NOTION_SECRET environment variable set
NOTION_TOKEN = os.getenv('NOTION_SECRET', '')


def list_blocks(page_id: str):
    has_more = True
    blocks = []
    next_cursor = None

    # Notion uses "Pagination", which is a technique to split large amounts of data into smaller chunks.
    # Each requests has a has_more attribute which indicates if there are more pages to be fetched.
    # The next_cursor variable is the cursor for the next page.
    # More information about pagination: https://developers.notion.com/reference/pagination
    while has_more:

        # In the first iteration we don't have a cursor, so we don't pass it as a parameter
        if next_cursor is not None:
            params = {'start_cursor': next_cursor}
        else:
            params = {}

        # The actual API request
        response = requests.get('https://api.notion.com/v1/blocks/{}/children'.format(page_id), params, headers={
            'Authorization': 'Bearer '+NOTION_TOKEN, 'Notion-Version': '2022-02-22'})

        # If the request was not successful, we print the error and return the block array
        if not response.ok:
            print('Error:', response.status_code)
            print('Error:', response.content)
            return blocks

        # Parse the response as JSON
        data = response.json()
        # Extract has_more and next_cursor attributes
        has_more = data['has_more']
        next_cursor = data['next_cursor']

        # Extend our user array with the new results
        blocks.extend(data['results'])

        # If you want to see the complete response, uncomment the following line
        # print(json.dumps(data, indent=4))

    return blocks


if __name__ == "__main__":

    # You can get the page_id with list_pages.py
    tarea3_page = '025bb222-7a22-4762-b191-289684d84d8f'
    main_block = '848f6239-1b7e-4494-9183-d5df022cf68a'
    first_child = '3c781e69-cba2-4d5b-8256-4608db4bf1b9'
    second_child = '8f52fed9-9ae5-4615-a43d-1e2ca8116ae3'
    # Call function to get blocks
    blocks = list_blocks(first_child)

    # Example iteration over block array
    for block in blocks:
        # Read more about blocks: https://developers.notion.com/reference/block
        print(json.dumps(block, indent=4))