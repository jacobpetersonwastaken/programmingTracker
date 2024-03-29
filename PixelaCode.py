from json import loads, dump, load
from os import getenv
from dotenv import load_dotenv
from requests import post, delete, put


class PixelaCode:
    secret_stuff = load_dotenv('.env')
    pixela_api_key = getenv('PIXELA_API_KEY')
    pixela_api_username = getenv('PIXELA_API_USERNAME')
    pixela_api_id = getenv('PIXELA_API_ID')
    post_value_endpoint = f'https://pixe.la/v1/users/{pixela_api_username}/graphs/{pixela_api_id}'

    def log_pixela_push(self, push_date: str):
        """logs if pixela date was pushed successfully. cant add to logData because that class runs
        on its own thread"""
        with open('runtime_sessions.json', 'r') as f:
            data = load(f)
        with open('runtime_sessions.json', 'w') as file:
            if "days_pushed_to_pixela" not in data:
                data["days_pushed_to_pixela"] = [push_date]
            else:
                data["days_pushed_to_pixela"].append(push_date)
            dump(data, file)

    def upload_to_pixela(self, hours: float, log_date: str):
        """Uploads the summed session data to pixela"""
        parameters = {
            'date': log_date,
            'quantity': str(hours)
        }
        try:
            response = post(url=self.post_value_endpoint, headers={'X-USER-TOKEN': self.pixela_api_key},
                            json=parameters)
            if loads(response.text)['isSuccess']:
                return True
        except:
            return False

    def delete_a_pixela_upload(self, date: str):
        """delete pixela"""
        post_value_endpoint = f'https://pixe.la/v1/users/{self.pixela_api_username}/graphs/{self.pixela_api_id}/{date}'
        delete(url=post_value_endpoint, headers={'X-USER-TOKEN': self.pixela_api_key})
