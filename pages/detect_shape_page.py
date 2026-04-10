import streamlit as st
from library.init_display import *
from library.shape import *
from PIL import Image

converted = False

if __name__ == "__main__":
    
    # Header text: Shape Detection
    with st.container():
        st.markdown("""<div id="title_main" class="header1">
                Shape Detection</div>
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
    img_width = st.slider("Image Width", 0, 500, 500, 10)
    
    pn1, pn2 = st.columns(2)
    
    # Left panel: show original image
    with pn1:
        try:      
            if img_file is not None:
                st.image(img_file, width = img_width)
                img = Image.open(img_file)
                frame = np.array(img)
                
                # Begin detecting if button is pressed
                if st.button("Detect", key="conv_but"):
                    imgout = DetectShape(frame)
                converted = True
        except:
            pass

    # Right panel: show image with detected shapes             
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
