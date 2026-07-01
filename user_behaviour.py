
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv(r"C:\Users\ARAVINDHAN\Downloads\user_behaviour.csv")

st.title("📊 Customer Segmentation & Business Insights Dashboard")

# --- KPI Cards ---
st.header("Key KPIs")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", df["user_id"].nunique())
col2.metric("High-Value Customers", len(df[(df["cluster_profile"]=="High Engagement Users") & (df["churn_risk_score"]<0.3)]))
col3.metric("At-Risk Customers", len(df[(df["cluster_profile"].isin(["Low Activity Users","Occasional Users"])) & (df["churn_risk_score"]>0.5)]))
col4.metric("Moderate Users", len(df[df["cluster_profile"]=="Moderate Users"]))

# --- Segment Distribution Pie Chart ---
st.header("Customer Distribution by Segment")
segment_counts = df["cluster_profile"].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', startangle=140)
ax1.axis("equal")
st.pyplot(fig1)

# --- Churn Risk Bar Chart ---
st.header("Average Churn Risk by Segment")
churn_risk = df.groupby("cluster_profile")["churn_risk_score"].mean().reset_index()
fig2, ax2 = plt.subplots()
sns.barplot(x="cluster_profile", y="churn_risk_score", data=churn_risk, palette="Set2", ax=ax2)
ax2.set_title("Churn Risk per Segment")
st.pyplot(fig2)

# --- Engagement vs Churn Heatmap ---
st.header("Engagement vs Churn Risk Heatmap")
engagement_churn = df.groupby("cluster_profile")[["engagement_score","churn_risk_score"]].mean()
fig3, ax3 = plt.subplots()
sns.heatmap(engagement_churn, annot=True, cmap="YlGnBu", ax=ax3)
ax3.set_title("Engagement vs Churn Risk")
st.pyplot(fig3)

# --- Business Action Mapping ---
st.header("Business Action Mapping")
action_map = {
    "High Engagement Users": "🎯 Loyalty rewards, premium upsell offers",
    "Moderate Users": "🔄 Personalized engagement campaigns",
    "Low Activity Users": "⚠️ Retention offers, reactivation nudges",
    "Occasional Users": "💤 Win-back campaigns, awareness marketing"
}
for cluster, action in action_map.items():
    st.write(f"**{cluster}** → {action}")
