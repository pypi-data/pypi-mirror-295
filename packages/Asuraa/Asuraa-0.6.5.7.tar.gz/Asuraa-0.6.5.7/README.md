
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

def generate_image(description):
    """Generate an AI image based on a description."""
    try:
        image_url = api.ai_image(description)
        print(f"Generated Image URL: {image_url}")
    except Exception as e:
        print(f"Error generating image: {e}")

# Example usage
generate_image("a futuristic city skyline")
```

### 2. ChatGPT AI

Interact with the ChatGPT AI for various responses. You can also specify modes for tailored interactions.

```python
from Asuraa import api

def chat_with_gpt(prompt, mode=None):
    """Interact with ChatGPT AI."""
    try:
        if mode:
            response = api.chatgpt(prompt, mode)
        else:
            response = api.chatgpt(prompt)
        print(f"ChatGPT Response: {response}")
    except Exception as e:
        print(f"Error with ChatGPT: {e}")

# Example usage
chat_with_gpt("Explain quantum computing", mode="anime")
```

### 3. Chatbot AI

Interact with a generic chatbot AI.

```python
from Asuraa import api

def chat_with_bot(prompt):
    """Interact with a generic chatbot AI."""
    try:
        response = api.chatbot(prompt)
        print(f"Chatbot Response: {response}")
    except Exception as e:
        print(f"Error with Chatbot: {e}")

# Example usage
chat_with_bot("What's the weather like today?")
```

### 4. Code Generation

Generate code using either Blackbox AI or Gemini AI.

```python
from Asuraa import api

def generate_code(prompt, ai_type='blackbox'):
    """Generate code using Blackbox or Gemini AI."""
    try:
        if ai_type == 'blackbox':
            response = api.blackbox(prompt)
        elif ai_type == 'gemini':
            response = api.gemini(prompt)
        else:
            raise ValueError("Invalid AI type specified.")
        print(f"Generated Code: {response}")
    except Exception as e:
        print(f"Error generating code: {e}")

# Example usage
generate_code("write a Flask app", ai_type='blackbox')
generate_code("write a REST API with Flask", ai_type='gemini')
```

### 5. IMDB Search

Fetch movie information from IMDB.

```python
from Asuraa import api

def fetch_movie_info(title):
    """Fetch movie information from IMDB."""
    try:
        movie_data = api.imdb(title)
        print(f"Movie Data: {movie_data}")
    except Exception as e:
        print(f"Error fetching movie data: {e}")

# Example usage
fetch_movie_info("The Godfather")
```

### 6. Data Science Information

Fetch data science information using DataGPT AI.

```python
from Asuraa import api

def get_data_info(query):
    """Fetch data science information using DataGPT AI."""
    try:
        response = api.datagpt(query)
        print(f"DataGPT Response: {response}")
    except Exception as e:
        print(f"Error with DataGPT: {e}")

# Example usage
get_data_info("What is machine learning?")
```

## License

© 2024-2025 Asuraa. All rights reserved.
