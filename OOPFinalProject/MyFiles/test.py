from dotenv import load_dotenv
import os
from main import ComponentAPI
load_dotenv()

# Your API key is now loaded
api = ComponentAPI()
results = api.get_component_prices('cpu', 'Ryzen 5600X')
print(results)