📦 NexusStore: E-Commerce Inventory \& Analytics Hub



A lightweight, interactive web application built with Python, Streamlit, and Pandas that demonstrates how raw data flows from storage (CSV files) into actionable business analytics.



🚀 Features



Visual Product Gallery: Browse inventory items in a responsive grid complete with real-time product photos, pricing, and stock status.



Interactive Sales Logger: Simulate real-world customer purchases that automatically update live inventory and trigger restock alerts.



Dynamic Analytics Dashboard: Instantly switch between 5 analytical views:



All Products (Raw Catalog)



Most Sales (Top Units Sold via Grouping)



Highest Revenue Generated (Mathematical Calculations)



Most Profitable Products (Financial Margin Analysis)



Low Stock Warnings (< 10 units conditional filtering)



Live CSV Storage: No complex database required—all changes persist directly in transparent flat CSV files.



📁 Project Structure



Inside your project folder, you should have three files:



app.py — The core Python script running the Streamlit web interface and data analysis pipeline.



products.csv — Master catalog storing product IDs, names, categories, pricing, stock levels, and image URLs.



transactions.csv — Operational ledger recording every sale transaction over time.



🛠️ How to Run the Project



1\. Prerequisites



Make sure you have Python installed on your computer. Then, open your terminal or command prompt and install the required libraries:



pip install streamlit pandas





2\. Setup Files



Ensure app.py, products.csv, and transactions.csv are all saved together inside the exact same folder.



3\. Launch the App



Open your terminal, navigate to your project folder, and run:



streamlit run app.py





Streamlit will automatically launch and open the interactive dashboard right in your web browser (http://localhost:8501).

