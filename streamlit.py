import streamlit as st
import numpy as np
import datetime
import db

# Calculate main and side statistics
def calculate_statistics():
    # Main statistics
    current_people = db.get_latest_data()[1]
    daily_avg = db.every_daily_avg()
    
    # Predict number of people in line (simple moving average)
    next_3_hours = db.next_three_hours()
    
    # Side statistics
    total_today = db.total_today()[0]
    historical_total = db.historical_total()[0]
    #these need to have AM or PM
    busiest_time = db.busiest_time()[0].strftime("%I:%M %p")
    least_busy_time = db.least_busy_time()[0].strftime("%I:%M %p")
    
    return current_people, daily_avg, next_3_hours, total_today, historical_total, busiest_time, least_busy_time

(current_people, daily_avg, next_3_hours, 
 total_today, historical_total, 
 busiest_time, least_busy_time) = calculate_statistics()

# Streamlit App UI
st.set_page_config(
    page_title="Line Statistics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("📊 Line Statistics Dashboard")

# Main Section
st.markdown("## 🛠️ Key Statistics")

col1, col2 = st.columns(2)

with col1:
    st.metric("Current Number of People in Line", current_people)
    st.metric("Expected in Next 3 Hours", f"{', '.join(map(str, next_3_hours))}")

with col2:
    st.bar_chart(daily_avg, use_container_width=True)
    st.caption("Average Number of People by Day of the Week")

# Sidebar: Cool Stats
st.sidebar.markdown("## 🆒 Cool Stats")
st.sidebar.metric("Total People in Line Today", total_today)
st.sidebar.metric("Historical Total People in Line", historical_total)
st.sidebar.metric("Busiest Time Today", busiest_time)
st.sidebar.metric("Least Busy Time Today", least_busy_time)

# Footer Section
st.markdown("#### 📈 Historical Trends")
st.line_chart(db.every_daily_avg(), use_container_width=True)
st.caption("Line activity for the past week")
