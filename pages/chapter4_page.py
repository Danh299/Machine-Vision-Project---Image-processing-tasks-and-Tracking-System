import streamlit as st
import numpy as np
from library.init_display import *
from library.chapter4 import *
from PIL import Image

converted = False               # True after Convert button is pressed

if __name__ == "__main__":
    
    # Header text: Chapter 4
    with st.container():
        st.markdown("""<div id="title_main" class="header1">
                Chapter 4</div>
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
    c4_options = ["Spectrum", "Draw Notch Filter", "Remove Moire Simple", "Remove Period Noise"]
    c4_select = st.selectbox(
            "",
            c4_options,
            index=None,
            key="c4_selectbox"
        )
    
    pn1, pn2 = st.columns(2)
    
    # Left panel: show original image
    with pn1:
        if c4_select:
            
            # Process image if image is not browsed
            if img_file is None:
                match c4_select:
                    case "Spectrum":
                        img_file = Image.open("images\\c4_images\\Fig0421(car_newsprint_sampled_at_75DPI).tif")
                    case "Remove Moire Simple":
                        img_file = Image.open("images\\c4_images\\Fig0421(car_newsprint_sampled_at_75DPI).tif")
                    case "Draw Notch Filter":
                        img_file = Image.open("images\\c4_images\\Fig0421(car_newsprint_sampled_at_75DPI).tif")
                    case "Remove Period Noise":
                        img_file = Image.open("images\\c4_images\\Fig0465(a)(cassini).tif")
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
                if c4_select:
                    if st.button("Convert", key="conv_but"):
                        match c4_select:
                            case "Spectrum":
                                imgout = Spectrum(frame)
                            case "Remove Moire Simple":
                                imgout = RemoveMoireSimple(frame)
                            case "Draw Notch Filter":
                                imgout = DrawNotchFilter(frame)
                            case "Remove Period Noise":
                                imgout = RemovePeriodNoise(frame)
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
