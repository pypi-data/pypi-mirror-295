
# Asuraa Library

## Overview

The Asuraa library provides a suite of AI functionalities, including image generation, code generation, and chatbot interactions. This README provides a guide to install and use the library in a Python environment.

## Installation

To install or upgrade the Asuraa library, use the following pip command:

```bash
pip install --upgrade Asuraa
```

## Usage

### 1. AI Image Generation

Generate an AI image based on a description.

```python
from Asuraa import api
generated_image= api.ai_image("boy image")
print(generated_image)
```

### 2. ChatGPT AI

Interact with the ChatGPT AI for various responses. You can also specify modes for tailored interactions.

```python
from Asuraa import api

# Execute Chatgpt AI with the input text

response = api.chatgpt("Write simple basic html website")

print(response)

# Execute Chatgpt AI with the input text with modes features

# available modes are "girlfriend","anime","animev2","flirt","friend","humans"

response = api.chatgpt("hi babe","girlfriend")

print(response)
```

### 3. Chatbot AI

Interact with a generic chatbot AI.

```python
from Asuraa import api

# Execute Chatbot AI with the input text

print(api.chatbot("hii"))
```

### 4. Code Generation

Generate code using either Blackbox AI or Gemini AI.

```python
from Asuraa import api

# Execute blackbox AI with the input text

print(api.blackbox("write flask app code"))
```

### 5. IMDB Search

Fetch movie information from IMDB.

```python
from Asuraa import api


movie_data = api.imdb("The Godfather")

print(movie_data)
```

### 6. Data Science Information

Fetch data science information using DataGPT AI.

```python
from Asuraa import api

# Execute datagpt AI with the input text
response = api.datagpt("what is data science")
print(response)
```

## License

© 2024-2025 Asuraa. All rights reserved.
