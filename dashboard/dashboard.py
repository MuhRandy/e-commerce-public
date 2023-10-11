import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return daily_orders_df

def create_bycity_df(df):
    bycity_df = df.groupby(by="customer_city").customer_id.nunique().reset_index()
    bycity_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bycity_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bystate_df

def create_byproduct_df(df):
    byproduct_df = df.groupby(by="product_id").order_id.nunique().reset_index()
    byproduct_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return byproduct_df

def create_bycategory_df(df):
    bycategory_df = df.groupby(by="product_category_name").order_id.nunique().reset_index()
    bycategory_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return bycategory_df

def create_bypayment_df(df):
    bypayment_df = df.groupby(by="payment_type").order_id.nunique().reset_index()
    bypayment_df.rename(columns={
        "order_id": "order_count"
    }, inplace=True)
    
    return bypayment_df

all_df = pd.read_csv('all_data.csv')

all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
all_df["order_purchase_timestamp"] = pd.to_datetime(all_df["order_purchase_timestamp"])

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
 
with st.sidebar:    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                (all_df["order_purchase_timestamp"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
bycity_df = create_bycity_df(main_df)
bystate_df = create_bystate_df(main_df)
byproduct_df = create_byproduct_df(main_df)
bycategory_df = create_bycategory_df(main_df)
bypayment_df = create_bypayment_df(main_df)

st.header('E-Commerce Public Dashboard :sparkles:')

st.subheader('Daily Orders')
 
total_orders = daily_orders_df.order_count.sum()
st.metric("Total orders", value=total_orders)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Most Customer by City and State")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(y="customer_count", x="customer_city", data=bycity_df.sort_values(by='customer_count', ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("City", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(y="customer_count", x="customer_state", data=bystate_df.sort_values(by='customer_count', ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].yaxis.tick_right()
ax[1].set_title("State", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)
 
st.pyplot(fig)

st.subheader("Most Selling by Product and Product Category")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="order_count", y="product_id", data=byproduct_df.sort_values(by='order_count', ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Product", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="order_count", y="product_category_name", data=bycategory_df.sort_values(by='order_count', ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.tick_right()
ax[1].set_title("Product Category", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)
 
st.pyplot(fig)

st.subheader("Number of Payment Type by Order")

fig = plt.figure(figsize=(10, 5))

sns.barplot(
    y="order_count",
    x="payment_type",
    data=bypayment_df.sort_values(by="order_count", ascending=False),
    palette=colors
)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)

st.pyplot(fig)