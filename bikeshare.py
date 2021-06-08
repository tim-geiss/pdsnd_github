import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months_moglich = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
tag_moglich=['all','0','1','2','3','4','5','6']

def get_filters():
   
    print('Hello! Let\'s explore some US bikeshare data!')
    city = input("City Name (chicago, new york city, washington): ").lower()
    while city not in CITY_DATA:
        city = input("Please again, only this cities(chicago, new york city, washington):").lower()
       
    monat = input("Month (all or january, february,...,june): ").lower()
    while monat not in months_moglich:
        monat = input("Please again, only name of months or all (all or january, february,..,june): ").lower()
        
    tag = input("Day (all or monday=0, tuesday=1, ...): ").lower()
    while tag not in tag_moglich :
        tag = input("Please again, only all or 0-6(all or monday=0, ...): ").lower()
    print('-'*40)
    
    city = city
    month = monat
    day = tag
    
    return city, month, day

def load_data(city, month, day):

    if city == "chicago":
        filename = CITY_DATA["chicago"]
    elif city == "new york city":
        filename = CITY_DATA["new york city"]
    elif city == "washington":
        filename = CITY_DATA["washington"]
    
    df = pd.read_csv(filename)

    df['Start Time'] = pd.to_datetime(df['Start Time'],format='%Y-%m-%d %H:%M:%S')
    df['hour'] =  df['Start Time'].dt.hour
    df['month'] =  df['Start Time'].dt.month
    df['day_of_week'] =  df['Start Time'].dt.dayofweek

    if month != 'all':
        month = months_moglich.index(month)
        df = df.loc[(df.month==month)]
    if day != 'all':
        df = df.loc[(df.day_of_week == int(day))]
    
    return df
    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    popular_month = df.mode().max()
    print('Most Frequent Month:', int(popular_month['month']))

    popular_dayofweek = df.mode().max()
    print('Most Frequent Week Day:', int(popular_dayofweek['day_of_week']))
    
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:',popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start = df[['Start Station']].groupby(['Start Station']).size().reset_index(name='Counts').sort_values(['Counts'], ascending=False).head(1)
    print('Most Frequent Start Station: \n', popular_start)
    print('-'*10)
    
    popular_end = df[['End Station']].groupby(['End Station']).size().reset_index(name='Counts').sort_values(['Counts'], ascending=False).head(1)
    print('Most Frequent End Station: \n', popular_end)
    print('-'*10)

     most_freq_combi = df[["Start Station","End Station"]].groupby(["Start Station","End Station"])['End Station']\
        .size()\
            .reset_index(name="Counts")\
                .sort_values(['Counts'], ascending=False)\
                    .head(1)
    print('Most Frequent Station Combinations: \n',most_freq_combi,"")
    print('-'*10)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = dt.timedelta(seconds=int(df['Trip Duration'].sum()))
    print("Total Travel Time:", total_travel_time)
    
    mean_travel_time = dt.timedelta(seconds=int(df['Trip Duration'].mean()))
    print("Mean Travel Time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    counts_of_usertypes = df['User Type'].value_counts().to_string()
    print("Counts of Usertypes :\n",counts_of_usertypes)


   if 'Gender' in df:
        counts_of_gender = df['Gender'].value_counts(dropna = False).to_string()
        print("Counts of Gender :\n",counts_of_gender)

    if 'Birth Year' in df:
        counts_of_earliestyear = int(df['Birth Year'].min())
        print("Counts of Earliest Birth Year :\n",counts_of_earliestyear)
    
        counts_of_mostrecent = int(df['Birth Year'].max())
        print("Counts of Most Recent Birth Year :\n",counts_of_mostrecent)

        counts_of_birthyear = int(df['Birth Year'].mode().max())
        print("Counts of Most Birth Year :\n",counts_of_birthyear)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        row = 0
        while True:
            viewData = input("Would you like to see the raw data? Type 'Yes' or 'No'.").lower()
            if viewData == "yes":
                print('Dataframe', df.iloc[row:row+5])
                
                row += 5
            else:        
                break
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
	main()

