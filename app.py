import streamlit as st 
import pandas as pd
import os
from io import BytesIO



st.set_page_config(page_title="Data Sweeper", page_icon=":bar_chart:", layout="wide")
st.title("Data Sweeper")
st.write("This is a simple web app that allows you to upload a dataset and view its contents. You can also view the summary statistics of the dataset and download the dataset.")

uploaded_files = st.file_uploader("Choose a file", type=['csv', 'xlsx'], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file.ext = os.path.splitext(file.name)[-1].lower()

        if file.ext == ".csv":
            df = pd.read_csv(file)
        elif file.ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"File type not supported: {file.ext}")
            continue

        # Display info
        st.write(f"File Name: {file.name}")
        st.write(f"File Type: {file.size/1024}")

        #show 5 row of our df
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        #Options for data cleaning

        st.subheader("Datacleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1,col2 = st.columns(2)
            with col1:
                if st.button("Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled")


        #choose specific columns to keep or convert
        st.subheader("Select Columns to Keep Convert")
        columns = st.multiselect(f"choose column for {file.name}",df.columns, default=df.columns)
        df = df[columns]

        #create some visualizations

        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=['number']).iloc[:,:2])

        #covert the file csv to excel
        st.subheader("Conversion Options ")
        conversion_type = st.radio(f"Convert {file.name} to:",["CSV","Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file.ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file.ext, ".xlsx")
                mime_type ="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            #download the file
            st.download_button(label=f"Click here to download {file_name} as {conversion_type}", data=buffer, file_name=file_name, mime=mime_type)

st.success("")


         









