import datetime
import requests
import json
from app.config import config


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

    def post_idea_to_monday(self, user_name, idea_text):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        column_values = {
            # First row is column id's
            "text": idea_text,
            "status": {"label": "New Idea"},
            "date4": {"date": date},
            "text__1": user_name
        }
        result = self.create_task(config.config.MONDAY_BOARD_ID, config.config.MONDAY_GROUP_ID, idea_text, column_values)
        return result

