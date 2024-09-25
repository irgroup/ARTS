import streamlit as st
import pickle
import numpy as np
import pandas as pd
from utils import Text, handle_scores, apply_history
import os
from datetime import datetime
import glob

def _login():
    st.session_state['name'] = st.session_state["login_name"]
    #try to load history
    path = f"/workspace/{st.session_state['name']}-{st.session_state['ds_version']}_history.pkl"

    data_path = f"/workspace/data/ARTS_only_texts_{st.session_state['ds_version']}.pkl"

    data = pickle.load(open(data_path, "rb"))
    st.session_state['texts'] = {t_id : Text(t_id, text[0]) for t_id, text in data.iterrows()}
    if os.path.exists(path):
        
        st.session_state['history'] = pickle.load(open(path, "rb"))
        st.session_state['current_match_id'] = len(st.session_state['history'].keys())
        apply_history(st.session_state['history'], st.session_state['texts'])
    else:
        #user does not exist
        st.session_state['history'] = {}
        st.session_state['current_match_id'] = 0

    _init()

def _init():
    det_pairs_path = f"data/determined_pairs_{int(st.session_state['ds_version'])*4}.pkl"
    st.session_state['determined_pairs'] = pickle.load(open(det_pairs_path, "rb"))

    if st.session_state['current_match_id'] >= len(st.session_state['determined_pairs']):
        st.session_state['current_match_id'] = len(st.session_state['determined_pairs'])-1
        st.write("You are done labeling the dataset")

    #now deterministic
    st.session_state['can_a'],  st.session_state['can_b'] = st.session_state['determined_pairs'][st.session_state['current_match_id']]

def _update_history(winner):
    system_time = datetime.now().strftime("%H:%M:%S")
    st.session_state['history'][st.session_state['current_match_id']] = ((st.session_state['can_a'], st.session_state['can_b']), st.session_state[f'can_{winner}'], system_time)
    st.session_state['current_match_id'] +=1
    if st.session_state['current_match_id'] >= len(st.session_state['determined_pairs']):
        _save_history()
        st.session_state['current_match_id'] = len(st.session_state['determined_pairs'])-1
        st.write("You are done labeling the dataset")

    if winner == 'a':
        handle_scores(st.session_state['texts'][st.session_state['can_a']], st.session_state['texts'][st.session_state['can_b']])
    elif winner == 'b':
        handle_scores(st.session_state['texts'][st.session_state['can_b']], st.session_state['texts'][st.session_state['can_a']])

def _get_new_pair(winner="init"):
    _update_history(winner)
    st.session_state['can_a'],  st.session_state['can_b'] = st.session_state['determined_pairs'][st.session_state['current_match_id']]

def _save_history():

    path = f"/workspace/{st.session_state['name']}-{st.session_state['ds_version']}_history.pkl"
    pickle.dump(st.session_state['history'], open(path, "wb"))



if "name" in st.session_state:

    if 'current_match_id' in st.session_state and 'determined_pairs' in st.session_state:
        finished = st.session_state['current_match_id']
        total = len(st.session_state['determined_pairs'])
        st.header(f'Click on the text which is easier to understand ({finished+1}/{total})', divider='rainbow')
    else:
        st.header('Click on the text which is easier to understand', divider='rainbow')

    
    tab1, tab2 = st.columns(2)
    i_a, i_b = st.session_state['can_a'], st.session_state['can_b']

    can_a_text = f"{i_a}: {st.session_state['texts'][i_a].get_text()}"
    can_b_text = f"{i_b}: {st.session_state['texts'][i_b].get_text()}"

    #changed winner as the user should click on the easier text now: winner is the harder text as a high score should indicate high complexity
    with tab1:
        st.button(can_a_text, key="b_can_a", on_click=_get_new_pair, args=("b",))

    with tab2:
        st.button(can_b_text, key="b_can_b", on_click=_get_new_pair, args=("a",))

    st.sidebar.button("Save history", on_click=_save_history)

else:
    
    #load all datasets
    avail_dataset_paths = sorted(glob.glob("/workspace/data/*_only_texts*"), key = lambda x: int(x.split("_")[-1].replace(".pkl", "")))
    ds_names = [path.split("/")[-1].replace(".pkl", "") for path in avail_dataset_paths]

    st.session_state['ds_version'] = st.sidebar.selectbox('Select a dataset', ds_names).split("_")[-1]

    st.sidebar.text_input("Username", key="login_name")
    st.sidebar.button("Login", on_click=_login)


st.sidebar.subheader("Simplicity:")
st.sidebar.write("Imagine you are writing an exam where you are allowed to google and where the task is to understand the two given texts.")
st.sidebar.subheader("Which of the two texts...")
st.sidebar.markdown("* generates less cognitive load?")
st.sidebar.markdown("* can you understand more quickly?")
st.sidebar.markdown("* are you more confident to answer questions about?")
st.sidebar.markdown("* is easier for you to reformulate without changing the meaning?")
