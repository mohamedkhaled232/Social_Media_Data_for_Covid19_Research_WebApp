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

### `data_preparation.py` Script
To use the `data_preparation.py` script, follow these steps:
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


*Note*: This web app is built using Python and Streamlit.

--- 

