
import streamlit as st
import google.generativeai as genai
import os8
from dotenv import load_dotenv
from PIL import Image

load_dotenv() 

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def getFoodInfo(input_prompt, image):
    gemini_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = gemini_model.generate_content([input_prompt, image[0]]) 
    return response.text  

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type, 
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Calories Counter")
st.header("Calories Counter")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert nutritionist where you need to see the food items from the image, evaluate what you think the
serving size is, and based on each food item and the serving amount of each food, calculate the total calories, also provide the details of every
food item with calories intake in the below format:

1. Item 1 - number of calories
2. Item 2 - number of calories

      ----
      ----

Finally, mention whether the food is healthy or not.
"""

if submit and uploaded_file is not None:
    image_data = input_image_setup(uploaded_file)
    response = getFoodInfo(input_prompt, image_data)
    st.header("The Response is")
    st.write(response)
