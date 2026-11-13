import os
import pandas as pd
import streamlit as st

# --- 1. PAGE CONFIG & MODERN UI THEME ---
st.set_page_config(
    page_title="E-Commerce Analytics Hub", page_icon="⚡", layout="wide"
)

# Custom CSS for a sleek, modern SaaS look
st.markdown("""
    <style>
        /* Main Background & Font */
        .main {
            background-color: #0e1117;
            color: #c9d1d9;
        }
        
        /* Metric Card Styling */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            border: 1px solid #374151;
            padding: 16px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease;
        }
        div[data-testid="metric-container"]:hover {
            transform: translateY(-2px);
            border-color: #6366f1;
        }
        
        /* Headers & Typography */
        h1, h2, h3 {
            color: #f3f4f6 !important;
            font-family: 'Inter', sans-serif;
        }
        
        /* Info & Success Banners */
        .stAlert {
            background-color: #1e293b !important;
            color: #e2e8f0 !important;
            border: 1px solid #334155 !important;
            border-radius: 8px;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0b0f19;
            border-right: 1px solid #1f2937;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            transition: opacity 0.2s ease;
        }
        .stButton>button:hover {
            opacity: 0.9;
        }
    </style>
""", unsafe_allow_html=True)

# --- 2. FILE PATHS & DATA LOADING ---
PRODUCTS_FILE = "products.csv"
TRANSACTIONS_FILE = "transactions.csv"


@st.cache_data
def load_data():
  if not os.path.exists(PRODUCTS_FILE):
    pd.DataFrame(
        columns=[
            "product_id",
            "product_name",
            "category",
            "cost_price",
            "selling_price",
            "stock_level",
        ]
    ).to_csv(PRODUCTS_FILE, index=False)
  if not os.path.exists(TRANSACTIONS_FILE):
    pd.DataFrame(
        columns=[
            "transaction_id",
            "date",
            "product_id",
            "quantity",
            "transaction_type",
        ]
    ).to_csv(TRANSACTIONS_FILE, index=False)

  df_p = pd.read_csv(PRODUCTS_FILE)
  df_t = pd.read_csv(TRANSACTIONS_FILE)
  return df_p, df_t


df_products, df_transactions = load_data()

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.markdown(
    "<h2 style='text-align: center; color: #818cf8;'>⚡ NexusStore</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation", ["📊 Dashboard & Views", "➕ Add New Product", "🛒 Log Sale"]
)

# --- ACTION A: ADD NEW PRODUCT ---
if menu == "➕ Add New Product":
  st.markdown("### ➕ Add New Product to Catalog")
  st.write("Expand your product inventory by adding a new item to `products.csv`.")

  with st.form("add_product_form"):
    col1, col2 = st.columns(2)
    with col1:
      p_name = st.text_input("Product Name", placeholder="e.g., Wireless Earbuds")
      p_cat = st.selectbox(
          "Category", ["Electronics", "Furniture", "Accessories", "Office"]
      )
      p_stock = st.number_input("Initial Stock Level", min_value=0, value=20)
    with col2:
      p_cost = st.number_input("Cost Price ($)", min_value=0.0, value=15.0)
      p_price = st.number_input("Selling Price ($)", min_value=0.0, value=35.0)

    st.markdown("")
    submitted = st.form_submit_button("🚀 Save Product to CSV")
    if submitted:
      if p_name.strip() == "":
        st.error("Product name cannot be empty!")
      else:
        new_id = f"P{len(df_products) + 1:03d}"
        new_row = pd.DataFrame(
            {
                "product_id": [new_id],
                "product_name": [p_name],
                "category": [p_cat],
                "cost_price": [p_cost],
                "selling_price": [p_price],
                "stock_level": [p_stock],
            }
        )
        updated_products = pd.concat([df_products, new_row], ignore_index=True)
        updated_products.to_csv(PRODUCTS_FILE, index=False)
        st.success(
            f"✨ Successfully added **{p_name}** (`{new_id}`) to `products.csv`!"
        )
        st.balloons()

# --- ACTION B: LOG SALE ---
elif menu == "🛒 Log Sale":
  st.markdown("### 🛒 Record a New Sale Transaction")
  st.write(
      "Simulate a customer purchase. This will log a transaction and reduce"
      " stock automatically."
  )

  if df_products.empty:
    st.warning("No products available. Please add a product first.")
  else:
    with st.form("log_sale_form"):
      product_options = {
          f"{row['product_name']} ({row['product_id']})": row["product_id"]
          for _, row in df_products.iterrows()
      }
      selected_label = st.selectbox(
          "Select Product", list(product_options.keys())
      )
      sel_product_id = product_options[selected_label]

      col1, col2 = st.columns(2)
      with col1:
        sale_qty = st.number_input("Quantity Sold", min_value=1, value=1)
      with col2:
        sale_date = st.date_input("Transaction Date")

      st.markdown("")
      sale_submitted = st.form_submit_button("⚡ Complete Sale & Update Stock")
      if sale_submitted:
        current_stock = int(
            df_products.loc[
                df_products["product_id"] == sel_product_id, "stock_level"
            ].values[0]
        )
        if sale_qty > current_stock:
          st.error(
              f"⚠️ Not enough stock! Current stock available: {current_stock}"
          )
        else:
          new_t_id = f"T{101 + len(df_transactions)}"
          new_t_row = pd.DataFrame(
              {
                  "transaction_id": [new_t_id],
                  "date": [str(sale_date)],
                  "product_id": [sel_product_id],
                  "quantity": [sale_qty],
                  "transaction_type": ["SALE"],
              }
          )
          updated_t = pd.concat([df_transactions, new_t_row], ignore_index=True)
          updated_t.to_csv(TRANSACTIONS_FILE, index=False)

          # Update stock level in products.csv
          df_products.loc[
              df_products["product_id"] == sel_product_id, "stock_level"
          ] -= sale_qty
          df_products.to_csv(PRODUCTS_FILE, index=False)

          st.success(
              "🎉 Sale recorded successfully! CSV files updated in real time."
          )
          st.rerun()

# --- VIEW C: DASHBOARD & ANALYTICAL VIEWS ---
elif menu == "📊 Dashboard & Views":
  st.markdown(
      "<h1>⚡ E-Commerce Analytics Hub</h1>", unsafe_allow_html=True
  )
  st.markdown(
      "<p style='color: #94a3b8;'>Live interactive intelligence tracking"
      " products, sales, and profit metrics via CSV storage.</p>",
      unsafe_allow_html=True,
  )

  st.markdown("---")

  # Top KPI Metrics Row
  col1, col2, col3, col4 = st.columns(4)
  total_products = len(df_products)
  total_stock = df_products["stock_level"].sum()
  low_stock_count = len(df_products[df_products["stock_level"] < 10])

  if not df_transactions.empty and not df_products.empty:
    merged_kpi = pd.merge(df_transactions, df_products, on="product_id")
    total_rev = (merged_kpi["quantity"] * merged_kpi["selling_price"]).sum()
  else:
    total_rev = 0.0

  col1.metric("📦 Total Products", total_products)
  col2.metric("📊 Total Stock Units", int(total_stock))
  col3.metric(
      "⚠️ Low Stock Warnings",
      low_stock_count,
      delta="-Action Needed" if low_stock_count > 0 else "All Good",
      delta_color="inverse",
  )
  col4.metric("💰 Total Revenue", f"${total_rev:,.2f}")

  st.markdown("<br>", unsafe_allow_html=True)

  # Analytical Views Section
  st.markdown("### 🔍 Deep-Dive Analytical Views")
  view_option = st.selectbox(
      "Select an analytical lens to inspect your data transformation:",
      [
          "1. All Products (Raw Catalog)",
          "2. Most Sales (Top Units Sold)",
          "3. Highest Revenue Generated",
          "4. Most Profitable Products",
          "5. Low Stock Alerts (< 10 left)",
      ],
  )

  st.markdown("<br>", unsafe_allow_html=True)

  # --- VIEW 1 ---
  if view_option == "1. All Products (Raw Catalog)":
    st.info(
        "📂 **Storage Inspection:** Displaying the complete master file record"
        " from `products.csv`."
    )
    st.dataframe(df_products, use_container_width=True, height=400)

  # --- VIEW 2 ---
  elif view_option == "2. Most Sales (Top Units Sold)":
    st.info(
        "📈 **Data Analysis:** Grouping rows in `transactions.csv` by"
        " `product_id` and summing units sold using pandas `groupby()`."
    )
    if df_transactions.empty:
      st.warning("No transactions recorded yet.")
    else:
      sales_summary = (
          df_transactions.groupby("product_id")["quantity"].sum().reset_index()
      )
      sales_summary.rename(
          columns={"quantity": "total_units_sold"}, inplace=True
      )
      merged = pd.merge(df_products, sales_summary, on="product_id", how="left")
      merged["total_units_sold"] = merged["total_units_sold"].fillna(0)
      sorted_df = merged.sort_values(by="total_units_sold", ascending=False)
      st.dataframe(sorted_df, use_container_width=True, height=400)

  # --- VIEW 3 ---
  elif view_option == "3. Highest Revenue Generated":
    st.info(
        "💵 **Data Transformation:** Merging transactions and catalog files, then"
        " computing mathematical revenue (`Quantity × Selling Price`)."
    )
    if df_transactions.empty:
      st.warning("No transactions recorded yet.")
    else:
      merged = pd.merge(df_transactions, df_products, on="product_id")
      merged["revenue"] = merged["quantity"] * merged["selling_price"]
      rev_summary = (
          merged.groupby(["product_id", "product_name", "category"])["revenue"]
          .sum()
          .reset_index()
      )
      sorted_rev = rev_summary.sort_values(by="revenue", ascending=False)
      st.dataframe(sorted_rev, use_container_width=True, height=400)

  # --- VIEW 4 ---
  elif view_option == "4. Most Profitable Products":
    st.info(
        "💎 **Financial Analytics:** Calculating true net profit (`[Selling Price"
        " - Cost Price] × Quantity`)."
    )
    if df_transactions.empty:
      st.warning("No transactions recorded yet.")
    else:
      merged = pd.merge(df_transactions, df_products, on="product_id")
      merged["total_revenue"] = merged["quantity"] * merged["selling_price"]
      merged["total_cost"] = merged["quantity"] * merged["cost_price"]
      merged["profit"] = merged["total_revenue"] - merged["total_cost"]

      profit_summary = (
          merged.groupby(["product_id", "product_name"])["profit"]
          .sum()
          .reset_index()
      )
      sorted_profit = profit_summary.sort_values(by="profit", ascending=False)
      st.dataframe(sorted_profit, use_container_width=True, height=400)

  # --- VIEW 5 ---
  elif view_option == "5. Low Stock Alerts (< 10 left)":
    st.info(
        "🚨 **Conditional Filtering:** Extracting rows where `stock_level` < 10"
        " to flag immediate restock requirements."
    )
    low_stock = df_products[df_products["stock_level"] < 10]
    if low_stock.empty:
      st.success("🎉 All products have healthy stock levels (10+ units)!")
    else:
      st.dataframe(low_stock, use_container_width=True, height=400)