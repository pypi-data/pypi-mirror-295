import random
import requests
import string,re,os,io
import base64,json,time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
from requests_html import HTMLSession
from Asuraa.function import (payloads_response,gpt_4_mode,payload4)
from base64 import b64decode as m,b64encode as n
from PIL import Image, ImageDraw, ImageFont
__version__ = "0.6.5.7"

__all__ = ["api"]


class Asuraa:
    
    def __init__(self)->None:
        """Api for various purpose
    support group : https://t.me/AsuraaSupport
    owner : @itzAsuraa
        """
        pass
    
    @staticmethod
    def datagpt(args:str):
        """
        Sends a query to a specified datagpt API endpoint to retrieve a response based on the provided question.

        Args:
            args (str): The question or input for the datagpt.

        Returns:
            str: The response text from the datagpt API.

        Example usage:
        >>> from Asuraa import api
        >>> response = api.datagpt("What are the latest trends in AI?")
        >>> print(response)
        """
        url = "https://www.blackbox.ai/api/chat=="
        payload = {
            "question": args,
            "chatbotId": "712544d1-0c95-459e-ba22-45bae8905bed",
            "session_id": "8a790e7f-ec7a-4834-be4a-40a78dfb525f",
            "site": "datacareerjumpstart.mykajabi.com"
        }

        try:
            response = requests.post(url, json=payload)
            extracted_text = re.findall(r"\{(.*?)\}", response.text, re.DOTALL)
            extracted_json = "{" + extracted_text[0] + "}]}"
            json_text = extracted_json.replace('\n', ' ')

            data = json.loads(json_text)
            return {"results":data["text"],"join": "@AsuraaSupport", "success": True
                    }
        except Exception as e:
            return e   
        
    @staticmethod
    def blackbox(args: str) -> requests.Response:
        """
        Interact with the Blackbox AI API for generating content. 🧠

        Args:
            args (str): The input text to interact with the Blackbox AI chat API.

        Returns:
            requests.Response: The response object from the API request.

        Example usage:
        >>> from Asuraa import api
        >>> response = api.blackbox("Hello, how are you?")
        >>> print(response.text)
        {
            "response": "Generated content response",
            "status": 200
        }
        """

        url = f"https://www.blackbox.ai/api/chat="
        
        payload = {
            "agentMode": {},
            "codeModelMode": True,
            "id": "XM7KpOE",
            "isMicMode": False,
            "maxTokens": None,
            "messages": [
                {
                    "id": "XM7KpOE",
                    "content": urllib.parse.unquote(args),
                    "role": "user"
                }
            ],
            "previewToken": None,
            "trendingAgentMode": {},
            "userId": "87cdaa48-cdad-4dda-bef5-6087d6fc72f6",
            "userSystemPrompt": None
        }

        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'sessionId=f77a91e1-cbe1-47d0-b138-c2e23eeb5dcf; intercom-id-jlmqxicb=4cf07dd8-742e-4e3f-81de-38669816d300; intercom-device-id-jlmqxicb=1eafaacb-f18d-402a-8255-b763cf390df6; intercom-session-jlmqxicb=',
            'Origin': m('aHR0cHM6Ly93d3cuYmxhY2tib3guYWk=').decode("utf-8"),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return {"results": response.text, "join": "@AsuraaSupport", "success": True}
        except Exception as e:
            return e  
    
    @staticmethod
    def chatgpt(args:str,mode:str=False):
       
        """
        Sends a query to a specified chatgpt API endpoint to retrieve a response based on the provided question.
        

        Args:
            args (str): The question or input for the chatgpt.
            mode(str) : this  parameter is used to select different models of Chatgpt
                        available modes are "girlfriend","anime","animev2","flirt","santa","elonmusk","wormgpt"

        Returns:
            str: The response text from the chatgpt API.

        Example usage:
        >>> from Asuraa import api
        >>> response = api.chatgpt("hi babe?",mode="girlfriend")
        >>> print(response)
        """
        if not mode:
            session = requests.Session()
            response_data=payloads_response(payloads=payload4,args=args)
            url = "https://api.exh.ai/chatbot/v1/get_response"
            headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6ImJvdGlmeS13ZWItdjMifQ.O-w89I5aX2OE_i4k6jdHZJEDWECSUfOb1lr9UdVH4oTPMkFGUNm9BNzoQjcXOu8NEiIXq64-481hnenHdUrXfg",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
            response = session.post(url, headers=headers, data=json.dumps(response_data))
            return {"results":response.json()["response"],"join": "@AsuraaSupport", "success": True}
        else:
            try:
                result = gpt_4_mode(args, mode)
                return {"results":result,"join": "@AsuraaSupport", "success": True}
                
            except Exception as e:
                return e  
           
    @staticmethod
    def gemini(args: str) -> dict:
        """
        Generate content using the Gemini API. ✨

        Args:
            args (str): The input text to generate content.

        Returns:
            dict: A dictionary containing the generated content with metadata.

        Example usage:
        >>> from Asuraa import api
        >>> generated_content = api.gemini("Hello, how are you?")
        >>> print(generated_content)
        """
        url = m('aHR0cHM6Ly9nZW5lcmF0aXZlbGFuZ3VhZ2UuZ29vZ2xlYXBpcy5jb20vdjFiZXRhL21vZGVscy9nZW1pbmktcHJvOmdlbmVyYXRlQ29udGVudD9rZXk9QUl6YVN5QlFhb1VGLUtXalBWXzRBQnRTTjBEUTBSUGtOZUNoNHRN').decode("utf-8")
        headers = {'Content-Type': 'application/json'}
        payload = {
            'contents': [
                {'parts': [{'text': args}]}
            ]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                generated_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                return {"results":generated_text,"join": "@AsuraaSupport", "success": True}
        except Exception as e:
            return e
    
    @staticmethod
    def imdb(args: str) -> dict:
        """
        Retrieve information about a movie or TV show from IMDb based on the search query.

        Args:
        args (str): The movie or TV show to search for on IMDb.

        Returns:
        dict: A dictionary containing details about the movie or TV show, such as name, description, genre,
            actors, trailer link, and more.

        Example usage:
        >>> from Asuraa import api
        >>> movie_data = api.imdb("The Godfather")
        >>> print(movie_data)
        """

        session = HTMLSession()

        url = f"https://www.imdb.com/find?q={args}"
        response = session.get(url)
        results = response.html.xpath("//section[@data-testid='find-results-section-title']/div/ul/li")
        urls = [result.find("a")[0].attrs["href"] for result in results][0]

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(f"https://www.imdb.com/{urls}", headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")

        movie_name = soup.title.text.strip()

        meta_tags = soup.find_all("meta")
        description = ""
        keywords = ""

        for tag in meta_tags:
            if tag.get("name", "") == "description":
                description = tag.get("content", "")
            elif tag.get("name", "") == "keywords":
                keywords = tag.get("content", "")

        json_data = soup.find("script", type="application/ld+json").string
        parsed_json = json.loads(json_data)

        movie_url = parsed_json["url"]
        movie_image = parsed_json["image"]
        movie_description = parsed_json["description"]
        movie_review_body = parsed_json["review"]["reviewBody"]
        movie_review_rating = parsed_json["review"]["reviewRating"]["ratingValue"]
        movie_genre = parsed_json["genre"]
        movie_actors = [actor["name"] for actor in parsed_json["actor"]]
        movie_trailer = parsed_json["trailer"]
        
        output = []
        for result in results:
            name = result.text.replace("\n", " ")
            url = result.find("a")[0].attrs["href"]
            if ("Podcast" not in name) and ("Music Video" not in name):
                try:
                    image = result.xpath("//img")[0].attrs["src"]
                    file_id = url.split("/")[2]
                    output.append({
                        "movie_name": movie_name,
                        "id": file_id,
                        "poster": image,
                        "description": description,
                        "keywords": keywords,
                        "movie_url": movie_url,
                        "movie_image": movie_image,
                        "movie_description": movie_description,
                        "movie_review_body": movie_review_body,
                        "movie_review_rating": movie_review_rating,
                        "movie_genre": movie_genre,
                        "movie_actors": movie_actors,
                        "movie_trailer": movie_trailer,
                        "join": "@AsuraaSupport",
                        "success": True,
                    })
                    return {"results": output}
                except:
                    return {"Success": False}
    
        @staticmethod
        def blackpink(args):
            """generate blackpink  image from text
        """
        text = args
        font_path = os.path.dirname(__file__)+"blackpink.ttf"
        font_size = 230
        font = ImageFont.truetype(font_path, font_size)
        fontsize = int(font.getlength(text))
        img = Image.new("RGB", (fontsize + 100, font_size + 100), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text(
            ((img.width - fontsize) / 2, 0),
            text,
            fill=(255, 148, 224),
            font=font,
            align="center",
        )
        draw.rectangle([0, 0, img.width, img.height], outline="#ff94e0", width=20)
        img2 = Image.new("RGB", (fontsize + 800, font_size + 300), color=(0, 0, 0))
        img2.paste(img, (350, 100))

        buffered = io.BytesIO()
        img2.save(buffered, format="JPEG")
        img_str = n(buffered.getvalue()).decode("utf-8")
        return img_str
        
    @staticmethod
    def ai_image(prompt: str) -> bytes:
        """Generates an AI-generated image based on the provided prompt.

        Args:
            prompt (str): The input prompt for generating the image.

        Returns:
            bytes: The generated image in bytes format.
            
        Example usage:
        >>> from Asuraa import api
        >>> generated_image= api.ai_image("boy image")
        >>> print(generated_image)
        """
        url = f"https://ai-api.magicstudio.com/api/ai-art-generator"

        form_data = {
            'prompt': prompt,
            'output_format': 'bytes',
            'request_timestamp': str(int(time.time())),
            'user_is_subscribed': 'false',
        }

        response = requests.post(url, data=form_data)
        if response.status_code == 200:
            try:
                if response.content:
                    return response.content
                else:
                    raise Exception("Failed to get image from the server.")
            except Exception as e:
                raise e
        else:
            raise Exception("Error:", response.status_code)

        
            
api=Asuraa()

