import requests
import json
from dotenv import load_dotenv
import os



YOUR_API_KEY = os.getenv("RELEVANCE_AI_API_KEY")
data = requests.post('https://api-f1db6c.stack.tryrelevance.com/latest/studios/191d63f3-79e9-4c9c-bbdd-63183acb8c5e/trigger_limited', 
  headers={"Content-Type":"application/json"},
  data=json.dumps({"params":{"url":"https://docs.python.org/3/tutorial/index.html","objective_of_scraping":"print hello wolrd"}
                   ,"project":"aab78808483b-4114-81eb-ae9686888922"})
)

print(data.json())


