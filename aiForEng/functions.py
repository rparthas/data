# from cairosvg import svg2png
import os
import logging
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def svg_to_png_bytes(svg_string):
    # Convert SVG string to PNG bytes
    # png_bytes = svg2png(bytestring=svg_string.encode('utf-8'))
    # return png_bytes
    return 'not implemented'


def python_math_execution(math_string):
    try:
        answer = eval(math_string)
        if answer:
            return str(answer)
    except:
        return 'invalid code generated'


def generate_image(image_prompt):
    logging.info(f"Generating image from prompt: {image_prompt}")
    try:
        response = openai.images.generate(prompt=image_prompt,
                                          model="dall-e-3",
                                          n=1,
                                          size="1024x1024")
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return str(e)


def run_function(name: str, args: dict):
    if name == "svg_to_png_bytes":
        return svg_to_png_bytes(args["svg_string"])
    elif name == "python_math_execution":
        return python_math_execution(args["math_string"])
    elif name == "image_generation":
        return generate_image(args["image_prompt"])
    else:
        return None


functions = [
    {
        "type": "function",
        "function": {
            "name": "svg_to_png_bytes",
            "description": "Generate a PNG from an SVG",
            "parameters": {
                "type": "object",
                "properties": {
                    "svg_string": {
                        "type":
                            "string",
                        "description":
                            "A fully formed SVG element in the form of a string",
                    },
                },
                "required": ["svg_string"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "image_generation",
            "description": "Generate an image from a prompt",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_prompt": {
                        "type":
                            "string",
                        "description":
                            "A prompt that describes the image to be generated",
                    },
                },
                "required": ["image_prompt"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "python_math_execution",
            "description": "Solve a math problem using python code",
            "parameters": {
                "type": "object",
                "properties": {
                    "math_string": {
                        "type":
                            "string",
                        "description":
                            "A string that solves a math problem that conforms with python syntax that could be passed directly to an eval() function",
                    },
                },
                "required": ["math_string"],
            },
        },
    },
]
