import requests
import json
from dotenv import load_dotenv
import os


#This script provides the agents function for the python api call with relevance api  

url_to_be_scrapped = "https://docs.python.org/3/tutorial/index.html"
YOUR_API_KEY = os.getenv("RELEVANCE_AI_API_KEY")


### todo
### 1. Get the correct api link 
### 2. Get the relevants prompt for the web scraper agent


# web scrapping agent 
def webScraperAgent(url : str, prompt: str) -> json :
  """
  Given a url and a prompt, this function will scrape the url and return the data in json format
  """
  data = requests.post('https://api-f1db6c.stack.tryrelevance.com/latest/studios/191d63f3-79e9-4c9c-bbdd-63183acb8c5e/trigger_limited', 
    headers={"Content-Type":"application/json"},
    data = json.dumps({"params":{"url": url,"objective_of_scraping":"<insert prompt here"}
                ,"project":"a0d6e4ed-8bd9-4c7e-8708-2827fc3bd44c"}))


  return data.json()

# verifier
def CodeVerifierAgent(question: str, solution: str) -> bool:
  """
  Given a question and a solution, this function will return a boolean value
  """
  isCorrect = 0

  data = requests.post('https://api-f1db6c.stack.tryrelevance.com/latest/studios/191d63f3-79e9-4c9c-bbdd-63183acb8c5e/trigger_limited',
    headers={"Content-Type":"application/json"},
    data=json.dumps({"params":{"question": question,"solution": solution}
                    ,"project":"a0d6e4ed-8bd9-4c7e-8708-2827fc3bd44c"}))
  
  if data.json()["result"] == "correct":
    isCorrect = 1
  
  return isCorrect

