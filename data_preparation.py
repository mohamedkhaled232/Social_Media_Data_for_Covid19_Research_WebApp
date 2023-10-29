import os
import pandas as pd
import numpy as np


# This script is used to prepare the data for using it in the web app 
# First you need to download the country tweets data from here : https://crisisnlp.qcri.org/tbcov and unzip it
# And to download the stringency index data using this URL : https://covid.ourworldindata.org/data/owid-covid-data.csv

# The script will ask you to enter 4 things:
# 1- the path of the folder containing the TSV file/files that you downloaded from the crisisnlp website for the desired country
# 2- the path for the output folder where you want to save the final tsv file
# 3- the name of the country (the same of the country should be similar to the name of the country in the stringency index csv file)
# 4- the path of the csv file that contain the stringency index

# Enter the folder path containing the TSV file/files for the desired country
folder_path = input("Please enter the path of the folder containing the TSV file/files: ")

if not os.path.exists(folder_path):
    print(f"The folder {folder_path} does not exist.")
    exit()

# Get a list of TSV files in the folder
tsv_files = [f for f in os.listdir(folder_path) if f.endswith('.tsv')]

if not tsv_files:
    print(f"No TSV files found in the folder {folder_path}.")
    exit()

# the path for the output folder and the name of the country
# the same of the country should be similar to the name of the country in the stringency index file
output_folder = input("Please enter the path of the folder where you want to save the output (final tsv file): ")
if not os.path.exists(output_folder):
    print(f"The folder {output_folder} does not exist.")
    exit()
output_filename = input("Please enter (the country name ): ")

output_filename = output_filename.title()

# the path of the csv file that contain the stringency index
actual_data_file = input("path of the csv file that contain the stringency index: ")

# the script will read only the date_time and sentiment_label columns and if there is more than 1 tsv file for the same country it will concatenate them
columns_to_read = ['date_time', 'sentiment_label']

# this empty list to store the data frame
dfs = []

# append the data to dfs list
for tsv_file in tsv_files:
    tsv_file_path = os.path.join(folder_path, tsv_file)
    df = pd.read_csv(tsv_file_path, sep='\t', usecols=columns_to_read)
    dfs.append(df)

concatenated_df = pd.concat(dfs, ignore_index=True)

# convert 'date_time' column to datetime object to use it for the filtering step
concatenated_df['date_time'] = pd.to_datetime(concatenated_df['date_time'])

# filter rows with dates (I used the full range of the tweets data)
start_date = pd.to_datetime('2020-02-01')
end_date = pd.to_datetime('2021-04-01')
country_tweets_df = concatenated_df[(concatenated_df['date_time'] >= start_date) & (concatenated_df['date_time'] <= end_date)].copy()

# the path of the csv file that contain the stringency index
actual_data = pd.read_csv(actual_data_file)

#  extract day from 'date_time' and create a new column (day)
country_tweets_df['day'] = country_tweets_df['date_time'].dt.date

#  grouping by day and sentiment_label, then count the number of tweets
grouped_tweets_data = country_tweets_df.groupby(['day', 'sentiment_label']).size().reset_index(name='tweet_count')


#  Reindex to fill missing days with zeros
all_days = pd.date_range(start=start_date, end=end_date, freq='D').date
all_sentiments = [-1, 0, 1]
idx = pd.MultiIndex.from_product([all_days, all_sentiments], names=['day', 'sentiment_label'])
grouped_tweets_data = grouped_tweets_data.set_index(['day', 'sentiment_label']).reindex(idx, fill_value=0).reset_index()


# Convert 'date' column to datetime object for the acual data csv file
actual_data['date'] = pd.to_datetime(actual_data['date'], format='%Y-%m-%d')

# Filter rows by the country name
country_actual_data = actual_data[actual_data['location'] == output_filename].copy()

# Convert the 'date' column to date format (without time) for merging and creating the 'day' column
country_actual_data['day'] = country_actual_data['date'].dt.date

# Merge with country_actual_data with grouped_tweets_data on 'day' column
# in country_actual_data we choosed only ['day', 'stringency_index','new_cases'] columns
grouped_tweets_data['day'] = pd.to_datetime(grouped_tweets_data['day']).dt.date
merged_data = pd.merge(grouped_tweets_data, country_actual_data[['day', 'stringency_index','reproduction_rate','gdp_per_capita','extreme_poverty','new_cases']], on='day', how='left')

merged_data = merged_data[merged_data['day'] < merged_data['day'].max()]

merged_df = pd.DataFrame(merged_data)

# Pivot the DataFrame to create separate columns for each sentiment_label
pivot_merged_df = merged_df.pivot(index='day', columns='sentiment_label', values='tweet_count').fillna(0)

# Reset the index to make 'day' a regular column again
pivot_merged_df = pivot_merged_df.reset_index()

# Rename the columns for better clarity
pivot_merged_df.columns = ['day', 'tweet_count_-1', 'tweet_count_0', 'tweet_count_1']

# Merge with the original DataFrame on 'day' and 'stringency_index'
final_merged_df = pd.merge(pivot_merged_df, merged_df[['day', 'stringency_index','reproduction_rate','gdp_per_capita','extreme_poverty', 'new_cases']].drop_duplicates(), on='day')

# Calculate the sum of the tweet counts per day and insert it as a column
sum_of_tweet_counts = final_merged_df[['tweet_count_-1', 'tweet_count_0', 'tweet_count_1']].sum(axis=1)
final_merged_df.insert(final_merged_df.columns.get_loc('tweet_count_1') + 1, 'sum_tweet_counts', sum_of_tweet_counts)

# Calculate the normalized columns by dividing each sentiment category count for each day by the sum of the tweet counts for that day
normalized_tweet_count_minus_1 = final_merged_df['tweet_count_-1'] / final_merged_df['sum_tweet_counts']
normalized_tweet_count_0 = final_merged_df['tweet_count_0'] / final_merged_df['sum_tweet_counts']
normalized_tweet_count_1 = final_merged_df['tweet_count_1'] / final_merged_df['sum_tweet_counts']
# Insert the normalized columns
final_merged_df.insert(final_merged_df.columns.get_loc('sum_tweet_counts') + 1, 'normalized_tweet_count_-1', normalized_tweet_count_minus_1)
final_merged_df.insert(final_merged_df.columns.get_loc('normalized_tweet_count_-1') + 1, 'normalized_tweet_count_0', normalized_tweet_count_0)
final_merged_df.insert(final_merged_df.columns.get_loc('normalized_tweet_count_0') + 1, 'normalized_tweet_count_1', normalized_tweet_count_1)

# Calculate the sum of 0 , 1 tweets count and insert it
sum_of_tweet_count_0_and_1 = final_merged_df['tweet_count_0'] + final_merged_df['tweet_count_1']
normalized_sum_of_tweet_count_0_and_1 = sum_of_tweet_count_0_and_1 / final_merged_df['sum_tweet_counts']
final_merged_df.insert(final_merged_df.columns.get_loc('normalized_tweet_count_1') + 1, 'normalized_sum_tweet_count_0_and_1', normalized_sum_of_tweet_count_0_and_1)

# Smoothing the tweets count ( moving average)
# Define a window size for the moving average smoothing
window_size = 7

# Apply moving average smoothing to each column and insert them
columns_to_smooth = ['tweet_count_-1', 'tweet_count_0', 'tweet_count_1', 'sum_tweet_counts',
                    'normalized_tweet_count_-1', 'normalized_tweet_count_0', 'normalized_tweet_count_1',
                    'normalized_sum_tweet_count_0_and_1']

for column in columns_to_smooth:
    smoothed_column_name = f'{column}_smoothed'
    final_merged_df[smoothed_column_name] = final_merged_df[column].rolling(window=window_size, min_periods=1).mean()

# Because there is a gap in the tweets data and this gap is count as zero tweets 
# So we need to replace the zeros with NaNs and then apply linear interpolation to fill the missing values
columns_to_replace = ['tweet_count_-1', 'tweet_count_0', 'tweet_count_1', 'sum_tweet_counts',
        'normalized_tweet_count_-1', 'normalized_tweet_count_0', 'normalized_tweet_count_1', 'normalized_sum_tweet_count_0_and_1',
        'tweet_count_-1_smoothed', 'tweet_count_0_smoothed', 'tweet_count_1_smoothed', 'sum_tweet_counts_smoothed',
        'normalized_tweet_count_-1_smoothed', 'normalized_tweet_count_0_smoothed', 'normalized_tweet_count_1_smoothed', 'normalized_sum_tweet_count_0_and_1_smoothed']
final_merged_df[columns_to_replace] = final_merged_df[columns_to_replace].replace(0, np.nan)

# Linear interpolation to fill the missing values
final_merged_df[columns_to_replace] = final_merged_df[columns_to_replace].interpolate(method='linear')

# Adding noise to the stringency index column is needed for calculating person correlation coefficient
# Because if the window size is small and the stringency index is constant for a period of time then the correlation coefficient will be NaN
noise = 0.001  # You can adjust this value as needed
final_merged_df['stringency_index'] = final_merged_df.groupby('stringency_index', group_keys=False)['stringency_index'].apply(lambda x: x + np.random.uniform(-noise, noise, len(x)))

# For the sack of simplicity and size we will keep only the columns that we need 
# keep only the columns that you want with the order that you want
desired_column_order = [
    'day', 'stringency_index','normalized_tweet_count_-1_smoothed'
]


final_merged_df = final_merged_df[desired_column_order]

# Save the final merged DataFrame to tsv file
output_file_path = os.path.join(output_folder, f'{output_filename}.tsv')
final_merged_df.to_csv(output_file_path, sep='\t', index=False)
