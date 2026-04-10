import streamlit as st
from library.init_display import *
from library.recog_plates import *

converted = False           # True after Detect button is pressed

# Face Recognition: Video
if __name__ == "__main__":
    
    # Header text: Number Plate Recognition
    with st.container():
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
        
    # Subheader text: Video
    st.markdown("""<div id="member_main" class="header1">
            Video</div>
            <style>
            #member_main {
                font-family: "Source Sans Pro", sans-serif;
                font-size: 20px;
                padding-left: 50px;
            }
            </style>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Upload file
    vd_file = st.file_uploader("Upload a file", label_visibility="collapsed", key="file_uploader", type=['mp4'])
        
    pn1, pn2 = st.columns(2)
    
    # Left panel: shows original video
    with pn1:
        try:      
            if vd_file is not None:
                
                # Convert file .mp4 to proper file to show on panel 
                vd_bytes = vd_file.read()
                st.video(vd_bytes)
                output_path = "videos/out_plates1.mp4"         # Create an output file .mp4 for processing and showing
                    
                # Begin detecting if button is pressed
                if st.button("Detect", key="conv_but"):
                    converted = True
        except:
            pass
    
    # Right panel: shows processed video
    with pn2:
        if converted:
            with st.spinner("Processing video..."):
                    success = Recog_Video_Plates(os.path.join("videos", vd_file.name), output_path)
            
            # After output file .mp4 is created, shows it on panel and then delete the file
            if success:
                st.video(output_path)
                # os.unlink(output_path)
            converted = False
            
    # Build and decorate background and sidebar
    display_background()
    display_sidebar()
