import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')

def get_filters():
    """Ask user to specify city(ies) and filters, month(s) and weekday(s).
    Returns:
        (str) city -name of the city(ies) to analyze
        (str) month -name of the month(s) to filter
        (str) day -name of the day(s) of week to filter
    """

    print("\n\nLet's explore some US bikeshare data!\n")

    print("Type end at any time if you would like to exit the program.\n")

    while True:
        cities = CITY_DATA.keys()
        city = input("\nPlease input city of your choice (Chicago,Washington,New york City \n").lower()
        if city in cities:
            break
        else:
            print("Please eneter corrent input")
    
    while True:
        month = input("\nEnter Month for which data needs to be considered from January to June\n").lower()
        if month in months:
            break
        else:
            print("\nPlease input valid month from January to June\n")
    while True:
        day = input("\nPlease enter a valid day from Monday to sunday\n").lower()
        if day in weekdays:
            break
        else:
            print("\n Kindly input days from Monday to Sunday \n")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data for the specified filters of city(ies), month(s) and
       day(s) whenever applicable.
    Args:
        (str) city - name of the city(ies) to analyze
        (str) month - name of the month(s) to filter
        (str) day - name of the day(s) of week to filter
    Returns:
        df - Pandas DataFrame containing filtered data
    """

    start_time = time.time()

    # filter the data according to the selected city filters
    df = pd.read_csv(CITY_DATA[city])
        
    # create columns to display statistics
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the data according to month and weekday into two new DataFrames
    if month in months:
        df = df[df['Month'] == (months.index(month)+1)]
        
    if day in weekdays:
        df = df[df['Weekday'] == day.title()]
        
    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)
    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""

    print('\nDisplaying the statistics on the most frequent times of '
          'travel...\n')
    start_time = time.time()

    # display the most common month
    
    most_common_month = df['Month'].mode()[0]
    most_travel_month = months[most_common_month-1]
    print('Most trave Month is: ' + most_travel_month.title() + '.')

    # display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('Most common day of the week is: ' + most_common_day + '.')

    # display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('Most common start hour is: ' +str(most_common_hour) + '.')

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print("The most common start station is: " +most_common_start_station)

    # display most commonly used end station
    most_common_end_station = str(df['End Station'].mode()[0])
    print("The most common start end is: " + most_common_end_station)

    # display most frequent combination of start station and
    # end station trip
    df['Start-End Combination'] = (df['Start Station'] + ' - ' + df['End Station'])
    most_common_start_end_combination = str(df['Start-End Combination'].mode()[0])
    print("The most common start-end combination ""of stations is: " + most_common_start_end_combination)

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time  # looked for help from github on how to format this 
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) +
                         'd ' +
                         str(int((total_travel_time % 86400)//3600)) +
                         'h ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +
                         'm ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +
                         's')
    print('Total travel time is : ' +
          total_travel_time + '.')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' +
                        str(int(mean_travel_time % 60)) + 's')
    print("Mean travel time is : " +
          mean_travel_time + ".")

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)


def user_stats(df, city):
    """Display statistics on bikeshare users."""
    """Added checks for no gender in dataset"""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("Distribution for user types:",user_counts)
    if 'Gender' not in df:
        print("No gender data available")
    else:
       gender_distribution = df['Gender'].value_counts()
       print("\nDistribution for each gender:",gender_distribution)
    
    # Display earliest, most recent, and most common year of birth
    if 'Gender' not in df:
        print("No Birth Year data available")
    else:
        earliest_birth_year = str(int(df['Birth Year'].min()))
        print("\nOldest person to ride one bike was born in: " + earliest_birth_year)
        most_recent_birth_year = str(int(df['Birth Year'].max()))
        print("Youngest person to ride one bike was born in: " + most_recent_birth_year)
        most_common_birth_year = str(int(df['Birth Year'].mode()[0]))
        print("Most common birth year amongst riders is: " + most_common_birth_year)
    
    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

def data_display(df):
    counter = 0
    while True:
        for i in range(counter, len(df.index)):
            print("\n")
            print(df.iloc[counter:counter+5].to_string())
            print("\n")
            counter += 5
            prompt = input("\nDo you want to display more y or n \n").lower()
            if prompt == 'y':
                if (counter> len(df.index):
                        print("No more data to display")
                continue
            else:
                break
        break

def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data = input("\nWould you like to display raw data 5 rows at a time  \n").lower()
        if display_data == 'y':
            data_display(df)
        restart = input("\nWould you like to restart?\n\n[y]Yes\n[n]No\n\n>")
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
