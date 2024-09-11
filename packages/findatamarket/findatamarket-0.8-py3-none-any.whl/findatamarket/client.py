import requests
import pandas as pd
from io import StringIO

class Client:
    def __init__(self, API_TOKEN: str) -> None:
        self.api_token = API_TOKEN
        self.DOMAIN = 'https://ru.findata.market'
    
    def load_dataset(self, dataset_path: str) -> pd.DataFrame | None:
        
        username = dataset_path.split('/')[0].strip('@')
        dataset_slug = dataset_path.split('/')[1]
        

        response = requests.get(f"{self.DOMAIN}/@{username}/datasets/{dataset_slug}/download")

        if response.status_code == 200:
            csv_data = StringIO(response.text)
            return pd.read_csv(csv_data)
        
        return None
        
        
        
        