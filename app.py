import streamlit as st

st.markdown("---")
st.header("🏋️ Exercise: File Converter")

st.markdown("""
**Your Task:** Build a simple file format converter!

**Requirements:**
1. Allow upload of text files (.txt)
2. Provide conversion options:
   - To uppercase
   - To lowercase
   - Reverse text
   - Add line numbers
3. Preview the converted result
4. Allow download of the converted file
5. Show a comparison (original vs converted)

**Bonus:**
- Support multiple file formats (txt, md, json)
- Add a "batch convert" option for multiple files
- Create a conversion history in session state
""")

if 'history' not in st.session_state:
    st.session_state.history = []

def convertText(text, transformation):
    if transformation == 'To Uppercase':
        return text.upper()
    elif transformation == 'To Lowercase':
        return text.lower()
    elif transformation == 'Reverse Text':
        return text[::-1]
    elif transformation == 'Add Line Numbers':
        lines = text.split('\n')
        return '\n'.join([f"{i+1}: {line}" for i, line in enumerate(lines)])
    return text

st.title('File Converter')
st.sidebar.header('Settings')
transformation = st.sidebar.selectbox(
    'Choose Transformation',
    ['To Uppercase', 'To Lowercase', 'Reverse Text', 'Add Line Numbers']
)

uploaded_files = st.file_uploader(
    'Choose Files [txt, md, json]',
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        original_content = uploaded_file.read().decode('utf-8')
        converted_content = convertText(original_content, transformation)
        st.session_state.history.append({
            'filename': uploaded_file.name,
            'transformation': transformation
        })
        with st.expander(f"Results for: {uploaded_file.name}", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader('Original')
                st.text_area('Source', original_content, height=200, disabled=True, key=f"orig_{uploaded_file.name}")
            with col2:
                st.subheader('Converted')
                st.text_area('Result', converted_content, height=200, key=f"converted_{uploaded_file.name}")
        st.download_button(
            label='Download Converted File',
            data=converted_content,
            file_name=f"converted_{uploaded_file.name}",
            mime='text/plain'
        )
if st.session_state.history:
    st.divider()
    st.subheader('Conversion History')
    for item in st.session_state.history[-5:]:
        st.write(f"- Converted **{item['filename']}** using **{item['transformation']}**")