import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish", "Japanese"]  # Added Japanese


# Main app layout
def main():
    # Header
    st.markdown(
        "<h3 style='text-align: center; color: grey;'>Made by YASH LONKAR</h3>",
        unsafe_allow_html=True
    )

    st.subheader("MEDIA MATE")

    # Create three columns for the dropdowns
    col1, col2, col3 = st.columns(3)

    fs = FewShotPosts()
    tags = fs.get_tags()

    with col1:
        # Dropdown for Topic (Tags)
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        # Dropdown for Length
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_options)

    # Generate Button
    if st.button("Generate"):
        post = generate_post(selected_length, selected_language, selected_tag)

        # If Japanese, use Noto Sans JP font for better rendering
        if selected_language == "Japanese":
            st.markdown(
                f"<p style='font-family: \"Noto Sans JP\", sans-serif;'>{post}</p>",
                unsafe_allow_html=True
            )
        else:
            st.write(post)

    # Footer
    st.markdown("<hr>", unsafe_allow_html=True)  # horizontal line
    st.markdown(
        "<p style='text-align: center; color: grey; font-size:12px;'>Made by Yash Lonkar</p>",
        unsafe_allow_html=True
    )


# Run the app
if __name__ == "__main__":
    main()
