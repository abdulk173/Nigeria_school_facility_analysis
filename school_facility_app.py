import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(page_title="school dashboard" , page_icon="👥" , layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("New_school_data.csv" , encoding="latin-1")
    return df


def create_sidebar_filter(df):
    st.sidebar.header("filter")
    facility_type = st.sidebar.multiselect(
     "selecte facility type",
     options=df["facility_type_display"].unique(),
     default=df["facility_type_display"].unique()
    )    

    local_government = st.sidebar.multiselect(
     "select a particular local government",
     options=df["unique_lga"].unique()


    )
    management = st.sidebar.multiselect(
     "select management type",
     options=df["management"].unique(),
     default=df["management"].unique() 
    )

    return facility_type , management, local_government

def filter_data(df, facility_type, management, local_government):
    
    if not facility_type and not management and not local_government:
        return df.iloc[0:0]

    filtered_df = df.copy()

    if facility_type:
        filtered_df = filtered_df[
            filtered_df["facility_type_display"].isin(facility_type)
        ]

    if management:
        filtered_df = filtered_df[
            filtered_df["management"].isin(management)
        ]

    if local_government:
        filtered_df = filtered_df[
            filtered_df["unique_lga"].isin(local_government)
        ]

    return filtered_df

def display_metrics(filtered_df):

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Number of Schools" , len(filtered_df))

    with col2:
        Total_Students = filtered_df["num_students_total"].sum() if len(filtered_df) > 0 else 0
        st.metric("Total Number of Students" ,f"{Total_Students}")

    with col3:
        avg_student = filtered_df["num_students_total"].mean() if len(filtered_df) > 0 else 0
        st.metric("👥 Average Students per School" , f"{avg_student:.2f}")

    with col4:
        pct_with_elect =  f"{(filtered_df['phcn_electricity']==True).mean() * 100:.2f}%" 
        st.metric("Percentage of Schools with Electricity" , pct_with_elect)

    with col5:
        pct_with_water = f"{(filtered_df['improved_water_supply']==True).mean() * 100:.2f}%"
        st.metric("Percentage of Schools with Improved Water Supply" , pct_with_water)

def display_chart(filtered_df):
    if len(filtered_df) == 0:
        st.warning("no available data for selected filter")
        return

    col1 , = st.columns(1)  

    with col1:
        st.subheader("Distribution of school types") 
        type_counts = filtered_df["facility_type_display"].value_counts()

        fig1 = px.bar(
        x=type_counts.values,
        y=type_counts.index,
        orientation="h",
        title= "Distribution of school typest"
    )

    fig1.update_layout(xaxis_title = "Number of Facilitiesy" , yaxis_title="Type of School")
    st.plotly_chart(fig1 , use_container_width=True)

    col2, col3 =st.columns(2)

    with col2:
        st.subheader("Student population distribution")
        fig2 = px.histogram(filtered_df,x="num_students_total",nbins=6,title="Distribution of Student Population Across Schools")
        fig2.update_layout(xaxis_title="number of student" , yaxis_title="count")
        fig2 .update_traces(marker_line_color="white",marker_line_width=1.5)
        st.plotly_chart(fig2 , use_container_width=True)
    
    with col3:
        st.subheader(" Public vs Private school comparison")
        student_comparison = filtered_df.groupby("management")["num_students_total"].sum().reset_index()
        fig3 = px.bar(student_comparison,x="management",y="num_students_total",title="Public vs Private Schools (Total Students)",)
        fig3.update_layout(xaxis_title="management" , yaxis_title="number of student")
        st.plotly_chart(fig3 , use_container_width=True)

    col4 , col5= st.columns(2)

    with col4:
        st.subheader("Electricity availability")
        fig4 = px.pie(filtered_df,names="phcn_electricity",title="Electricity Availability in Schools")
        st.plotly_chart(fig4 , use_container_width=True)
        
    with col5:
        st.subheader("Water and sanitation access")
        water_total = filtered_df["improved_water_supply"].sum()
        sanitation_total = filtered_df["improved_sanitation"].sum()

        labels = ["Improved Water Supply", "improved_sanitation"]
        values = [water_total, sanitation_total]

        fig5 = px.pie(names=labels,values=values,title="Water vs Sanitation Access")
        st.plotly_chart(fig5 , use_container_width=True)

    col6, = st.columns(1)

    with col6:
        st.subheader("School locations using latitude & longitude")
        fig6 = px.scatter_map(filtered_df,lat="latitude",lon="longitude",hover_name="facility_name",zoom=5,title="School Locations")
        st.plotly_chart(fig6 , use_container_width=True)  

def display_table_data(filtered_df):
    if len(filtered_df) > 0:
        st.dataframe(filtered_df , use_container_width=True , height=300)
        st.success("data successfully displayed")
    else:
        st.info("no data available")

def main():
    df=load_data()

    facility_type , management, local_government = create_sidebar_filter(df)

    filtered_df = filter_data(df, facility_type, management, local_government)

    display_metrics(filtered_df)     

    st.markdown("--")      

    display_chart(filtered_df)

    display_table_data(filtered_df)

if __name__ == "__main__":
    main()    