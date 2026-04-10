import streamlit as st
import numpy as np
from library.init_display import *
from library.chapter9 import *
from PIL import Image

converted = False               # True after Convert button is pressed

if __name__ == "__main__":
    
    # Header text: Chapter 9
    with st.container():
        st.markdown("""<div id="title_main" class="header1">
                Chapter 9</div>
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
    c9_options = ["Erosion", "Dilation", "Boundary", "Contour", "Convex Hull", "Defect Detect", "Hole Fill", "Connected Components", "Remove Small Rice"]
    c9_select = st.selectbox(
            "",
            c9_options,
            index=None,
            key="c9_selectbox"
        )
    
    pn1, pn2 = st.columns(2)
    
    # Left panel: show original image
    with pn1:
        if c9_select:
            
            # Process image if image is not browsed
            if img_file is None:
                match c9_select:
                    case "Erosion":
                        img_file = Image.open("images\\c9_images\\Fig0905(a)(wirebond-mask).tif")
                    case "Dilation":
                        img_file = Image.open("images\\c9_images\\Fig0907(a)(text_gaps_1_and_2_pixels).tif")
                    case "Boundary":
                        img_file = Image.open("images\\c9_images\\Fig0914(a)(licoln from penny).tif")
                    case "Contour":
                        img_file = Image.open("images\\c9_images\\Fig0914(a)(licoln from penny).tif")
                    case "Convex Hull":
                        img_file = Image.open("images\\c9_images\\Fig0914(a)(licoln from penny).tif")
                    case "Defect Detect":
                        img_file = Image.open("images\\c9_images\\Fig0914(a)(licoln from penny).tif")
                    case "Hole Fill":
                        img_file = Image.open("images\\c9_images\\Fig0916(a)(region-filling-reflections).tif")
                    case "Connected Components":
                        img_file = Image.open("images\\c9_images\\Fig0918(a)(Chickenfilet with bones).tif")
                    case "Remove Small Rice":
                        img_file = Image.open("images\\c9_images\\Fig0940(a)(rice_image_with_intensity_gradient).tif")
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
                if c9_select:
                    if st.button("Convert", key="conv_but"):
                        match c9_select:
                            case "Erosion":
                                imgout = erosion(frame)
                            case "Dilation":
                                imgout = dilation(frame)
                            case "Boundary":
                                imgout = Boundary(frame)
                            case "Contour":
                                imgout = Contour(frame)
                            case "Convex Hull":
                                imgout = ConvexHull(frame)
                            case "Defect Detect":
                                imgout = DefectDetect(frame)
                            case "Hole Fill":
                                imgout = HoleFill(frame)
                            case "Connected Components":
                                imgout = ConnectedComponents(frame)
                            case "Remove Small Rice":
                                imgout = RemoveSmallRice(frame)
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
