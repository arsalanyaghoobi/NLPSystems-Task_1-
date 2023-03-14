import asyncio
import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
from spacy import displacy

async def bodyConfig():
    st.set_page_config(page_title="Reilans Corporation", page_icon=":guardsman:", layout="centered")
    # Header section:
    await sideBarconfig()
    st.header("Reilans Corporation")
    st.subheader("We are the number one AI company in the world")
    st.title(" You are contacting our NER section; please enter your data in the bar below:  ")
    inputData = st.text_input(label="Please enter your data here!: ")
    if len(inputData) > 0:
        result = NER_Spacy(inputData)
        html = displacy.render(result, style='ent')
        with open('result.html', 'w', encoding='utf-8') as f:
            f.write(html)
        st.components.v1.html(open('result.html', 'r', encoding='utf-8').read(), height=500)
    else:
        st.write("Make sure you have tested our NER models! You will love it. Promised! ")

    link = 'https://www.linkedin.com/in/arsalan-yaghoubi-766911119/'
    text = 'FOR OTHER SERVICES CLICK HERE '
    st.markdown(f'<a href="{link}" target="_blank" style="text-decoration:none; color:Red; font-size:15px;">{text}</a>', unsafe_allow_html=True)



    # Define CSS style for the container
    bottom_container_style = """
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: gray;
        text-align: center;
        padding: 20 px;
    """
    # Create the container and apply the style
    bottom_container = st.container()
    bottom_container.markdown("<div style='" + bottom_container_style + "'> \U0001F33A Call Reilans Corporation at +1-781-520-3534 \U0001F33A", unsafe_allow_html=True)



def sidebarQuestionare():
    st.sidebar.write("Please choose level of satisfaction with this website: ")
    satisfaction_level = st.sidebar.slider("Choose your level of satisfaction: ", 0, 10, 5)
    if satisfaction_level >= 8:
        st.sidebar.write("We are happy that you liked the website! Please let us know what has made you to thin kpositive about us!")
        idea = st.sidebar.text_input("Enter your idea:")
    else:
        st.sidebar.write("We are so sorry that you are not satisfied with our website; please let us know how to improve our services here! ")
        idea = st.sidebar.text_input("Enter your idea:")

    return idea, satisfaction_level


async def sideBarconfig():
    conn = sqlite3.connect('mydb.db')
    df = pd.DataFrame(columns=["Name", 'Contact_info', "Ethnicity", "Score", "Idea"])
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.markdown(f'<p style="color:Red"><b> TIME:{current_time}</b></p>', unsafe_allow_html=True)

    st.sidebar.button("**Need us to contact you? Complete the form below** ")
    full_name = st.sidebar.text_input("Enter your full name: ")
    ethnicity_option = ["Earth", "Heaven", "Mars", "None"]
    ethnicity = st.sidebar.radio("Choose your ethnicity: ", ethnicity_option, index=3)
    Contact_info = st.sidebar.selectbox(
        "How would you like us to contact you? ",
        ("Email", "Home phone", "Mobile phone"))
    option = ['Yes', 'No', 'None']
    if Contact_info == "Email":
        email = st.sidebar.text_input("Please Enter your Email: ")
        new_data = {"Name": full_name, 'Contact_info': email, "Ethnicity": ethnicity, "Score": None, "Idea": None}
        st.sidebar.write("Please make sure that your e-mail is correct? ")
        yes_or_no = st.sidebar.radio('Do you confirm that your e-mail is correct ?', option, index=2)
        if yes_or_no == "Yes":
            for key, val in new_data.items():
                if  type(val) != int  and key != "Score" and key != "Idea" and len(val) == 0:
                    raise ValueError(
                        'You have not submitted your ***** ' + key + ' ***** information correctly! Try it again.')
        elif yes_or_no == "None":
            st.sidebar.write('Dont forget to confirm you contact information in the above section! ')
        else:
            st.sidebar.write('Please submit your accurate contact information, so that we can contact you ASAP!')

    elif Contact_info == " Home phone":
        home_phone = st.sidebar.text_input("Please Enter your home phone: ")
        new_data = {"Name": full_name, 'Contact_info': home_phone, "Ethnicity": ethnicity, "Score": None,
                    "Idea": None}
        st.sidebar.write("Please make sure that your Home phone is correct ? ")
        yes_or_no = st.sidebar.radio('Do you confirm that your home phone is correct ?', option, index=2)
        if yes_or_no == "Yes":
            for key, val in new_data.items():
                if  type(val) != int and key != "Score" and key != "Idea" and len(val) == 0 :
                    raise ValueError(
                        'You have not submitted your ***** ' + key + ' ***** information correctly! Try it again.')
        elif yes_or_no == "None":
            st.sidebar.write('Dont forget to confirm you contact information in the above section! ')
        else:
            st.sidebar.write('Please submit your accurate contact information, so that we can contact you ASAP!')
    else:
        mobile_phone = st.sidebar.text_input("Please Enter your Mobile phone: ")
        new_data = {"Name": full_name, 'Contact_info': mobile_phone, "Ethnicity": ethnicity, "Score": None,
                    "Idea": None}
        st.sidebar.write("Please make sure that your Mobile phone is correct? ")
        yes_or_no = st.sidebar.radio('Do you confirm that your mobile phone is correct ?', option, index=2)
        if yes_or_no == "Yes":
            for key, val in new_data.items():
                if type(val) != int  and key != "Score" and key != "Idea" and len(val) == 0:
                    raise ValueError(
                        'You have not submitted your ***** ' + key + ' ***** information correctly! Try it again.')
        elif yes_or_no == "None":
            st.sidebar.write('Dont forget to confirm you contact information in the above section! ')
        else:
            st.sidebar.write('Please submit your accurate contact information, so that we can contact you ASAP!')
    idea, score = sidebarQuestionare()
    new_data["Score"] = score
    new_data["Idea"] = idea



    if st.sidebar.button("click for submission!"):
        for key, val in new_data.items():
            if type(val) != int and len(val) == 0:
                raise ValueError('You have not submitted your information! There is nothing be submitted!')
        st.sidebar.write('You submitted your information to our website and we will contact you ASAP')
        dataf = df.append(new_data, ignore_index=True)
        dataf.to_sql(name="ReilansDatabase", con=conn, if_exists='append', index=False)
        conn.commit()
        dataf = pd.read_sql("SELECT * FROM ReilansDatabase", conn)
        st.write(dataf)
        st.snow()
        conn.close()
    else:
        st.sidebar.write("Please make sure you have submitted your information")




def emptyDatabaseCache():
    conn = sqlite3.connect('mydb.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ReilansDatabase;")
    conn.commit()
    conn.close()


def NER_Spacy(data):
    import spacy
    nlp = spacy.load('en_core_web_sm')
    document = nlp(data)
    return document

if __name__ == '__main__':
    asyncio.run(bodyConfig())
    # emptyDatabaseCache() # uncommenting this will clean the whole previous records

