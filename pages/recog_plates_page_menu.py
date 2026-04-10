import streamlit as st
from library.init_display import *

converted = False

# Main menu of Face Recognition
if __name__ == "__main__":
    with st.container():
        
        # Header text: Face Recognition
        st.markdown("""<div id="title_main" class="header1">
                Number Plate Recognition</div>
                <style>
                #title_main {
                    font-family: "Source Sans Pro", sans-serif;
                    font-size: 35px;
                    font-weight: bold;
                }
                </style>
        """, unsafe_allow_html=True)
    st.markdown("---")    
    
    pn1, pn2, pn3 = st.columns(3)
    
    # Left panel: press button to direct to page Image
    with pn1:
        if st.button("Image", key="img_but"):
            st.switch_page("pages/recog_plates_page_img.py")

    # Right panel: press button to direct to page Video
    with pn2:
        if st.button("Video", key="vd_but"):
            st.switch_page("pages/recog_plates_page_vd.py")
            
    with pn3:
        if st.button("Real Time", key="rt_but"):
            st.switch_page("pages/recog_plates_page_rt.py")
    
    # Build and decorate background and sidebar
    display_background()
    display_sidebar()
