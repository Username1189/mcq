import streamlit as st
import os

c = st.text_input("Enter Your Name:")
s = st.button("Submit")
if s:
    with open("name", "w") as file:
        content = c
        file.write(content)
        file.close()
        os.system("streamlit run questions.py")
