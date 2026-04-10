import streamlit as st
from library.init_display import *
from library.recog_faces import *

converted = False

# Face Recognition: Real Time
if __name__ == "__main__":
    
    # Header text: Face Recognition
    with st.container():
        st.markdown("""<div id="title_main" class="header1">
                Face Recognition</div>
                <style>
                #title_main {
                    font-family: "Source Sans Pro", sans-serif;
                    font-size: 35px;
                    font-weight: bold;
                }
                </style>
        """, unsafe_allow_html=True)
        
    # Subheader text: Real Time
    st.markdown("""<div id="member_main" class="header1">
            Real Time</div>
            <style>
            #member_main {
                font-family: "Source Sans Pro", sans-serif;
                font-size: 20px;
                padding-left: 50px;
            }
            </style>
    """, unsafe_allow_html=True)
    st.markdown("---")
        
    pn1, pn2 = st.columns(2)
    
    # Build and decorate background and sidebar
    display_background()
    display_sidebar()
    
    # Left panel: original image from webcam
    with pn1:
        try:
            frame_placeholder1 = st.empty()
        except:
            pass
             
    # Right panel: image with detected faces from webcam
    with pn2:
        try:
            frame_placeholder2 = st.empty()
        except:
            pass
        
    # Load available .pkl file which stores feature information of faces and corresponding names
    load_pickle("library/known_faces.pkl")
    
    # Turn on webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Could not open webcam or video source.")
    else:
        ret, frame = cap.read()
        h, w = frame.shape[:2]
        face_detector.setInputSize((w, h))

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            st.warning("Failed to read frame from webcam. Please verify the webcam is connected properly.")
            break

        frame_placeholder1.image(frame, channels="BGR")  # Display original frame on left panel
        frame = Recog_Faces(frame)
        frame_placeholder2.image(frame, channels="BGR")  # Display processed frame on right panel
