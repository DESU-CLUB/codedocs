import re
import requests
import json
import dotenv
import os
from groq import Groq
import nbformat as nbf


# This script provides the agents function for the python api call with relevance api
dotenv.load_dotenv("../.env")
GROQ_KEY = os.environ["GROQ_KEY"]
print(GROQ_KEY)
client = Groq(
    api_key=GROQ_KEY
)

url_to_be_scrapped = "https://docs.python.org/3/tutorial/index.html"
YOUR_API_KEY = os.getenv("RELEVANCE_AI_API_KEY")
exercise_pattern = r'Exercise (\d+):\s*([\s\S]*?)(?=Exercise \d+:|$)'
solution_pattern = r'Exercise (\d+)\s*\*\*\n```python\n([\s\S]*?)(?=```)'
testcase_pattern = r'Exercise (\d+)\s*\*\*\n```python\n([\s\S]*?)(?=```)'


### General workflow ->
## scrape -> problems generator -> problems verifier -> publish to ipynb

### This scrapes the relevant data from the documentation sites
def webScraperAgent(url: str) -> json:
    print(f"Scraping {url}")
    data = requests.post(
        'https://api-f1db6c.stack.tryrelevance.com/latest/studios/191d63f3-79e9-4c9c-bbdd-63183acb8c5e/trigger_limited',

        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {"params": {"url": url,
                        "objective_of_scraping": "You are a agent responsible in scraping out relevant information "
                                                 "from coding documentations. Your main job is to ensure accuracy, "
                                                 "so do not include things you are not sure of."}, "project":
                 "aab78808483b-4114-81eb-ae9686888922"})
    )

    return data.json()["output"]["output"]


def getFileName(url):
    filename = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Given the following URL, please provide a suitable name for the notebook file that will be created. Ideally the file name should be the topic of the documentation.
                
                Here is the URL:{url}
                """
            }
        ],
        model = "mixtral-8x7b-32768"
    )
    return filename.choices[0].message.content
    

def problemGeneratorAgent(summary):
    print("Generating problems for ")
    problems = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Given the following summary, please write a coding exercise for the user to complete. You should write most of the code out already, and only leave a few lines blank for the user to write out
    
    You should only generate the instructions and the code exercise. The solutions and explanations are to be omitted. The focus on the exercises/incomplete lines should be on the code related to the given documentation
    
    The following example is an example of what you should output:
   Here are a few coding exercises based on the summary:

################################################
Exercise 1:
Write code to compute the inverse discrete Fourier transform of a 1D signal using `torch.fft.ifft()`.

```python
import torch

# Create a sample signal
signal = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8])

# Compute the discrete Fourier transform of the signal
fft_signal = torch.fft.fft(signal)

###TODO: Compute the inverse discrete Fourier transform of the signal (roughly 1 line)

print(ifft_signal)
```

################################################
Exercise 2:
Write code to compute the 2D discrete Fourier transform of a 2D signal using `torch.fft.fftn()`.

```python
import torch

# Create a sample 2D signal
signal = torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

###TODO: Compute the 2D discrete Fourier transform of the signal (roughly 1 line)

print(fftn_signal)
```

################################################
Exercise 3:
Write code to shift the zero-frequency component of a 1D signal to the center of the spectrum using `torch.fft.fftshift()`.

```python
import torch

# Create a sample signal
signal = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8])

# Compute the discrete Fourier transform of the signal
fft_signal = torch.fft.fft(signal)

###TODO: Shift the zero-frequency component of the signal to the center of the spectrum (roughly 1 line)

print(shifted_fft_signal)
```

Note: You need to complete the exercises by filling in the `###TODO` lines with the appropriate code.
    Here is the summary:
    {summary}""",
            }
        ],
        model="mixtral-8x7b-32768")
    return problems.choices[0].message.content


def answer_question_agent(exercise: str):
    print("Trying to answer this question")
    possible_answer = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
    Given the following coding exercise, please write out the code that would complete the exercise. You should write out the code that would complete the exercise.

    Example solution will be:
    Here are the completed exercises with test cases:

**Exercise 1**
```python
import torch
import numpy as np

# Create a sample signal
signal = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8], dtype=torch.float32)

# Compute the sample frequencies associated with the Fourier transform of the signal
freq = torch.fft.fftfreq(signal.size()[0], dtype=torch.float32)

print(freq)

```

**Exercise 2**
```python
import torch

# Create a sample 2D signal
signal = torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Compute the 2D discrete Fourier transform of the signal
fftn_signal = torch.fft.fftn(signal)

# Reorder the elements of the FFT data
reordered_fftn_signal = torch.fft.fftshift(fftn_signal)

print(reordered_fftn_signal)

```

**Exercise 3**
```python
import torch

# Create a sample 2D signal
signal = torch.tensor([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Compute the 2D discrete Fourier transform of the signal
fftn_signal = torch.fft.fftn(signal)

# Compute the inverse 2D discrete Fourier transform of the signal
ifftn_signal = torch.fft.ifftn(fftn_signal)

print(ifftn_signal)


```
    {exercise}

""",
            }
        ],
        model="mixtral-8x7b-32768")
    return possible_answer.choices[0].message.content


def generate_test_cases(exercise):
    print("Generating test cases")
    possible_test_cases = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                Given the following code, please write out the test cases that would verify the correctness of the code. You should write out the test cases that would verify the correctness of the code. Make sure the test cases align with the code.
                Below is an example of how the testcases would look like: (You must follow the format provided)
                #######################################################################################################
**Exercise 1**
```python
assert freq.shape == torch.Size([8])
assert torch.allclose(freq, torch.tensor([-0.5, -0.375, -0.25, -0.125, 0.125, 0.25, 0.375, 0.5]))
```


**Exercise 2**
```python
assert reordered_fftn_signal.shape == torch.Size([3, 3])
assert torch.allclose(reordered_fftn_signal, torch.tensor([[7.06225781e+01+1.22464680e-16j, 2.12132034e+00-1.22464680e-16j, 2.12132034e+00+1.22464680e-16j], 
                                                            [2.12132034e+00-1.22464680e-16j, 3.53553391e+00+1.22464680e-16j, 3.53553391e+00-1.22464680e-16j], 
                                                            [2.12132034e+00+1.22464680e-16j, 3.53553391e+00-1.22464680e-16j, 7.06225781e+01-1.22464680e-16j]]))
**Exercise 3**
```python
assert ifftn_signal.shape == torch.Size([3, 3])
assert torch.allclose(ifftn_signal, signal)
```
  ################################################################################################################  
    Below is the solutions you have to write test cases for:
    
    {exercise}
"""
                , }
        ],
        model="mixtral-8x7b-32768")
    return possible_test_cases.choices[0].message.content


def create_notebook(exercises, solutions, testcases, filename = 'new_exercise_notebook'):
    import nbformat as nbf

    # Create a new notebook
    nb = nbf.v4.new_notebook()


    nb.cells.append(nbf.v4.new_markdown_cell("# Setup\nImport your libraries here"))
    nb.cells.append(nbf.v4.new_code_cell("import mercury as mr"))
    print(exercises)
    # Loop through the exercises, solutions, and test cases
    for ex_number, ex_content in exercises:
        # Add exercise description as a markdown cell
        desc_pattern = r'([\s\S]*?)(?=```python)'
        desc_match = re.search(desc_pattern, ex_content)
        description = desc_match.group(1).strip() if desc_match else ""
        nb.cells.append(nbf.v4.new_markdown_cell(f"# Exercise {ex_number}\n{description.strip()}"))
        
        # Extract code part from exercise content (assume it's inside triple backticks)
        code_match = re.search(r'```python\n([\s\S]*?)\n```', ex_content)
        if code_match:
            exercise_code = code_match.group(1)
            # Add exercise code as a code cell
            nb.cells.append(nbf.v4.new_code_cell(exercise_code.strip()))
        
        # Add hidden solution as a code cell with a docstring to prevent execution
        solution = next((sol[1] for sol in solutions if sol[0] == ex_number), "")
        if solution:
            hidden_solution = f'"""\n# Solution hidden\n{solution.strip()}\n"""'
            solution_cell = nbf.v4.new_code_cell(hidden_solution)
            solution_cell.metadata.update({"tags": ["hide_cell"]})
            nb.cells.append(nbf.v4.new_markdown_cell(f'# Solution {ex_number}'))
            nb.cells.append(solution_cell)
        
        # Add test case as a code cell
        print(testcases)
        testcase = next((tc[1] for tc in testcases if tc[0] == ex_number), "")
        if testcase:
            testcase_cell = nbf.v4.new_code_cell(testcase.strip()+'\n'+'mr.Confetti()')
            testcase_cell.metadata.update({"tags": ["hide_cell"]})
            nb.cells.append(testcase_cell)

    # Save the new notebook
    with open(f'{filename}.ipynb', 'w') as f:
        nbf.write(nb, f)



def creator(url):
    summary = webScraperAgent(url)
    filename = getFileName(url)
    generated_problems = problemGeneratorAgent(summary)
    possible_solution_code = answer_question_agent(generated_problems)
    possible_test_cases = generate_test_cases(possible_solution_code)
    print(possible_test_cases)
    extracted_problems = re.findall(exercise_pattern, generated_problems)
    extracted_solutions = re.findall(solution_pattern, possible_solution_code)
    extracted_testcases = re.findall(testcase_pattern, possible_test_cases)
    while not(len(extracted_problems) == len(extracted_solutions) == len(extracted_testcases)):
        possible_solution_code = answer_question_agent(generated_problems)
        possible_test_cases = generate_test_cases(possible_solution_code)
        extracted_problems = re.findall(exercise_pattern, generated_problems)
        extracted_solutions = re.findall(solution_pattern, possible_solution_code)
        extracted_testcases = re.findall(testcase_pattern, possible_test_cases)
    veriified_problems = []
    verified_solutions = []
    verified_testcases = []
    verified_descriptions=  []
    
    """ for description,problem, solution, testcase in zip(extracted_problems, extracted_solutions, extracted_testcases):
        print(solution)
        print(testcase)
     """
    create_notebook(extracted_problems, extracted_solutions, extracted_testcases)
    return filename






""" if __name__ == "__main__":
    summary = webScraperAgent("https://pytorch.org/docs/stable/tensors.html")
    generated_problems = problemGeneratorAgent(summary)

    extracted_problems = re.findall(exercise_pattern, generated_problems)
    for problem in extracted_problems:
        print(problem)
        possible_solution_code = answer_question_agent(problem)
        possible_test_cases = generate_test_cases(possible_solution_code)
        print(possible_solution_code)
        print(possible_test_cases)
 """
 
 
creator(url_to_be_scrapped)