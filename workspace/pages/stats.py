import streamlit as st

if 'history' in st.session_state:
    
    st.write([text.get_rating() for i, text in sorted(st.session_state['texts'].items())])

else:
    st.write("No history available")