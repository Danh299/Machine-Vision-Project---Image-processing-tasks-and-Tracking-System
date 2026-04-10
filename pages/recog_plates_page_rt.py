import streamlit as st
from library.init_display import *
from library.recog_plates import *

begin = False

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
        
    camera_device = st.text_input("Enter IP: ", "http://10.166.0.180:8080/video")
    if st.button("Record", key="conv_but"):
        begin = True
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
    car_tracker, plate_tracker = Initialize_Recog_Plates('library/yolo_plate.pt')

    # Turn on webcam
    cap = cv2.VideoCapture(camera_device)
    if not cap.isOpened():
        st.error("Could not open webcam or video source.")
        begin = False
    else:
        ret, frame = cap.read()

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            st.warning("Failed to read frame from webcam. Please verify the webcam is connected properly.")
            break

        frame_placeholder1.image(frame, channels="BGR")  # Display original frame on left panel
        frame = Recog_Plate(frame, car_tracker, plate_tracker)
        frame_placeholder2.image(frame, channels="BGR")  # Display processed frame on right panel
