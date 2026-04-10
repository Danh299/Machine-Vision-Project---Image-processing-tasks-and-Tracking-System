import streamlit as st
import numpy as np
import cv2
from library.init_display import *
from library.chapter5 import *
from PIL import Image

converted = False               # True after Convert button is pressed

if __name__ == "__main__":
    
    # Header text: Chapter 5
    with st.container():
        st.markdown("""<div id="title_main" class="header1">
                Chapter 5</div>
                <style>
                #title_main {
                    font-family: "Source Sans Pro", sans-serif;
                    font-size: 35px;
                    font-weight: bold;
                }
                </style>
        """, unsafe_allow_html=True)
    st.markdown("---")

    # Upload file and width slider
    img_file = st.file_uploader("Upload a file", label_visibility="collapsed", key="file_uploader", type=img_allowable_types)
    img_width = st.slider("Image Width", 0, 500, 250, 10)
    
    # Selectbox
    c5_options = ["CreateMotion", "DeMotion"]
    c5_select = st.selectbox(
            "",
            c5_options,
            index=None,
            key="c5_selectbox"
        )
    
    pn1, pn2 = st.columns(2)
    
    # Left panel: show original image
    with pn1:
        if c5_select:
            
            # Process image if image is not browsed
            if img_file is None:
                match c5_select:
                    case "CreateMotion":
                        img_file = Image.open("images\\c5_images\\Fig0526(a)(original_DIP).tif")
                    case "DeMotion":
                        img_file = Image.open("images\\c5_images\\Fig0529(g)(least_noise_var_10minus37).tif")
                img = img_file
            else:
                img = Image.open(img_file)
        
        try:      
            if img_file is not None:
                st.image(img_file, width = img_width)
                
                # Create new output image copied from input image, if datatype is bool then convert to uint8
                frame = np.array(img)
                if(frame.dtype == bool):
                    frame = np.array(frame, dtype=np.uint8)
                    _, frame = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY)
                    
                # Process output image
                if c5_select:
                    if st.button("Convert", key="conv_but"):
                        match c5_select:
                            case "CreateMotion":
                                imgout = CreateMotion(frame)
                            case "DeMotion":
                                imgout = DeMotion(frame)
                converted = True
        except:
            pass
             
    # Right panel: show processed image
    with pn2:
        try: 
            if converted:
                st.image(imgout, width = img_width)
                converted = False
        except:
            pass
    
    # Build and decorate background and sidebar
    display_background()
    display_sidebar()
