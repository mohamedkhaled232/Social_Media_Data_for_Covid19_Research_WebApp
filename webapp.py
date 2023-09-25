
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
    selected = option_menu("Main Menu", ["Home", 'correlation', 'countries comparison'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=0)
    

if selected== "Home" :
    st.title("Hi")


if selected== "correlation" :
   # Add a title to your app
    st.title("Stringency - Negative Sentiment Tweets")

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

    ax1.plot(x, y1, color='tab:blue', label='Negative Tweets')
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
    plt.title('Negative tweets - Stringency Index')

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
    st.write("Pearson Correlation Coefficient Between Stringency & Negative Sentiment Tweets =", correlation_y1_y2)
    

    # Calculate the window_size by dividing days_difference by 7
    window_size = int(days_difference / 7)
    df['rolling_correlation'] = df['normalized_tweet_count_-1_smoothed'].rolling(window=window_size).corr(df['stringency_index'])
    plt.figure(figsize=(12, 6))
    plt.plot(df['day'], df['rolling_correlation'], label='Rolling Correlation', color='tab:blue')
    plt.xlabel('Day')  # Change 'Date' to 'Day' for consistency with the first plot
    plt.ylabel('Rolling Correlation')
    plt.title('Rolling Correlation between Tweet Count and Stringency Index')
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

    
    st.write("windows size =", window_size)   



if selected== "countries comparison" :
    st.title('Countries Comparison')
    selected_option = st.radio("Select a parameter:", ["Stringency Index", "Negative Tweets", "Correlation between Stringency Index and Negative Tweets"])




    # Initialize selected_factor variable
    selected_factor = ""

    # Set selected_factor based on the user's choice
    if selected_option == "Stringency Index":
        selected_factor = 'stringency_index'
    elif selected_option == "Negative Tweets":
        selected_factor = 'normalized_tweet_count_-1_smoothed'
    elif selected_option == "Correlation between Stringency Index and Negative Tweets":
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
        # Define the directory path for your data
        #dir_path = "/path/to/your/data/directory"
        
        # Define your list of country names
        #country_names = ['Country1', 'Country2', 'Country3']  # Replace with your list of country names
        
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








