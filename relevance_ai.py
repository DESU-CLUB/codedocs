import re
import requests
import json
import dotenv
import os
from groq import Groq

# This script provides the agents function for the python api call with relevance api
dotenv.load_dotenv()
GROQ_KEY = os.environ["GROQ_KEY"]
print(GROQ_KEY)
client = Groq(
    api_key=GROQ_KEY
)

url_to_be_scrapped = "https://docs.python.org/3/tutorial/index.html"
YOUR_API_KEY = os.getenv("RELEVANCE_AI_API_KEY")
exercise_pattern = r'Exercise (\d+):\s*([\s\S]*?)(?=Exercise \d+:|$)'
solution_pattern = r'Exercise (\d+)\s*\*\*\n```python\n([\s\S]*?)(?=```)'
testcase_pattern = r'Testcase (\d+)\*\*\n([\s\S]*?)(?=```)'


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
                "content": f"""Here are the completed exercises with test cases:

**Exercise 1**
```python
import torch
import numpy as np

# Create a sample signal
signal = torch.tensor([1, 2, 3, 4, 5, 6, 7, 8], dtype=torch.float32)

# Compute the sample frequencies associated with the Fourier transform of the signal
freq = torch.fft.fftfreq(signal.size()[0], dtype=torch.float32)

print(freq)

**Testcase 1**
assert freq.shape == torch.Size([8])
assert torch.allclose(freq, torch.tensor([-0.5, -0.375, -0.25, -0.125, 0.125, 0.25, 0.375, 0.5]))
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

**Testcase 2**
assert reordered_fftn_signal.shape == torch.Size([3, 3])
assert torch.allclose(reordered_fftn_signal, torch.tensor([[7.06225781e+01+1.22464680e-16j, 2.12132034e+00-1.22464680e-16j, 2.12132034e+00+1.22464680e-16j], 
                                                            [2.12132034e+00-1.22464680e-16j, 3.53553391e+00+1.22464680e-16j, 3.53553391e+00-1.22464680e-16j], 
                                                            [2.12132034e+00+1.22464680e-16j, 3.53553391e+00-1.22464680e-16j, 7.06225781e+01-1.22464680e-16j]]))
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

**Testcase 3**
assert ifftn_signal.shape == torch.Size([3, 3])
assert torch.allclose(ifftn_signal, signal)
```
    
    Please also generate test cases for the code that you write. You should ensure that the testcases work. You need to make sure other than the incomplete line, the rest of the previous template code is unchanged. 
    
    {exercise}
"""
                , }
        ],
        model="mixtral-8x7b-32768")
    return possible_test_cases.choices[0].message.content


if __name__ == "__main__":
    summary = webScraperAgent("https://pytorch.org/docs/stable/tensors.html")
    generated_problems = problemGeneratorAgent(summary)

    extracted_problems = re.findall(exercise_pattern, generated_problems)
    for problem in extracted_problems:
        print(problem)
        possible_solution_code = answer_question_agent(problem)
        possible_test_cases = generate_test_cases(problem)
        print(possible_solution_code)
        print(possible_test_cases)