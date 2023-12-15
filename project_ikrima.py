from PIL import Image
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="ECommerceAnalys-Ikrima",
    page_icon="📊",
    layout="wide", # atau "centered"
    initial_sidebar_state="expanded" # atau "collapsed"
)

# Konten aplikasi Streamlit di sini

st.title('Proyek Analisis Data:E-Commerce Dataset')
st.header('Nama: Ikrima Rai Saiddah | Email: ikrimarai13@gmail.com | ID Dicoding: Ikrimars')
st.subheader('Visualization & Explanatory Analysis E-Commerce Dataset')
st.markdown('Hasl analisa data e-commerce')

# Gathering Data
order_df = pd.read_csv('orders_dataset.csv')
product_df = pd.read_csv('products_dataset.csv')
geolocation_df = pd.read_csv('geolocation_dataset.csv')
sellers_df= pd.read_csv('sellers_dataset.csv')
product_category_df= pd.read_csv('product_category_name_translation.csv')
order_review_df= pd.read_csv('order_reviews_dataset.csv')
order_item_df= pd.read_csv('order_items_dataset.csv')
order_payments_df= pd.read_csv('order_payments_dataset.csv')
customers_df= pd.read_csv('customers_dataset.csv')

#cleaning data order df
order_df.order_approved_at.fillna(method='ffill',inplace=True)
order_df.order_delivered_carrier_date.fillna(method='ffill', inplace=True)
order_df.order_delivered_customer_date.fillna(method='ffill', inplace=True)
#type data order df
datetime_order = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]

for column in datetime_order:order_df[column] = pd.to_datetime(order_df[column])

#mengganti status karena typo dengan processing order df
order_df['order_status']=order_df['order_status'].replace(['created','approved'],'processing')
order_df['order_status'].value_counts()

#clean product df
product_df['product_category_name'].fillna(product_df['product_category_name'].mode()[0], inplace=True)
product_df['product_name_lenght'].fillna(product_df['product_name_lenght'].mean(), inplace=True)
product_df['product_description_lenght'].fillna(product_df['product_description_lenght'].mean(), inplace=True)
product_df['product_photos_qty'].fillna(product_df['product_photos_qty'].mean(), inplace=True)
product_df.product_weight_g.fillna(value=product_df.product_weight_g.mean(),inplace=True)
product_df.product_length_cm.fillna(value=product_df.product_length_cm.mean(), inplace=True)
product_df.product_height_cm.fillna(value=product_df.product_height_cm.mean(), inplace= True)
product_df.product_width_cm.fillna(value=product_df.product_width_cm.mean(), inplace = True)

#clean geolocatio
geolocation_df.drop_duplicates(inplace=True)

#clean order_payments_df
order_payments_df['payment_type'].replace('not_defined', inplace=True)

agg_pay=order_payments_df[['payment_type','order_id']]
agg_pay=order_payments_df.groupby('payment_type')['order_id'].agg('count').reset_index()
agg_pay.columns = ['payment type','count order']

#clean order_review
datetime_review = ["review_creation_date","review_answer_timestamp"]

for column in datetime_review:
  order_review_df[column] = pd.to_datetime(order_review_df[column])

datetime_item = ["shipping_limit_date"]

for column in datetime_item:
  order_item_df[column] = pd.to_datetime(order_item_df[column])

# Analyze delivery time
order_df['order_purchase_timestamp'] = pd.to_datetime(order_df['order_purchase_timestamp'])  # Convert to datetime
order_df['order_estimated_delivery_date'] = pd.to_datetime(order_df['order_estimated_delivery_date'])  # Convert to datetime

order_df['waktu_pengiriman'] = (
    order_df['order_estimated_delivery_date'] - order_df['order_purchase_timestamp']
).dt.days.astype('int')

# Menghitung rata-rata waktu pengiriman
rata_rata_pengiriman = order_df['waktu_pengiriman'].mean()

Q1 = order_df['waktu_pengiriman'].quantile(0.25)
Q3 = order_df['waktu_pengiriman'].quantile(0.75)

IQR = Q3 - Q1
min_value = Q1 - 1.5 * IQR
max_value = Q3 + 1.5 * IQR

# Filtering outliers
filter_min = order_df['waktu_pengiriman'] < min_value
filter_max = order_df['waktu_pengiriman'] > max_value

outlier = order_df[filter_min | filter_max]
clr_outlier = order_df[~(filter_min | filter_max)]

#jika ngin hari saja dengan formt int
clr_outlier['waktu_pengiriman'] = (order_df['order_estimated_delivery_date'] - order_df['order_purchase_timestamp']).dt.days.astype('int')

# Menghitung rata-rata waktu pengiriman
rata_pengiriman = clr_outlier['waktu_pengiriman'].mean()

# Aggregate data for plotting
agg_clr_outlier = clr_outlier[['order_purchase_timestamp', 'order_id']]
agg_clr_outlier['order_purchase_timestamp'] = agg_clr_outlier['order_purchase_timestamp'].dt.strftime('%B')
agg_clr_outlier = agg_clr_outlier.groupby('order_purchase_timestamp')['order_id'].agg('count').reset_index()
agg_clr_outlier.columns = ['time order', 'count order']

agg_y_clr_outlier=clr_outlier[['order_purchase_timestamp','order_id']]
agg_y_clr_outlier['order_purchase_timestamp'] = agg_y_clr_outlier['order_purchase_timestamp'].dt.strftime('%Y-%m')
agg_y_clr_outlier=agg_y_clr_outlier.groupby('order_purchase_timestamp')['order_id'].agg('count').reset_index()
agg_y_clr_outlier.columns=['time order','count order']


# Your existing code for plotting the graph
plt.figure(figsize=(10, 5))
plt.plot(
    agg_clr_outlier['time order'],
    agg_clr_outlier['count order'],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
plt.title("Total Revenue per Month", loc="center", fontsize=20)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

# Streamlit app
st.title("E-commerce Dashboard")

# Display the orders DataFrame
st.subheader("Orders Dataset")
st.write(order_df.head())

# Display the delivery time analysis
st.subheader("Delivery Time Analysis")
st.write(f"Average delivery time: {rata_pengiriman:.2f} days")
st.write(f"Minimum delivery time: {min_value} days")
st.write(f"Maximum delivery time: {max_value} days")

st.header("Jumlah Skor Ulasan ")
# Display the orders DataFrame
st.subheader("Order Review Dataset")
st.write(order_review_df.head())
st.subheader("Review Score")
review= order_review_df.groupby(by='review_score').agg({
 "review_score":["count"]
})
st.write(review)
st.markdown('Pada review score terdapat 57328 dengan score 5 dan paling sedikit dengan score 2 sebanyak 3151 review')

st.header("Total Revenue per Month and Year")
# Create tabs
tabs = st.tabs(["Total Revenue per Month", "Total Revenue per Month and Year"])

# Tab 1: Total Revenue per Month
with tabs[0]:
    plt.figure(figsize=(20, 5))
    plt.plot(
        agg_clr_outlier['time order'],
        agg_clr_outlier['count order'],
        marker='o',
        linewidth=2,
        color="#72BCD4"
    )
    plt.title("Total Revenue per Month", loc="center", fontsize=20)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    st.pyplot(plt)
    st.markdown("Selama tiga tahun terakhir memiliki total revenue tertinggi terdapat pada bulan agustus dengan total order sebanyak 10588 kali dan terendah terdapat pada bulan september sebanyak 4271 kali.")

# Tab 2: Total Revenue per Month and Year
with tabs[1]:
    plt.figure(figsize=(20, 5))
    plt.plot(
        agg_y_clr_outlier['time order'],
        agg_y_clr_outlier['count order'],
        marker='o',
        linewidth=2,
        color="#72BCD4"
    )
    plt.title("Total Revenue per Month and Year", loc="center", fontsize=20)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    st.pyplot(plt)
    st.markdown("tahun 2017 bulan november memiliki jumlah order tertinggi sebanyak 7499 kali")

item_category_df = pd.merge(
    left=order_item_df,
    right=product_df,
    how="left",
    left_on="product_id",
    right_on="product_id"
)

st.write(item_category_df.head())

st.header("Analisa Kategori Produk")
#kolom data kaegori
col1, col2, col3 = st.columns(3)

# Mengelompokkan data berdasarkan kategori produk dan menghitung jumlah pembelian
top_categories = item_category_df['product_category_name'].value_counts().nlargest(10)

with col1:
    # Membuat grafik batang horizontal di Streamlit
    st.subheader("Kategori Produk Paling Banyak Dibeli")
    fig, ax = plt.subplots()
    ax.barh(top_categories.index, top_categories.values, color='blue')
    ax.set_xlabel('Jumlah Pembelian')
    ax.set_ylabel('Kategori Produk')
    ax.set_title('Top 10 Kategori Produk yang Paling Banyak Dibeli')

    # Menambahkan nilai di atas batang grafik
    for index, value in enumerate(top_categories.values):
        ax.text(value, index, str(value), ha='left', va='center')

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)
    st.markdown("cama_mesa_banho memiliki total order sebanyak 12718, dan memiliki harga tertinggi sebesar 3980.0 USD.")

# Mengelompokkan data berdasarkan produk dan mencari harga tertinggi
products_expensive = item_category_df.groupby('product_category_name')['price'].max().nlargest(10)
with col2:
    st.subheader("Kategori Produk dengan Harga Tertinggi")
    # Membuat grafik bar horizontal di Streamlit
    fig, ax = plt.subplots()
    ax.barh(products_expensive.index, products_expensive.values, color='red')
    ax.set_xlabel('Harga Tertinggi')
    ax.set_ylabel('Kategori Produk')
    ax.set_title('Top 10 Produk Paling Mahal')

    # Menambahkan nilai di atas batang grafik
    for index, value in enumerate(products_expensive.values):
        ax.text(value, index, str(value), ha='left', va='center')

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)
    st.markdown('10 produk paling mahal yaitu utilidades domesticas sebesar 6735.0 USD')

# Mengelompokkan data berdasarkan kategori produk dan mencari ongkos kirim tertinggi
ongkir_graph = item_category_df.groupby('product_category_name')['freight_value'].max().nlargest(10)

with col3:
    st.subheader("Kategori Produk dengan Ongkir Tertinggi")
    fig, ax = plt.subplots()
    ax.bar(ongkir_graph.index, ongkir_graph.values, color='orange')
    ax.set_xlabel('Kategori Produk')
    ax.set_ylabel('Ongkos Kirim Tertinggi')
    ax.set_title('Top 10 Kategori Produk dengan Ongkos Kirim Tertinggi')
    ax.set_xticklabels(ongkir_graph.index, rotation=45, ha='right')  # Rotasi label agar lebih mudah dibaca

    # Menambahkan nilai di atas batang grafik
    for index, value in zip(ongkir_graph.index, ongkir_graph.values):
        ax.text(index, value, f'{value:.2f}', ha='center', va='bottom')

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)
    st.markdown("produk dengan ongkos kirim tertinggi yaitu utilidades bebes sebesar 409.68 USD")

# Membuat gambar dengan ukuran lebih kecil
st.header("Distribusi tipe pembayaran untuk order")
fig, ax = plt.subplots(figsize=(8, 4))
ax.set_title('Distribution of Payment Types for Number of Orders')

# Menetapkan warna untuk setiap tipe pembayaran
colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightpink']

# Menampilkan diagram lingkaran di Streamlit
with st.container():
    explode = (0, 0.1, 0, 0)
    ax.pie(
        x=agg_pay['count order'],
        labels=agg_pay['payment type'],
        autopct='%1.1f%%',
        colors=colors,
        explode=explode,
        shadow=True,
        startangle=75,
        textprops = dict(size=7)  # Atur ukuran teks di sini
    )

    # Menampilkan diagram lingkaran di Streamlit
    st.pyplot(fig, clear_figure=True)

st.markdown('Metode pembayaran dengan menggunakan credi card banyak diminati customers untuk melakukan order dan paling sedikit menggunakan debit card.')

st.header("Lokasi Geografis Persebaran Pelanggan")
# Display the orders DataFrame
st.subheader("Geolocation Dataset")
st.write(geolocation_df.head())
# Tentukan warna berdasarkan nilai longitude dan latitude
colors = geolocation_df['geolocation_lng']

plt.scatter(geolocation_df['geolocation_lng'], geolocation_df['geolocation_lat'],c=colors, cmap='viridis', alpha=0.5)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Lokasi Geografis Pelanggan')
st.pyplot(plt)
st.markdown('Berdasarkan data diatas, Setiap titik akan memiliki koordinat longitude di sumbu x dan latitude di sumbu y. gambaran visual tentang sebaran lokasi pelanggan di berbagai daerah. hasilnya berkumpul pada satu titik lokasi geografis dengan rata-rata latitude -20.998353 dan longitude -46.461098. Semakin gelap warnanya, semakin rendah nilai longitude. Hal ini memungkinkan kita untuk melihat bagaimana pelanggan terdistribusi secara horizontal (sepanjang garis bujur)')
st.header("Dataset Informasi Kondisi Demografi")
order_customers_df = pd.merge(
    left=order_df,
    right=customers_df,
    how="left",
    left_on="customer_id",
    right_on="customer_id"
)
st.write(order_customers_df.head())
st.subheader("informasi Demografi Pelanggan")
colom1, colom2 = st.columns(2)
with colom1:
    st.write(order_customers_df.groupby(by="customer_city").order_id.nunique().sort_values(ascending=False).head(10))
with colom2:
    st.write(order_customers_df.groupby(by="customer_state").order_id.nunique().sort_values(ascending=False))

st.markdown("informasi mengenai pelanggan sebanyak 99441 orang yang menunjukkan terdapat 4119 kota yang berasal dari 27 negara. data tersebut, menunjukkan customers paling banyak berasal dari kota sao paulo dengan jumlah 15540 orang dengan kode negara SP sebanyak 41746 orang dari total pelanggan 99441 orang.")
