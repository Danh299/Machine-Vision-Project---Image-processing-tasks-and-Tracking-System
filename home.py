import streamlit as st
from library.init_display import *

if __name__ == "__main__":
    
    # Header text: Main title
    # Subheader text: Members name and MSSV 
    with st.container():
        st.markdown("""<div id="title_main" class="header1">
                Machine Vision Project</div>
                <style>
                #title_main {
                    font-family: "Source Sans Pro", sans-serif;
                    font-size: 35px;
                    font-weight: bold;
                }
                </style>
        """, unsafe_allow_html=True)
        
        st.subheader("Team Members: ")
        st.markdown("""<div id="member_main" class="header1">
                Nguyễn Công Danh - 22146280<br>
                Nguyễn Ngọc Độ - 22146294</div>
                <style>
                #member_main {
                    font-family: "Source Sans Pro", sans-serif;
                    font-size: 20px;
                    padding-left: 50px;
                }
                </style>
        """, unsafe_allow_html=True)
    st.markdown("---")

    pn1, pn2, pn3, pn4 = st.columns(4)

    # Decorate with images
    with pn1:
        st.image("images/logo_img/lena_color.gif")

    with pn2:
        st.image("images/logo_img/einstein.tif")
        
    with pn3:
        st.image("images/logo_img/pcb.tif")
        
    with pn4:
        st.image("images/logo_img/a.tif")
        
    # Build and decorate background and sidebar
    display_background()
    display_sidebar()
