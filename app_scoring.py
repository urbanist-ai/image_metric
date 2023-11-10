import streamlit as st
import os
import random
import pandas as pd
from PIL import Image

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 0rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)
        

hide_streamlit_style = """
            <style>
            #root > div:nth-child(1) > div > div > div > div > div {
                padding-top: 0rem;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 




@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


# Function to load and display images
def load_image(col2, image_folder, image_name):
    image_path = os.path.join(image_folder, image_name)
    image = Image.open(image_path)
    col2.image(image, use_column_width=True)
    col2.text(f'Remaining Image: {st.session_state.image_index}/{len(st.session_state.all_images)}')


# Function to save scores to a CSV file
def save_scores(scores, output_filename):
    df = pd.DataFrame(scores, columns=["image", "folder", "score"])
    df.to_csv(output_filename, index=False)
    return df

# Function to filter image files
def filter_images(files):
    valid_extensions = ('.jpg', '.jpeg', '.png')
    return [file for file in files if file.endswith(valid_extensions)]



# Main Streamlit app
def main():
    
    col1,col2, col3 = st.columns([1,3,1])
    col2.header("Floorplan Scoring Game")
    col2.text('Score images based on design and composition')


    generated_folder = "images_metric/generated"
    real_folder = "images_metric/actual"
    folder = 'player_scores'

    if "image_index" not in st.session_state:
        st.session_state.image_index = 0
        st.session_state.scores = []
        st.session_state.current_rating = 0
        st.session_state.player = 0
        st.session_state.all_images = 0
        st.session_state_player_name = 'unknown'
    # Load and filter images from the two folders
    
    if st.session_state.player == 0:
        player_name = str(col2.text_input('write your name'))
        start_btn = col2.button('Start playing ...',  use_container_width=True)

        st.session_state_player_name = player_name
        generated_images = filter_images(os.listdir(generated_folder))
        real_images = filter_images(os.listdir(real_folder))
    
        # Combine images list and shuffle  
        
        #generated image = 1, actual = 0
        
        all_images = [(name, 1) for name in generated_images] + \
                     [(name, 0) for name in real_images]
        random.shuffle(all_images)
        if start_btn and player_name: 
            st.session_state.player =1 
            st.session_state.all_images  = all_images
            st.rerun()

    os.makedirs(folder, exist_ok=True) 
    output_filename = os.path.join(folder, f" {st.session_state_player_name}.csv")

    state = True
    if st.session_state.player == state: 
        if st.session_state.image_index < len(st.session_state.all_images):
            
            image_name, image_type = st.session_state.all_images[st.session_state.image_index]
            load_image(col2, generated_folder if image_type == 1 else real_folder, image_name)
    
            # Store user rating in session state
            st.session_state.current_rating = col2.slider("Rate between 0 and 10", 0, 10, value=st.session_state.current_rating, key="rating_slider")
            
            button = col2.button('Next',  use_container_width=True)
            if button:
                # Save the rating when 'Next' is clicked and move to the next image
                st.session_state.scores.append([image_name, image_type, st.session_state.current_rating])
                st.session_state.image_index += 1
                st.rerun()
    
    
    
    
                # # Check if we've reached the end of the list
                # if st.session_state.image_index >= len(st.session_state.all_images):
                #     save_scores(st.session_state.scores, output_filename)
                #     col2.balloons()
                #     col2.success("All images have been rated, and the scores have been saved to a CSV file.")
                #     st.session_state.player = 0
        else:
            # st.write("All images have been rated.")
            df = save_scores(st.session_state.scores, output_filename)
            col2.balloons()
            col2.success("All images have been rated, and the scores have been saved.")
            
            
            # reset_btn = col2.button('Play again...',  use_container_width=True)
            csv = convert_df(df)
            
    
            col2.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f" {st.session_state_player_name}.csv",
                mime='text/csv',
            )

if __name__ == "__main__":
    main()


