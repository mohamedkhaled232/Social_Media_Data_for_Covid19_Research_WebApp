
import pandas as pd
from datetime import datetime
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os
import io
from streamlit_option_menu import option_menu



dir_path = os.path.dirname(os.path.realpath(__file__))
country_names = ["Afghanistan", "Belgium", "Bolivia", "Chile", "Croatia", "Czechia", "Denmark", "Egypt", "France", "Germany", "Ireland", "Israel", "Italy", "Luxembourg", "Malaysia", "Norway", "Slovakia", "Slovenia", "South Africa", "Spain", "Sudan", "Switzerland", "Togo", "Uganda", "United Kingdom", "Yemen", "Zimbabwe"]


with st.sidebar:
    selected = option_menu("Main Menu", ["Home", 'Correlation Plot', "Different Countries' Trends"], 
        icons=['house','graph-up', 'globe'], menu_icon="menu-button-wide", default_index=0)
    

if selected== "Home" :
    


    st.title("Social Media Data for Covid19 Research WebApp")

    st.write("This web application is designed to delve into human behavior during the COVID-19 pandemic by analyzing tweets related to COVID-19. we utilize tweets that have already been assigned sentiment labels (negative, positive, or neutral) using Natural Language Processing (NLP). By examining the correlation between daily counts of negative sentiment tweets and the government's stringency index, you can gain insights into how people reacted to changes in government policies during this period. You can also compare trends across different countries to understand how people in different parts of the world reacted to the pandemic and government policies. "
             )
    st.write("[Github Repository](https://github.com/mohamedkhaled232/Application-of-Social-Media-Data-in-COVID-19-Research)")
    # Data Source Expander
    with st.expander("Data Sources"):
        st.write("### Tweets Data")
        st.write("For our tweets data, we utilized the \"TBCOV: Two Billion Multilingual COVID-19\" project, "
                "which provides access to two billion multilingual tweets posted by 87 million users across 218 countries "
                "in 67 languages over a 14-month period. Each tweet comes pre-assigned with a sentiment score (-1 for negative, "
                "0 for neutral, and 1 for positive). This extensive dataset encompasses public discourse on various societal, "
                "health, and economic issues stemming from the pandemic. It sheds light on diverse perspectives and opinions "
                "regarding government policy decisions, ranging from lockdowns to aid allocations for individuals and businesses. "
                "Additionally, it covers significant pandemic-related aspects such as food scarcity, equipment shortages, "
                "and reports of anxiety and depression symptoms. Our analysis focuses on data from 27 selected countries.")
        
        st.write("For more information about TBCOV and access to raw data for any specific country, visit [their website](https://crisisnlp.qcri.org/tbcov).")
        
        st.write("### Stringency Index")
        st.write("We obtained the stringency index data from the Oxford Coronavirus Government Response Tracker (OxCGRT). "
                "This dataset provides daily stringency index values for each country.Stringency Index, a composite measure of nine of the response metrics : school closures; workplace closures; cancellation of public events; restrictions on public gatherings; closures of public transport; stay-at-home requirements; public information campaigns; restrictions on internal movements; and international travel controls. For more information about OxCGRT, "
                "visit [their website](https://ourworldindata.org/covid-stringency-index). You can download the data directly "
                "from [here](https://covid.ourworldindata.org/data/owid-covid-data.csv).")

    # Data Preparation Expander
    with st.expander("Data Preparation"):
        st.write("To prepare the data, we start with the raw tweets data that includes tweet IDs, dates, times, sentiment labels, and more. "
                "We then group this data by day to calculate the daily tweet count for each sentiment category. We normalize these counts by "
                "dividing them by the total number of tweets to obtain the proportion of each sentiment category for each day. To create a smoother "
                "trend, we apply a moving average with a window size of 7. Subsequently, we merge the stringency index data from OxCGRT with our processed data.")
        
        st.write("### `data_preparation` Script")
        st.write("To use the `data_preparation` script from the [Github Repository](https://github.com/mohamedkhaled232/Application-of-Social-Media-Data-in-COVID-19-Research) , follow these steps:")
        st.write("1. Download the tweet data for your selected countries from [here](https://crisisnlp.qcri.org/tbcov) and unzip it.")
        st.write("2. Download the stringency index CSV file from [here](https://covid.ourworldindata.org/data/owid-covid-data.csv).")
        st.write("3. The script works on a per-country basis, so provide the following inputs:")
        st.write("   - Path to the folder containing the country's tweet data (the folder should contain TSV files for the country).")
        st.write("   - Path to the stringency index CSV file.")
        st.write("   - Directory where you want to save the output.")
        st.write("   - Country name (ensure it matches the name in the stringency index CSV file).")
        st.write("4. The script filters and retains only the necessary columns. Since our focus is on negative tweets, "
                "it preserves the negative smoothed normalized tweet counts, stringency index, and the day. However, "
                "you can retain additional columns for other purposes. The output TSV files are stored in the 'data' folder "
                "for use in the web app.")

    # Web Application Expander
    with st.expander("Web Application sections"):
        st.write("Our web application consists of two sections:")
        
        st.write("### 1. Correlation Plot")
        st.write("In this section, you can select a country and a specific time period. The first plot displays trends for the stringency index "
                "and normalized negative sentiment tweet counts. The second plot presents a time series trend of the Pearson correlation coefficient, "
                "as well as the overall Pearson correlation coefficient for the selected period. The time series plot of the Pearson correlation coefficient "
                "is calculated using a rolling moving average with a window size equal to the number of days you select divided by 7. Smaller selected periods "
                "yield more accurate calculations.")
        
        st.write("### 2. Different Countries' Trends")
        st.write("In this section, you can analyze multiple countries simultaneously and compare their stringency index trends, negative tweet counts, "
                "or correlations between the stringency index and negative tweet counts trends. Once again, the time series plot of the Pearson correlation "
                "coefficient is calculated using a rolling moving average with a window size equal to the number of days you select divided by 7.")
        
        
    st.write("*Note*: This web app is built using Python and Streamlit.")



if selected== 'Correlation Plot' :
   # Add a title to your app
    st.title(" Correlation Plot ( Stringency Index - Negative Sentiment Tweet Count )")

    # Create a select box for country selection
    default_ix = country_names.index('Germany')
    selected_country = st.selectbox("Select a country:", country_names, index=default_ix)

    url = os.path.join(dir_path, f"Data/{selected_country}.tsv")

        
    df = pd.read_csv(url, sep='\t')

    # Set default values for the date range
    default_start_date = datetime(2020, 2, 1)
    default_end_date = datetime(2021, 2, 28)

    # Create a double-ended slider for selecting the date range
    start_date, end_date = st.slider(
        "Select date range",
        min_value=default_start_date,
        max_value=default_end_date,
        value=(default_start_date, default_end_date),
        format="MM/DD/YYYY",
    )


    days_difference = (end_date - start_date).days

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df['day'] = pd.to_datetime(df['day'])
    df = df[(df['day'] >= start_date) & (df['day'] <= end_date)]

    df.reset_index(drop=True, inplace=True)


    # Assuming you have already defined df and days_difference

    x = df['day']
    y1 = df['normalized_tweet_count_-1_smoothed']
    y2 = df['stringency_index']

    correlation_y1_y2 = np.corrcoef(y1, y2)[0, 1]

    # Create the first plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.plot(x, y1, color='tab:blue', label='Normalized Negative Tweet count')
    ax1.set_xlabel('Day')
    ax1.set_ylabel('Normalized Tweet Count', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_xlim(min(x), max(x))  # Set the same x-axis limits for both plots
    plt.grid(True)

    ax2 = ax1.twinx()
    # Plot y2 on the second y-axis (ax2)
    ax2.plot(x, y2, color='tab:green', label='Stringency Index')
    ax2.set_ylabel('Stringency Index', color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:green')
    ax2.set_xlim(min(x), max(x))  # Set the same x-axis limits for both plots

    # Combine the legends from both axes
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')
    plt.title('Stringency Index - Normalized Negative Sentiment Tweet count')

    plt.tight_layout()
    plt.show()

    st.pyplot(plt)

    def download_plot():
        # Save the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # Create a download button
        st.download_button(
            label="Download Plot",
            data=buffer,
            file_name="sample_plot.png",
            key="download_plot"
        )

    # Call the download_plot function to add the download button
    download_plot()
    
    correlation_y1_y2 = np.corrcoef(y1, y2)[0, 1]
    st.write("Pearson correlation coefficient between Stringency Index and normalized negative sentiment tweet count for the overall selected period =", correlation_y1_y2)
    

    # Calculate the window_size by dividing days_difference by 7
    window_size = int(days_difference / 7)
    df['rolling_correlation'] = df['normalized_tweet_count_-1_smoothed'].rolling(window=window_size).corr(df['stringency_index'])
    plt.figure(figsize=(12, 6))
    plt.plot(df['day'], df['rolling_correlation'], label='Rolling Correlation', color='tab:blue')
    plt.xlabel('Day')  # Change 'Date' to 'Day' for consistency with the first plot
    plt.ylabel('Rolling Correlation')
    plt.title('Correlation Between Stringency Index and Normalized Negative Sentiment Tweet Count')
    plt.legend()
    plt.grid(True)
    plt.xlim(min(x), max(x))  # Set the same x-axis limits for both plots
    plt.tight_layout()
    plt.show()
    st.pyplot(plt)

    def download_plot1():
        # Save the first plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # Create a download button for the first plot
        st.download_button(
            label="Download Plot",
            data=buffer,
            file_name="sample_plot1.png",
            key="download_plot1"
        )

    # Call the download_plot1 function to add the download button for the first plot
    download_plot1()

    
    st.write("This time series plot of the Pearson correlation coefficient is calculated using a rolling moving average with a window size  =", window_size)   



if selected== "Different Countries' Trends" :
    st.title('Explore Different Countries\' Trends ')
    selected_option = st.radio("Select a parameter:", ["Stringency Index", "Negative Tweets", "Correlation between Stringency Index and Normalized Negative Tweet count"])




    # Initialize selected_factor variable
    selected_factor = ""

    # Set selected_factor based on the user's choice
    if selected_option == "Stringency Index":
        selected_factor = 'stringency_index'
    elif selected_option == "Negative Tweets":
        selected_factor = 'normalized_tweet_count_-1_smoothed'
    elif selected_option == "Correlation between Stringency Index and Normalized Negative Tweet count":
        selected_factor = 'rolling_correlation'





    # Function to load data and plot
    def plot_time_series(country_name, color, start_date, end_date):
        # Construct the path to the TSV file based on the selected country
        file_path = os.path.join(dir_path, f"Data/{country_name}.tsv")
        
        # Load the data from the TSV file
        data = pd.read_csv(file_path, sep='\t')

        # Filter data based on the selected date range
        data['day'] = pd.to_datetime(data['day'])
        filtered_data = data[(data['day'] >= start_date) & (data['day'] <= end_date)]
        
        days_difference = (end_date - start_date).days
        window_size = int(days_difference / 7)
        
        filtered_data['rolling_correlation'] = filtered_data['normalized_tweet_count_-1_smoothed'].rolling(window=window_size).corr(filtered_data['stringency_index'])

        # Create a line plot with a specified color
        plt.plot(filtered_data['day'], filtered_data[selected_factor], label=f'{country_name}', color=color)
        

    # Streamlit app
    def main():
        

        # Create checkboxes for country selection
        selected_countries = st.multiselect('Select Countries:', country_names)

        # Create a double-ended slider for selecting the date range
        default_start_date = datetime(2020, 2, 1)
        default_end_date = datetime(2021, 2, 28)
        start_date, end_date = st.slider(
            "Select date",
            min_value=default_start_date,
            max_value=default_end_date,
            value=(default_start_date, default_end_date),
            format="MM/DD/YYYY",
        )

        # Define a list of colors for the lines
        colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan', 'g', 'r', 'c', 'm', 'y', 'k', 'purple', 'orange', 'lime', 'pink', 'brown', 'gray', 'teal']
        
        # Create a Matplotlib figure explicitly
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot and display selected countries
        if selected_countries:
            st.subheader(f'{selected_option} Time Series')
            
            for i, country in enumerate(selected_countries):
                color = colors[i % len(colors)]  # Cycle through colors
                plot_time_series(country, color, start_date, end_date)
            
            ax.set_xlabel('Day')
            ax.set_ylabel(selected_option)
            plt.grid(True)
            ax.legend()  # Adjust the legend position
            plt.tight_layout()
            st.pyplot(fig)  # Pass the Matplotlib figure to st.pyplot       

    if __name__ == '__main__':

        main()

    def download_plot2():
        # Save the second plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # Create a download button for the second plot
        st.download_button(
            label="Download Plot",
            data=buffer,
            file_name="sample_plot2.png",
            key="download_plot2"
        )

    # Call the download_plot2 function to add the download button for the second plot
    download_plot2()
    
    








