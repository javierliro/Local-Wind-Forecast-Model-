import streamlit as st
import app1
import app2


#menu=['Home','about']
#choice=st.sidebar.selectbox('Menu',menu)
#if choice=='about':
#    st.text('blabla')
    
st.set_page_config(layout="wide")
    
PAGES = {
    "Wind Forecast": app1,
    "Wind Station": app2
}
st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Menu", list(PAGES.keys()))
page = PAGES[selection]
page.app()