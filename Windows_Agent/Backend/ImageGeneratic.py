import asyncio
import os
import requests
from random import randint
from PIL import Image
from dotenv import dotenv_values
from time import sleep

# Load API key from .env
env_vars = dotenv_values(".env")
API_KEY = env_vars.get("Huggingfaceapikey")

if not API_KEY:
    raise ValueError("Hugging Face API key not found in .env file!")

# API URL for Stable Diffusion XL
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {API_KEY}"}

def open_images(prompt):
    """Opens the generated images using the default system viewer."""
    folder_path = os.path.join("Data", "image_gen")
    prompt_filename = prompt.replace(" ", "_")
    
    # We generated 4 images, let's try to open them
    for i in range(1, 5):
        image_path = os.path.join(folder_path, f"{prompt_filename}{i}.jpg")
        try:
            if os.path.exists(image_path):
                img = Image.open(image_path)
                print(f"Displaying: {image_path}")
                img.show()
                sleep(0.5)
        except Exception as e:
            print(f"Error opening {image_path}: {e}")

async def query(payload):
    """Sends the request to Hugging Face API."""
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def gen_image(prompt: str):
    """Handles the asynchronous generation of 4 images."""
    tasks = []
    folder_path = os.path.join("Data", "image_gen")
    os.makedirs(folder_path, exist_ok=True) # Ensure folder exists

    print(f"Requesting images for: {prompt}...")

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, 4k, cinematic, highly detailed, high resolution, seed={randint(0, 10**9)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        image_name = f"{prompt.replace(' ', '_')}{i + 1}.jpg"
        image_path = os.path.join(folder_path, image_name)
        with open(image_path, "wb") as f:
            f.write(image_bytes)
    
    print(f"Successfully saved 4 images to {folder_path}")

def generate_image(prompt: str):
    """Synchronous wrapper to run the async generation."""
    asyncio.run(gen_image(prompt))
    open_images(prompt)

def image_generation_listener():
    """Listens for commands written to ImageGeneration.data by the main assistant."""
    data_file = os.path.join("Frontend", "Files", "ImageGeneration.data")
    
    print("--- Image Generation Service Active ---")
    while True:
        try:
            if os.path.exists(data_file):
                with open(data_file, "r") as f:
                    content = f.read().strip()

                if content and "," in content:
                    prompt, status = content.split(",")

                    if status.strip().lower() == "true":
                        print(f"Trigger detected! Generating: {prompt}")
                        generate_image(prompt=prompt)

                        # Reset the file so it doesn't loop infinitely
                        with open(data_file, "w") as f:
                            f.write("None,False")
            
            sleep(1)
        except Exception as e:
            print(f"Service Error: {e}")
            sleep(2)

if __name__ == "__main__":
    image_generation_listener()