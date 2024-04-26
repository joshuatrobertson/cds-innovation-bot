import requests
import json
from app import config


class MondayManager:
    def __init__(self):
        self.url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": f"Bearer {config.MONDAY_KEY}",
            "Content-Type": "application/json"
        }

    def create_task(self, board_id, group_id, item_name, column_values):
        # Encode the column_values as JSON
        column_values_json = json.dumps(column_values)

        # Prepare the GraphQL query, inserting variables directly into the mutation
        query = f'''
                mutation ($boardId: ID!, $groupId: String!, $itemName: String!, $columnValues: JSON!) {{
                    create_item (
                        board_id: $boardId, 
                        group_id: $groupId, 
                        item_name: $itemName, 
                        column_values: $columnValues
                    ) {{
                        id
                    }}
                }}
                '''

        variables = {
            "boardId": board_id,
            "groupId": group_id,
            "itemName": item_name,
            "columnValues": column_values_json
        }

        data = {
            "query": query,
            "variables": variables
        }

        response = requests.post(self.url, headers=self.headers, json=data)
        try:
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Failed to create item in Monday.com: {e}")
            return None
