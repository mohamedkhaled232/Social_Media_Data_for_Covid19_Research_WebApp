# Social Media Data for Covid19 Research WebApp

---

This web application is designed to delve into human behavior during the COVID-19 pandemic by analyzing tweets related to COVID-19. we utilize tweets that have already been assigned sentiment labels (negative, positive, or neutral) using Natural Language Processing (NLP). By examining the correlation between daily counts of negative sentiment tweets and the government's stringency index, you can gain insights into how people reacted to changes in government policies during this period.

Web App URL : https://mohamedkhaled232-social-media-data-for-covid19-re-webapp-wq0azt.streamlit.app/

## Data Sources

### Tweets Data
For our tweet data, we utilized the "TBCOV: Two Billion Multilingual COVID-19" project, which provides access to two billion multilingual tweets posted by 87 million users across 218 countries in 67 languages over a 14-month period. Each tweet comes pre-assigned with a sentiment score (-1 for negative, 0 for neutral, and 1 for positive). This extensive dataset encompasses public discourse on various societal, health, and economic issues stemming from the pandemic. It sheds light on diverse perspectives and opinions regarding government policy decisions, ranging from lockdowns to aid allocations for individuals and businesses. Additionally, it covers significant pandemic-related aspects such as food scarcity, equipment shortages, and reports of anxiety and depression symptoms. Our analysis focuses on data from 27 selected countries.

For more information about TBCOV and access to raw data for any specific country, visit [Their website](https://crisisnlp.qcri.org/tbcov).

### Stringency Index
We obtained the stringency index data from the Oxford Coronavirus Government Response Tracker (OxCGRT). This dataset provides daily stringency index values for each country. Stringency Index is a composite measure of nine of the response metrics: school closures; workplace closures; cancellation of public events; restrictions on public gatherings; closures of public transport; stay-at-home requirements; public information campaigns; restrictions on internal movements; and international travel controls. To know more about OxCGRT, visit [Their website](https://ourworldindata.org/covid-stringency-index). You can download the data directly from [here](https://covid.ourworldindata.org/data/owid-covid-data.csv).

## Data Preparation

To prepare the data, we start with the raw tweet data that includes tweet IDs, dates, times, sentiment labels, and more. We then group this data by day to calculate the daily tweet count for each sentiment category. We normalize these counts by dividing them by the total number of tweets to obtain the proportion of each sentiment category for each day. To create a smoother trend, we apply a moving average with a window size of 7. Subsequently, we merge the stringency index data from OxCGRT with our processed data.

### `data_preparation` Script
To use the `data_preparation` script, follow these steps:
1. Download the tweet data for your selected countries from [here](https://crisisnlp.qcri.org/tbcov) and unzip it.
2. Download the stringency index CSV file from [here](https://covid.ourworldindata.org/data/owid-covid-data.csv).
3. The script works on a per-country basis, so provide the following inputs:
   - Path to the folder containing the country's tweet data (the folder should contain TSV files for the country).
   - Path to the stringency index CSV file.
   - Directory where you want to save the output.
   - Country name (ensure it matches the name in the stringency index CSV file).
4. The script filters and retains only the necessary columns. Since our focus is on negative tweets, it preserves the negative smoothed normalized tweet counts, stringency index, and the day. However, you can retain additional columns for other purposes. The output TSV files are stored in the 'data' folder for use in the web app.

# Web Application

Our web application consists of two sections:

## 1. Correlation Plot
In this section, you can select a country and a specific time period. The first plot displays time series trends for the stringency index and normalized negative sentiment tweet counts. The second plot presents a time series trend of the Pearson correlation coefficient, as well as the overall Pearson correlation coefficient for the selected period. The time series plot of the Pearson correlation coefficient is calculated using a rolling moving average with a window size equal to the number of days you select divided by 7. Smaller selected periods yield more accurate calculations.

## 2. Explore Different Countries' Trends
In this section, you can analyze multiple countries simultaneously and compare their stringency index trends, negative tweet counts, or correlations between the stringency index and negative tweet counts trends. Once again, the time series plot of the Pearson correlation coefficient is calculated using a rolling moving average with a window size equal to the number of days you select divided by 7.


# streamlite
This guide will walk you through the process of creating a web app with Streamlit and deploying it to Streamlit Cloud. Streamlit is a Python library that simplifies the development of data-driven web applications.

## Prerequisites

- Python installed on your computer.
- A Streamlit Cloud account. Sign up at [Streamlit Cloud](https://streamlit.io/cloud).

## Step 1: Install Streamlit

Install Streamlit using pip:

```bash
pip install streamlit
```

## Step 2: Create a Streamlit Web App

1. Create a Python script (e.g., `app.py`) where you'll write your Streamlit app code.
2. Import Streamlit and any necessary libraries.
3. Define the app layout and functionality using Streamlit components like `st.title`, `st.markdown`, `st.sidebar`, `st.button`, `st.plotly_chart`, etc.
   For detailed documentation on Streamlit, refer to the Streamlit Documentation https://docs.streamlit.io/ .
## Step 3: Run the Web App Locally

1. Open your terminal and navigate to the directory containing your `app.py` file.
2. Run the app using the following command:

```bash
streamlit run app.py
```

This will launch a local development server, and you can access your app in a web browser at `http://localhost:8501`.

## Step 4: Test Your Web App

Interact with your app locally to ensure it works as expected.

## Step 5: Set Up a Streamlit Cloud Account

Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign up for an account if you don't have one.

## Step 6: Prepare Your Project for Deployment

Make sure your project directory includes any necessary data files, assets, and dependencies listed in a `requirements.txt` file.

## Step 7: Deploy to Streamlit Cloud

1. Go to the Streamlit Cloud dashboard and create a new app.
2. Connect your GitHub repository to Streamlit Cloud if your code is hosted on GitHub.

## Step 8: Configure Deployment Settings

In the Streamlit Cloud dashboard, configure deployment settings, including the branch to deploy from, environment variables, and more.

## Step 9: Deploy Your App

1. Click the "Deploy" button in the Streamlit Cloud dashboard.
2. Streamlit Cloud will build and deploy your app automatically.

## Step 10: Access Your Deployed App

Once the deployment process is complete, you will receive a public URL where your app is hosted.

## Step 11: Share Your Web App

Share the provided URL with others to allow them to access your web app from anywhere.

## Step 12: Monitor and Update

You can monitor app usage and make updates to your app by pushing changes to your GitHub repository. Streamlit Cloud will automatically redeploy when changes are detected.

```
