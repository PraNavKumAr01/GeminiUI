import os
import streamlit as st
os.environ['GOOGLE_API_KEY'] = st.secrets['apikey']
from PIL import Image
import google.generativeai as genai


# Function to generate content using the model
def generate_content(user_prompt, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    try:
        response = model.generate_content([prompt, image], stream=True)
        response.resolve()
        result = response.text
    except Exception as e:
        # Handle the exception when an error occurs
        result = "Image size exceeded (Max Size : 20MB)"
        
    return result


def generate_text(user_prompt):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    response = chat.send_message(f"{user_prompt}")
    return response.text


def main():
    # APP FRAMEWORK
    st.title("🤖MultiModal AI💻")

    selected_page = st.sidebar.radio("Select a page", ["Text Chat", "Image Chat"])

    if selected_page == "Text Chat":
        st.header("Let me show you my conversational capabilities")

        # Input prompt for chat
        chat_prompt = st.text_area("Write a prompt")

        if st.button("Generate Response"):
            result = generate_text(chat_prompt)

            # Display the generated response
            st.subheader("Generated Response : ")
            st.write(result)

    elif selected_page == "Image Chat":

        prompt = st.text_input("Enter your input")

        with st.sidebar:
            uploaded_image = st.file_uploader("Choose a file")

            if uploaded_image:
                # Open the uploaded image using PIL
                img = Image.open(uploaded_image)

                # Display the uploaded image
                st.image(img, caption="Uploaded Image", use_column_width=True)

        # Check if there's a prompt and/or an uploaded image
        if prompt and uploaded_image:
            # Open the uploaded image using PIL
            img = Image.open(uploaded_image)

            # Generate content using prompt and image
            result = generate_content(prompt, img)

            # Display the generated content
            st.subheader("Generated Content:")
            st.write(result)


# Run the Streamlit app
if __name__ == "__main__":
    main()
