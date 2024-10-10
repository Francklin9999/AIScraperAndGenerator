import streamlit as st
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_text_with_ollama, parse_image_prompt_with_ollama
from flux1schnell.image_generator import generate_image


st.title("AI-Driven ImageScrape")
st.write("This is a web scraper that uses AI to extract relevant information from a website and generate and image using the scrape content.")

url = None
text = None

input_method = st.radio("Select Input Method:", ("Scrape from URL", "Use Text Input"))

if input_method == "Scrape from URL":
    url = st.text_input("Enter a Website URL: ")
    text = None  
else:
    url = None 
    text = st.text_area("Enter a description: ")

isGenerateImage = st.checkbox("Generate Image")


if st.button("Generate"):
    st.write("Generating...")

    if input_method == "Scrape from URL":
        result = scrape_website(url)
        body = extract_body_content(result)
        cleaned_content = clean_body_content(body)

        st.session_state.dom_content = cleaned_content
        st.write("Generated")
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)

    else:
        if text:
            st.session_state.dom_content = text
            st.write("Generated")
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", text, height=300)
        else:
            st.error("Please enter a description.")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Descrive what you want to parse?")

    if st.button("Parse Content"):
        st.write("Parsing the content...")

        dom_chunks = split_dom_content(st.session_state.dom_content)
        result = parse_text_with_ollama(dom_chunks, parse_description)
        st.write(result)

        if isGenerateImage:
            st.write("Generating the image...")
            prompt = parse_image_prompt_with_ollama(parse_description)
            image = generate_image(prompt, 1)
            st.image(image, caption="Generated Image", use_column_width=True)

