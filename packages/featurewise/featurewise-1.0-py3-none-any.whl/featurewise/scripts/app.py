import streamlit as st
import pandas as pd
from featurewise.imputation import MissingValueImputation
from featurewise.encoding import FeatureEncoding
from featurewise.scaling import DataNormalize
from featurewise.date_time_features import DateTimeExtractor
from featurewise.create_features import PolynomialFeaturesTransformer
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pkg_resources


st.set_page_config(
    page_title="FeatureWise",
    page_icon="🌟",
)

st.markdown(
    """
    <style>
    /* Apply primary color to the sidebar */
    [data-testid="stSidebar"] > div:first-child {
        background-color: #0096FF;
    }

    /* Customize the file uploader background */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #0096FF;  /* Change this to your desired color */
        border-radius: 10px;  /* Optional: add rounded corners */
        padding: 10px;  /* Optional: add padding */
    }

    /* Customize the 'Drag and drop' text color */
    [data-testid="stFileUploaderDropzoneInstructions"] .st-emotion-cache-9ycgxx {
        color: white;  /* Change this to your desired text color */
    }

    /* Customize the 'Browse files' button */
    [data-testid="baseButton-secondary"] {
        background-color: #004080;  /* Change this to your desired button color */
        color: white;  /* Change this to your desired button text color */
    }

    /* Change the color of the header */
    .ag-header-container {
        background-color: #004080;  /* Change this to your desired header color */
    }
    .ag-header-cell-text {
        color: white;  /* Change this to your desired header text color */
    }

    /* Change the color of the Imputation button */
    span[data-baseweb="tag"] {
        background-color: #004080;  /* Change this to your desired background color */
        color: white;  /* Change this to your desired text color */
        padding: 10px 20px;  /* Adjust padding to fit the button size */
        border-radius: 5px;  /* Optional: add rounded corners */
        display: inline-flex;  /* Ensure the span behaves like a button */
        align-items: center;  /* Center content vertically */
        justify-content: center;  /* Center content horizontally */
        cursor: pointer;  /* Show a pointer cursor on hover */
    }
    span[data-baseweb="tag"] svg {
        fill: white;  /* Change this to your desired icon color */
    }
    </style>
    """,
    unsafe_allow_html=True
)


def display_dataframe(df):
    # Configure the AgGrid display options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)  # Pagination
    gb.configure_side_bar()  # Enable column selection
    grid_options = gb.build()
    
    # Display the dataframe with AgGrid
    AgGrid(
        df,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme="streamlit"  # You can choose between different themes: "light", "dark", "blue", "material", "streamlit"
    )

def main():
    
     #Add logo at the top of the app
    logo_path = pkg_resources.resource_filename('featurewise', 'scripts/featurewise_logo.png')
    st.image(logo_path, caption=None, use_column_width=200)
     
    # st.markdown("<h1 style='color: blue;'>FEATUREWISE</h1>", unsafe_allow_html=True)
    
    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Load the DataFrame into session state if not already present
            if 'original_df' not in st.session_state:
                st.session_state.original_df = pd.read_csv(uploaded_file)
                st.session_state.df = st.session_state.original_df.copy()

            st.markdown(
                          "<h3 style='font-size:18px;'>Uploaded Dataframe</h3>",
                           unsafe_allow_html=True
                         )
            display_dataframe(st.session_state.df)

        except pd.errors.EmptyDataError:
            st.error("The uploaded file is empty. Please upload a valid CSV file.")
            return
        except pd.errors.ParserError:
            st.error("There was an issue parsing the CSV file. Please ensure it is formatted correctly.")
            return
        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")
            return

        # Sidebar title
        st.sidebar.title("Transformation Toolbox")
        transformations = st.sidebar.multiselect(
            "Select tools to apply:",
            [
                "Delete Columns", 
                "Imputation", 
                "Encoding", 
                "Scaling", 
                "Datetime Features", 
                "Feature Creation"
            ]
        )

        # Delete Columns
        if "Delete Columns" in transformations:
            st.sidebar.header("Delete Columns")
            columns_to_delete = st.sidebar.multiselect("Select columns to delete", st.session_state.df.columns)
            if st.sidebar.button("Apply Column Deletion"):
                st.session_state.df = st.session_state.df.drop(columns=columns_to_delete)
                st.markdown(
                          "<h3 style='font-size:18px;'>DataFrame After Column Deletion</h3>",
                           unsafe_allow_html=True
                         )
                display_dataframe(st.session_state.df)

        # Imputation
        if "Imputation" in transformations:
            st.sidebar.header("Imputation Settings")
            strategies = {}
            try:
                for column in st.session_state.df.columns:
                    if st.session_state.df[column].isnull().any():
                        strategy = st.sidebar.selectbox(
                            f"Select strategy for {column}",
                            ["mean", "median", "mode", "custom"],
                            key=column
                        )
                        if strategy == "custom":
                            custom_value = st.sidebar.number_input(f"Enter custom value for {column}", key=f"{column}_custom")
                            strategies[column] = custom_value
                        else:
                            strategies[column] = strategy
                if st.sidebar.button("Apply Imputation"):
                    imputer = MissingValueImputation(strategies=strategies)
                    st.session_state.df = imputer.fit_transform(st.session_state.df)
                    st.markdown(
                          "<h3 style='font-size:18px;'>DataFrame After Imputation</h3>",
                           unsafe_allow_html=True
                         )
                    display_dataframe(st.session_state.df)
            except KeyError as e:
                st.error(f"Column not found: {e}")
            except Exception as e:
                st.error(f"An error occurred during imputation: {e}")

        # Encoding
        if "Encoding" in transformations:
            st.sidebar.header("Encoding Settings")
            try:
                encoding_type = st.sidebar.selectbox("Select encoding type", ["Label Encoding", "One-Hot Encoding"])
                columns = st.sidebar.multiselect("Select columns to encode", st.session_state.df.columns)
                if st.sidebar.button("Apply Encoding"):
                    encoder = FeatureEncoding(st.session_state.df)
                    if encoding_type == "Label Encoding":
                        st.session_state.df = encoder.label_encode(columns)
                    elif encoding_type == "One-Hot Encoding":
                        st.session_state.df = encoder.one_hot_encode(columns)   
                    st.markdown(
                          "<h3 style='font-size:18px;'>DataFrame After Encoding</h3>",
                           unsafe_allow_html=True
                         )
                    display_dataframe(st.session_state.df)
            except KeyError as e:
                st.error(f"Column not found: {e}")
            except TypeError as e:
                st.error(f"Type error during encoding: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred during encoding: {e}")

        # Scaling
        if "Scaling" in transformations:
            st.sidebar.header("Scaling Settings")
            try:
                normalizer = DataNormalize()
                method = st.sidebar.selectbox("Select scaling method", list(normalizer.scalers.keys()), index=0)
                scale_option = st.sidebar.radio("Scale the entire DataFrame or specific columns?", ("Entire DataFrame", "Specific Columns"))
                if scale_option == "Specific Columns":
                    columns = st.sidebar.multiselect("Select columns to scale", st.session_state.df.columns)
                    if st.sidebar.button("Apply Scaling"):
                        if not all(st.session_state.df[col].dtype in ['int64', 'float64'] for col in columns):
                            raise TypeError("Selected columns must be numeric for scaling.")
                        st.session_state.df = normalizer.scale_columns(st.session_state.df, columns, method)
                        st.markdown(
                          "<h3 style='font-size:18px;'>DataFrame After Scaling</h3>",
                           unsafe_allow_html=True
                         )
                        display_dataframe(st.session_state.df)
                else:
                    if st.sidebar.button("Apply Scaling"):
                        st.session_state.df = normalizer.scale(st.session_state.df, method)
                        st.write("### DataFrame After Scaling")
                        display_dataframe(st.session_state.df)
            except KeyError as e:
                st.error(f"Column not found: {e}")
            except TypeError as e:
                st.error(f"Type error during scaling: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred during scaling: {e}")

        # Datetime Features
        if "Datetime Features" in transformations:
            st.sidebar.header("Datetime Features Settings")
            try:
                datetime_col = st.sidebar.selectbox("Select the datetime column", st.session_state.df.columns)
                extract_options = st.sidebar.multiselect("Select extraction(s)", ["Year", "Month", "Day", "Day of Week", "All"])
                if st.sidebar.button("Apply Datetime Transformations"):
                    datetime_extractor = DateTimeExtractor(st.session_state.df, datetime_col)
                    if "All" in extract_options:
                        st.session_state.df = datetime_extractor.extract_all()
                    else:
                        if "Year" in extract_options:
                            st.session_state.df = datetime_extractor.extract_year()
                        if "Month" in extract_options:
                            st.session_state.df = datetime_extractor.extract_month()
                        if "Day" in extract_options:
                            st.session_state.df = datetime_extractor.extract_day()
                        if "Day of Week" in extract_options:
                            st.session_state.df = datetime_extractor.extract_day_of_week()
                    st.markdown(
                          "<h3 style='font-size:18px;'>DataFrame After DateTime Features Extraction</h3>",
                           unsafe_allow_html=True
                         )
                    display_dataframe(st.session_state.df)
            except KeyError as e:
                st.error(f"Column not found: {e}")
            except Exception as e:
                st.error(f"An error occurred during datetime transformation: {e}")

        # Feature Creation
        if "Feature Creation" in transformations:
            st.sidebar.header("Feature Creation Settings")
            try:
                poly_degree = st.sidebar.number_input("Degree of polynomial features", min_value=1, value=2)
                poly_columns = st.sidebar.multiselect("Select columns for polynomial features", st.session_state.df.columns)
                if st.sidebar.button("Apply Polynomial Features"):
                    if poly_columns:
                        poly_transformer = PolynomialFeaturesTransformer(degree=poly_degree)
                        df_poly = poly_transformer.fit_transform(st.session_state.df[poly_columns], degree=poly_degree)
                        st.session_state.df = pd.concat([st.session_state.df.drop(columns=poly_columns), df_poly], axis=1)
                        st.markdown(
                          "<h3 style='font-size:18px;'>DataFrame After Polynomial Features</h3>",
                           unsafe_allow_html=True
                         )
                        display_dataframe(st.session_state.df)
                    else:
                        st.error("Please select at least one column for polynomial features.")
            except ValueError as e:
                st.error(f"Error during polynomial feature creation: {e}")
            except Exception as e:
                st.error(f"An unexpected error occurred during feature creation: {e}")

        # Download transformed DataFrame
        try:
            st.sidebar.markdown("### Download Transformed Data")
            csv = st.session_state.df.to_csv(index=False)
            st.sidebar.download_button("Download Transformed CSV", csv, "transformed_data.csv", "text/csv")
        except Exception as e:
            st.error(f"Error generating download: {e}")

if __name__ == "__main__":
    main()
