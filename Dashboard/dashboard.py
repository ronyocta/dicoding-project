import streamlit as st
import plotly.express as px
import pandas as pd


st.set_page_config(page_title="Bicycle Rental", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: Bicycle Rental (Exploratory Data Analysis)")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True)

url = "https://raw.githubusercontent.com/ronyocta/dicoding-project/master/Dashboard/main_data.csv"
df = pd.read_csv(url)


df["dteday"] = pd.to_datetime(df["dteday"])

# Mendapatkan tanggal terkecil dan terbesar
startDate = pd.to_datetime(df["dteday"]).min()
endDate = pd.to_datetime(df["dteday"]).max()

col1, col2 = st.columns((2))
with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

# Filter data berdasarkan tanggal
df = df[(df["dteday"] >= date1) & (df["dteday"] <= date2)].copy()

st.sidebar.header("Choose your filter : ")

# Membuat sidebar pilihan season
season_label = {1:'Springer', 2:'Summer', 3:'Fall', 4:'Winter'}
df['season_x'] = df['season_x'].map(season_label)
season = st.sidebar.multiselect("Pick weather", df["season_x"].unique())
if not season:
    df2 = df.copy()
else:
    df2 = df[df["season_x"].isin(season)]

# Bar and Pie Chart
with col1:
    st.subheader("Total Bicycle Users")
    fig = px.bar(df2, x="season_x", y="cnt_x", template='seaborn', labels={"season_x": "Season", "cnt_x": "Total"})
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Percentage of Users")
    fig = px.pie(df2, values="cnt_x", names="season_x", template="gridon", labels={"season_x": "Season", "cnt_x": "Total"})
    fig.update_traces(text=df2["season_x"], textposition="inside")
    fig.update_layout(margin=dict(t=50))
    st.plotly_chart(fig, use_container_width=True)

# Time series analysis
linechart_df2 = df2.groupby(df2["dteday"].dt.strftime("%b : %Y"))["cnt_x"].sum().reset_index()
linechart_df2["dteday"] = pd.to_datetime(linechart_df2["dteday"], format="%b : %Y")
linechart_df2 = linechart_df2.sort_values(by="dteday")

fig2 = px.line(linechart_df2, x="dteday", y="cnt_x", labels={"dteday": "Periode", "cnt_x": "Total"}, height=500, template="gridon", width=1000)
fig2.update_xaxes(categoryorder="total ascending")
st.plotly_chart(fig2, use_container_width=True)

# Download original Dataset
st.subheader("Download Original Dataset")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Data", data=csv, file_name="Bicycle Dataset", mime="text/csv")

st.caption('Copyright (C) Rony Octavia Rahardjo, ST. 2023')
