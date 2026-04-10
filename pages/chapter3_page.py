import streamlit as st
import numpy as np
from library.init_display import *
from library.chapter3 import *
from PIL import Image

converted = False               # True after Convert button is pressed

if __name__ == "__main__":
    
    # Header text: Chapter 3
    with st.container():
        st.markdown("""<div id="title_main" class="header1">
                Chapter 3</div>
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
    img_file = st.file_uploader("Upload a file", label_visibility="hidden", key="file_uploader", type=img_allowable_types)
    img_width = st.slider("Image Width", 0, 500, 250, 10)
    
    # Selectbox
    c3_options = ["Negative", "Logarit", "Power", "Negative Color", "PiecewiseLine", "Histogram", "Histogram Equalization",
              "Local Histogram", "Histogram Statistics", "Box Filter", "Gaussian Filter", "Median Filter", "Segmentation", "Sharpen", "Gradient"]
    c3_select = st.selectbox(
            "",
            c3_options,
            index=None,
            key="c3_selectbox"
        )
    
    pn1, pn2 = st.columns(2)
    
    # Left panel: show original image
    with pn1:
        if c3_select:
            
            # Process image if image is not browsed
            if img_file is None:
                match c3_select:
                    case "Negative":
                        img_file = Image.open("images\\c3_images\\Fig0304(a)(breast_digital_Xray).tif")
                    case "Logarit":
                        img_file = Image.open("images\\c3_images\\Fig0308(a)(fractured_spine).tif")
                    case "Power":
                        img_file = Image.open("images\\c3_images\\Fig0309(a)(washed_out_aerial_image).tif")
                    case "Negative Color":
                        img_file = Image.open("images\\c3_images\\Fig0635(top_ left_flower).tif")
                    case "PiecewiseLine":
                        img_file = Image.open("images\\c3_images\\Bear.jpg")
                    case "Histogram":
                        img_file = Image.open("images\\c3_images\\Fig0316(1)(top_left).tif")
                    case "Histogram Equalization":
                        img_file = Image.open("images\\c3_images\\Bear.jpg")
                    case "Local Histogram":
                        img_file = Image.open("images\\c3_images\\Fig0326(a)(embedded_square_noisy_512).tif")
                    case "Histogram Statistics":
                        img_file = Image.open("images\\c3_images\\Fig0326(a)(embedded_square_noisy_512).tif")
                    case "Box Filter":
                        img_file = Image.open("images\\c3_images\\Fig0335(a)(ckt_board_saltpep_prob_pt05).tif")
                    case "Gaussian Filter":
                        img_file = Image.open("images\\c3_images\\Fig0335(a)(ckt_board_saltpep_prob_pt05).tif")
                    case "Median Filter":
                        img_file = Image.open("images\\c3_images\\Fig0335(a)(ckt_board_saltpep_prob_pt05).tif")
                    case "Segmentation":
                        img_file = Image.open("images\\c3_images\\Fig0334(a)(hubble-original).tif")
                    case "Sharpen":
                        img_file = Image.open("images\\c3_images\\Fig0338(a)(blurry_moon).tif")
                    case "Gradient":
                        img_file = Image.open("images\\c3_images\\Fig0342(a)(contact_lens_original).tif")
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
                if c3_select:
                    if st.button("Convert", key="conv_but"):
                        match c3_select:
                            case "Negative":
                                imgout = Negative(frame)
                            case "Logarit":
                                imgout = Logarit(frame)
                            case "Power":
                                imgout = Power(frame)
                            case "Negative Color":
                                imgout = NegativeColor(frame)
                            case "PiecewiseLine":
                                imgout = PiecewiseLine(frame)
                            case "Histogram":
                                imgout = histogram(localHist(frame))
                            case "Histogram Equalization":
                                imgout = HisEqual(frame)
                            case "Local Histogram":
                                imgout = localHist(frame)
                            case "Histogram Statistics":
                                imgout = histStat(frame)
                            case "Segmentation":
                                imgout = phan_nguong(frame) 
                            case "Sharpen":
                                imgout = Sharp(frame)
                            case "Gradient":
                                imgout = Gradient(frame)       
                            case "Box Filter":
                                imgout = cv2.boxFilter(frame, cv2.CV_8UC1, (21,21))
                            case "Gaussian Filter":
                                imgout = cv2.GaussianBlur(frame, (43,43), 7.0)  
                            case "Median Filter":
                                imgout = cv2.medianBlur(frame, 3)      
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
