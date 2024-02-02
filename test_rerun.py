import streamlit as st


if 'index' not in st.session_state:
    st.session_state.index = 0


selected = st.selectbox(label='Commune', options=['', 'a', 'b'], index=st.session_state.index)

res = st.radio('test', ['', 'a', 'b'])
st.info(res)

if res == 'a':
    st.session_state.index = 1
    st.experimental_rerun()

if res == 'b':
    st.session_state.index = 2
    st.experimental_rerun()