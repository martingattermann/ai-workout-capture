import streamlit as st
import uuid
import yaml
import openai

with open('secrets.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# TODO: openai auth
openai.organization = config['openai']['organization']
openai.api_key = config['openai']['api_key']

#TODO: functions
def generate_msg(role, content):
    msg = {}
    msg["role"] = role
    msg["content"] = content
    return msg

def chat_response(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0
    )
    return response

def add_massage(massage):
    st.session_state.wt.append(message)
    completion = chat_response(st.session_state.wt)
    st.session_state.wt.append(completion.choices[0].message)

# TODO: session state
if "wt" not in st.session_state:
    st.session_state.wt = []
    initial_system_msg = generate_msg("system", """Your task is to create a workout log after the user have entered all informations about a workout. The workout includes exercise. Each exercise have a list of sets, with sets consisting of reps and weight./
                                                Your response is gental and motivating. Ask the user for the name of the exercise. Ask the user for the number of sets. Ask the user for the number of reps and weight for each set.""")

    st.session_state.wt.append(initial_system_msg)

if "id_user" not in st.session_state:
    st.session_state.id_user = uuid.uuid4()

if "id_system" not in st.session_state:
    st.session_state.id_system = uuid.uuid4()

# TODO: layout
st.title("AI Training log")
st.header('Log your training')

col1_chat, col2_input = st.columns(2)

with col2_input:
    c_input_user = st.container()
    prompt_user = c_input_user.text_area(label="Prompt User", value="", key=st.session_state.id_user, label_visibility="visible")

    c_buttons_user = st.container()
    with c_buttons_user:
        col_chat, col_prompt = st.columns(2)

        with col_chat:
            button_send_user = st.button('Send')

        with col_prompt:
            button_end_user = st.button('End Training')

    c_input_system = st.container()
    prompt_system = c_input_system.text_area(label="Prompt System", value="", key=st.session_state.id_system, label_visibility="visible")

    c_buttons_system = st.container()
    with c_buttons_system:
        col_chat, col_prompt = st.columns(2)

        with col_chat:
            button_send_system = st.button('Send System')

if button_send_user:
    message = generate_msg("user", prompt_user)
    add_massage(message)

if button_send_system:
    message = generate_msg("system", prompt_system)
    add_massage(message)

if button_end_user:
    message = generate_msg("system", "Check if every information for the workout is added. If not, ask for the missing information. If yes, end the training./")
    add_massage(message)

with col1_chat:
    c_chat = st.container()

    with c_chat:
        for i in reversed(st.session_state.wt):
            if  st.session_state.wt.index(i) >= (len(st.session_state.wt) -1):
                if i['role'] == 'system':
                    pass
                else:
                    id_chat = uuid.uuid4()
                    st.text_area(label=i['role'], value=i['content'], key=id_chat, height=200, disabled=True, label_visibility="visible")
            else:
                if i['role'] == 'system':
                    pass
                else:
                    id_chat = uuid.uuid4()
                    st.text_area(label=i['role'], value=i['content'], key=id_chat, disabled=True, label_visibility="visible")