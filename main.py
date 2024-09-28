import streamlit as st
import pandas as pd
import numpy as np
from scrape import (
    scrape_website,
    split_dom_content,
    clean_body_content,
    extract_body_content
)
from parse import parse_with_ollama

# Streamlit UI
st.title("Quét dữ liệu của mọi website bạn thấy bằng AI")
url = st.text_input("Điền URL của Website vào đây")

# Bước 1: quét website
if st.button("Bắt đầu quét"):
    st.write("Đang quét chờ tí...")
    
    result = scrape_website(url)
    print(result)

     # quét website
    dom_content = scrape_website(url)
    body_content = extract_body_content(dom_content)
    cleaned_content = clean_body_content(body_content)

        # Store the DOM content in Streamlit session state
    st.session_state.dom_content = cleaned_content

        # Display the DOM content in an expandable text box
    with st.expander("Xem DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)
    
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse here: ")

    if st.button("Parse content"):
        if parse_description:
            st.write("Parsing the content")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)