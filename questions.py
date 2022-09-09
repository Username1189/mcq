import streamlit as st
import pandas as pd
import smtplib

from functools import partial
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

df = pd.read_csv("questions.csv")
df2 = pd.read_csv("chosenAnswers.csv")


def check():
    score = 0
    totScore = 0
    i = 0
    for row in df2.iloc:
        if row["Chosen answer"] == df.iloc[i]["Answer"]:
            score += df.iloc[i]["Score"]
        else:
            score -= df.iloc[i]["NegScore"]
        totScore += df.iloc[i]["Score"]
        i += 1
    for row in df2.iloc:
        row["Chosen answer"] = ""
    df2.to_csv("chosenAnswers.csv", index=False)
    return f"{score}/{totScore}"


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def email(score):
    my_email = "sanjaymuthu12@gmail.com"
    password = "ofeiszesyjyozbfl"

    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    connection.login(user=my_email, password=password)

    msg = MIMEMultipart()

    with open("name", "r") as file:
        content = file.read()
    message_template = read_template('template')
    message = message_template.substitute(Name=content, Score=score)

    msg['From'] = my_email
    msg['To'] = "sanjaymuthudiscord@gmail.com"
    msg['Subject'] = "submit button cliked on questionpaper"

    msg.attach(MIMEText(message, 'plain'))

    connection.send_message(msg)

    del msg
    connection.close()


def submit():
    email(check())


def questions(pg_no):
    if pg_no == df.shape[0]+1:
        button_con = st.empty()
        s = button_con.button("Submit")
        if s:
            button_con.empty()
            submit()
            st.markdown("Submittion Done Plese Close This Tab")
        return
    question = df.iloc[pg_no-1]
    title = question["Question Title"]
    st.title(f"{pg_no}. {title}")
    selected_answer = st.selectbox("Select a answer", ["", question["Option 1"], question["Option 2"], question["Option 3"], question["Option 4"]])
    df2.loc[pg_no-1, "Chosen answer"] = str(selected_answer)
    df2.to_csv("chosenAnswers.csv", index=False)

page_names_to_funcs = {f"Question {i}": partial(questions, i) for i in range(1, df.shape[0]+2)}

selected_page = st.sidebar.selectbox("Select a question", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()