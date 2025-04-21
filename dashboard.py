import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Employee Performance Dashboard", layout="wide")

# Load the data
@st.cache_data
def load_data():
    try:
        # Using the sample data from your document
        data = {
            'Employee_ID': [101, 102, 103, 104, 105],
            'Gender': ['Male', 'Female', 'Male', 'Female', 'Male'],
            'Age': [29, 34, 27, 40, 31],
            'Job_Title': ['Software Engineer', 'Data Scientist', 'System Analyst', 
                         'HR Manager', 'Project Manager'],
            'Hire_Date': ['2019-06-15', '2017-09-23', '2021-02-11', 
                         '2015-12-05', '2018-07-19'],
            'Years_At_Company': [4, 6, 2, 9, 5],
            'Education_Level': ["Master's", 'PhD', "Bachelor's", "Master's", "Master's"],
            'Performance_Score': [3, 4, 2, 5, 4],
            'Monthly_Salary': [75000, 95000, 60000, 105000, 88000],
            'Work_Hours_Per_Week': [40, 45, 38, 42, 44],
            'Employee_Satisfaction_Score': [4.2, 4.5, 3.8, 4.9, 4.3],
            'Resigned': [0, 0, 0, 0, 0]
        }
        df = pd.DataFrame(data)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load data
df = load_data()

# Check if data loaded successfully
if df is None:
    st.error("Failed to load data. Please check the data source.")
    st.stop()

# Sidebar
st.sidebar.title("Filters")
selected_jobs = st.sidebar.multiselect(
    "Job Titles",
    options=df['Job_Title'].unique(),
    default=df['Job_Title'].unique()
)

selected_education = st.sidebar.multiselect(
    "Education Level",
    options=df['Education_Level'].unique(),
    default=df['Education_Level'].unique()
)

# Filter data based on selections
filtered_df = df[
    (df['Job_Title'].isin(selected_jobs)) &
    (df['Education_Level'].isin(selected_education))
]

# Main dashboard
st.title("Employee Performance Dashboard")
st.markdown("---")

# Layout columns
col1, col2 = st.columns(2)

# KPIs
with col1:
    st.subheader("Key Performance Indicators")
    st.metric("Total Employees", len(filtered_df))
    st.metric("Average Performance Score", 
             round(filtered_df['Performance_Score'].mean(), 2))
    st.metric("Average Salary", 
             f"${filtered_df['Monthly_Salary'].mean():,.0f}")
    st.metric("Average Satisfaction", 
             round(filtered_df['Employee_Satisfaction_Score'].mean(), 2))

# Charts
with col2:
    st.subheader("Performance Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x='Performance_Score', data=filtered_df, ax=ax)
    ax.set_title('Distribution of Performance Scores')
    st.pyplot(fig)

# Detailed statistics
st.subheader("Employee Statistics")
st.dataframe(filtered_df.describe())

# Additional Visualizations
st.subheader("Detailed Analysis")

tab1, tab2, tab3 = st.tabs(["Salary vs Performance", "Experience vs Salary", "Satisfaction by Job"])

with tab1:
    fig = px.scatter(filtered_df, 
                    x='Performance_Score', 
                    y='Monthly_Salary',
                    color='Job_Title',
                    size='Years_At_Company',
                    title='Salary vs Performance Score')
    st.plotly_chart(fig)

with tab2:
    fig = px.scatter(filtered_df,
                    x='Years_At_Company',
                    y='Monthly_Salary',
                    color='Education_Level',
                    title='Years at Company vs Salary')
    st.plotly_chart(fig)

with tab3:
    fig, ax = plt.subplots()
    sns.boxplot(x='Job_Title', y='Employee_Satisfaction_Score', data=filtered_df, ax=ax)
    plt.xticks(rotation=45)
    ax.set_title('Satisfaction Score by Job Title')
    st.pyplot(fig)

# Raw data view
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.dataframe(filtered_df)

# Footer
st.markdown("---")
st.markdown("Dashboard created with Streamlit | Data as of March 25, 2025")