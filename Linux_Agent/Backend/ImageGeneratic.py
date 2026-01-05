import asyncio
import os
import requests
import subprocess 
from random import randint
from PIL import Image
from dotenv import load_dotenv 
from pathlib import Path
from time import sleep


base_path = Path(__file__).resolve().parent.parent
env_path = base_path / ".env"
image_folder = base_path / "Data" / "image_gen"
data_file = base_path / "Frontend" / "Files" / "ImageGeneration.data"

# Ensure folders exist
image_folder.mkdir(parents=True, exist_ok=True)
data_file.parent.mkdir(parents=True, exist_ok=True)

# Load API key
load_dotenv(env_path)
API_KEY = os.getenv("Huggingfaceapikey")

if not API_KEY:
    raise ValueError(f"Hugging Face API key not found in {env_path}")

# API URL 
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {API_KEY}"}

def open_images(prompt):
    """Opens generated images using the system's default viewer."""
    prompt_filename = prompt.replace(" ", "_")
    
    for i in range(1, 5):
        image_path = image_folder / f"{prompt_filename}{i}.jpg"
        try:
            if image_path.exists():
                print(f"Displaying: {image_path}")
                if os.name == 'nt':
                    os.startfile(str(image_path))
                else:
                    # Native Linux viewer call
                    subprocess.Popen(['xdg-open', str(image_path)])
                sleep(0.5)
        except Exception as e:
            print(f"Error opening {image_path}: {e}")

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def gen_image(prompt: str):
    tasks = []
    print(f"🎨 Requesting images for: {prompt}...")

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, 4k, cinematic, highly detailed, seed={randint(0, 10**9)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):
        image_name = f"{prompt.replace(' ', '_')}{i + 1}.jpg"
        final_path = image_folder / image_name
        with open(final_path, "wb") as f:
            f.write(image_bytes)
    
    print(f"✅ Saved 4 images to {image_folder}")

def generate_image(prompt: str):
    asyncio.run(gen_image(prompt))
    open_images(prompt)

def image_generation_listener():
    """Listens for commands in ImageGeneration.data."""
    print(f"🔍 Monitoring: {data_file}")
    
    while True:
        try:
            if data_file.exists():
                with open(data_file, "r") as f:
                    content = f.read().strip()

                if content and "," in content:
                    prompt, status = content.split(",")

                    if status.strip().lower() == "true":
                        print(f"🚀 Trigger: {prompt}")
                        generate_image(prompt=prompt)

                        # Reset the file
                        with open(data_file, "w") as f:
                            f.write("None,False")
            
            sleep(1)
        except Exception as e:
            print(f"Service Error: {e}")
            sleep(2)

if __name__ == "__main__":
    image_generation_listener()