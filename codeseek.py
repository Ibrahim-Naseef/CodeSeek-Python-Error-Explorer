import streamlit as st
import shlex
import requests
import subprocess
import webbrowser
from io import StringIO

def extract_input_fields(file_path):
    input_fields = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'input(' in line or 'raw_input(' in line:
                input_fields.append(line)
    return input_fields

def execute_and_return(cmd, input_data=None):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = proc.communicate(input_data.encode() if input_data else None)
    return out.decode(), err.decode()

def make_request(error):
    resp = requests.get(f"https://api.stackexchange.com/2.2/search?order=desc&tagged=python&sort=activity&intitle={error}&site=stackoverflow")
    return resp.json()

def get_urls(json_dict, pages):
    url_list = []
    count = 0
    st.write(json_dict)
    for i in json_dict['items']:
        if i["is_answered"]:
            url_list.append(i["link"])
        count += 1
        if count == pages:
            break
    return url_list

# Streamlit app
st.title("CodeSeek: Python Error Explorer")
st.write("Upload a Python file, provide input values (if required), execute it, and get help for any errors.")

uploaded_file = st.file_uploader("Choose a Python file", type="py")
pages = st.number_input("Number of Solutions to Display:", min_value=1, max_value=20, value=3)

if uploaded_file is not None:
    file_path = uploaded_file.name
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

    input_fields = extract_input_fields(file_path)
    if input_fields:
        st.subheader("Input Required:")
        for field in input_fields:
            st.text_input(field.strip(), key=field.strip())

    if st.button("Execute Script"):
        inputs = {}
        for field in input_fields:
            user_input = st.session_state.get(field.strip())
            inputs[field.strip()] = user_input

        input_data = '\n'.join(inputs.values())
        out, err = execute_and_return(["python", file_path], input_data)
        print(out,err)
        
        error_message = err.strip().split("\r\n")[-1]
        if out and not(err):
            st.subheader("Output:")
            st.text("NO ERROR IN CODE")
        if err:
            st.subheader("Error:")
            st.text(err)
        
        if error_message:
            filter_out = error_message.split(":")
            json1 = make_request(filter_out[0])
            json2 = make_request(filter_out[1])
            json = make_request(error_message)
            
            st.subheader("Stack Overflow Links:")
            
            urls1 = get_urls(json1, pages)
            urls2 = get_urls(json2, pages)
            urls = get_urls(json, pages)
            
            all_urls = urls1 + urls2 + urls
            unique_urls = list(set(all_urls))[:pages]
            
            for url in unique_urls:
                webbrowser.open(url)

                if st.button(f"Open {url}"):
                    webbrowser.open(url)
