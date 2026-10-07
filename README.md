# food-delivery-analytics
# Food Delivery App Analytics (Zomato Bangalore)

**Course:** Data Analysis and Visualization Using Python (CUTM1018)  
**Academic Faculty:** Chandra Sekhar Jena  
**Domain:** Food Tech / Retail & Consumer Analytics  


## 1. Project Overview & Problem Statement
Bangalore is one of India's most saturated restaurant markets, featuring thousands of dining establishments ranging from street eateries to luxury fine dining. In this highly competitive environment, restaurant owners, cloud kitchen operators, and investors face major challenges:
* Identifying high-density restaurant hubs with strong consumer activity.
* Understanding how approximate dining cost for two correlates with customer ratings.
* Measuring the real impact of offering online delivery and table reservation services on restaurant popularity and engagement.
* Providing an interactive visualization tool for end-users to discover top-rated dining spots across localities.

This project analyzes the Kaggle Zomato Bangalore Restaurants dataset to uncover actionable operational patterns, price sensitivities, and geographic distributions.



## 2. Key Features & Deliverables
* **Data Cleaning & Standardization:** Handled missing values, formatted `rate` (extracted ratings out of 5), converted `cost` into numeric Indian Rupees, and removed duplicates.
* **Exploratory Data Analysis (EDA):** Five comprehensive visualizations covering distribution skewness, bivariate correlations, and categorical group ratings.
* **Outlier Detection:** Implemented the Interquartile Range (IQR) method to isolate fine-dining price outliers.
* **Interactive Dashboard:** Built a Plotly Dash web application featuring dynamic locality dropdown filtering and responsive multi-chart visualization.
* **AI Tool Integration:** Structured prompt engineering with critical statistical evaluation documented in `AI_Analysis.txt`.



## 3. Tech Stack
* **Programming Language:** Python 3.9+
* **Data Manipulation:** Pandas, NumPy
* **Visualization Libraries:** Matplotlib, Seaborn, Plotly Express
* **Web Dashboard Framework:** Plotly Dash
* **Development Environments:** Google Colab, Jupyter Notebook
* **AI Collaboration:** Google Gemini
* **Version Control:** Git, GitHub




## 4. Dataset Setup or installation steps

Due to GitHub's file size limit, the raw `zomato.csv` is not tracked directly in this repository. Follow these steps to obtain and place the dataset:

1. Download the dataset from Kaggle:
   [Zomato Bangalore Restaurants Dataset](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants)
2. Extract the downloaded archive to locate `zomato.csv`.
3. Create a `data/` directory in the root folder of this project if it does not already exist.
4. Place `zomato.csv` directly inside the `data/` folder:
   ```text
   food-delivery-analytics/
   └── data/
       └── zomato.csv


## 5. Screenshots
1. For dataset
  <img width="1909" height="975" alt="Screenshot 2026-10-08 000253" src="https://github.com/user-attachments/assets/d79e8678-6811-43c7-bbaa-e2a7c62c356b" />
2. For CSV (after extraction)  
  <img width="1920" height="1080" alt="Screenshot (40)" src="https://github.com/user-attachments/assets/06d545a9-7867-401e-b60f-7615ec0d06fe" />


   

