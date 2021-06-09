import datetime
import time
import pandas as pd
import numpy as np
import os
from tabulate import tabulate

CITY_DATA = {'chicago': 'short.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_OF_YEAR = ('january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                 'november', 'december', 'all')

DAY_OF_WEEK = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare dataS!')

    while True:
        city = input('\nplease insert city \n')
        if city.lower() not in CITY_DATA:
            print("Unknown city! Please take one of ", CITY_DATA.keys())
            continue
        else:
            break

    while True:
        month = input('please insert month:\n')
        if month.lower() not in MONTH_OF_YEAR:
            print("Unknown month! Please take one of ", MONTH_OF_YEAR)
            continue
        else:
            break

    while True:
        day = input('please insert day of week:\n')
        if day.lower() not in DAY_OF_WEEK:
            print("Unknown day! Please take one of ", DAY_OF_WEEK)
            continue
        else:
            break
    print('Calculating for city: {} in month: {} for day: {}: '.format(city, month, day))
    print('-' * 40)
    return city.lower(), month.lower(), day.lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_OF_YEAR.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def hour_stats(df):
    """
    Displays statistics on the hour of travel

    Args:
        df - Pandas DataFrame to explore

    Returns:
         nothing
    """
    # display the most common start hour
    column_name = 'Start Time'
    hour_column_name = 'hour'
    df[column_name] = pd.to_datetime(df[column_name])
    # extract hour from the Start Time column to create an hour column
    df[hour_column_name] = df[column_name].dt.hour

    # find the most popular hour
    popular_hour = df[hour_column_name].value_counts().idxmax()
    print('Most Popular Start Hour:', popular_hour)


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame to explore

    Returns:
         nothing
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if 'month' in df.columns and len(df['month'].value_counts()) > 1:
        popular_month = df['month'].value_counts().idxmax()
        print("Most popular month: ", MONTH_OF_YEAR[popular_month-1])
    else:
        print('Only one month selected!')

    # display the most common day of week
    if 'day_of_week' in df.columns and len(df['day_of_week'].value_counts()) > 1:
        popular_day = df['day_of_week'].value_counts().idxmax()
        print("Most popular day in week: ", popular_day)
    else:
        print('Only one day of week selected!')

    hour_stats(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame to explore

    Returns:
         nothing
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    combinations = df.groupby(['Start Station', 'End Station']).count().iloc[0:, 2]
    favorite_combination_str = str(combinations.idxmax()).replace("('", "").replace("')", "")
    print("Most popular combination:\nFrom -> ", favorite_combination_str.split("', '")[0], " to -> ", favorite_combination_str.split("', '")[1], combinations.max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame to explore

    Returns:
         nothing
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df[["Trip Duration"]].sum()
    total_trips = df[["Trip Duration"]].count()
    print("Total travel time: {} seconds in {} trips".format(total_travel_time.iloc[0], total_trips.iloc[0]))

    # display mean travel time
    mean_travel_time = df[["Trip Duration"]].mean()
    print("Mean travel time: {} seconds".format(mean_travel_time.iloc[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_types_count(column_name, df):
    """
    Display all values of column_name in df with the count of occurrence
    Args:
        (str) column_name - name of the column in the dataframe to group by
        df - Pandas DataFrame to explore

    Returns:
         nothing
    """
    default_value = "no set"
    if column_name in df.columns:
        types_series = df.fillna(default_value).groupby([column_name])[column_name].count()
        print(column_name, ":")
        for k in types_series.index:
            print("{}:\t\t{}".format(k, types_series[k]))
    else:
        print("No", column_name, "information given!")
    print("")


def birth_year_stats(df):
    """
    Display statistics regarding year of birth of users
    Args:
        df - Pandas DataFrame to explore

    Returns:
         nothing
    """
    column_name = 'Birth Year'
    if column_name in df.columns:
        earliest_year_of_birth = df[column_name].min()
        print("Earliest year of birth:\t\t", int(earliest_year_of_birth))

        most_recent_year_of_birth = df[column_name].max()
        print("Most recent year of birth:\t", int(most_recent_year_of_birth))

        most_common_year_of_birth = df[column_name].value_counts().idxmax()
        print("Most common year of birth:\t", int(most_common_year_of_birth))
    else:
        print("No year of birth given!")


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    Args:
        df - Pandas DataFrame to explore

    Returns:
         nothing
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print_types_count("User Type", df)
    # Display counts of gender
    print_types_count("Gender", df)

    # Display earliest, most recent, and most common year of birth
    birth_year_stats(df)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Display data slices from trip list in table layout
    Args:
        df - Pandas DataFrame to explore

    Returns:
         nothing
    """
    print ("We found ", len(df), " trips.")
    view_data = input(
        "\nWould you like to view 5 rows of individual trip data? Pres any key to continue or \"no\" to stop \n")
    start_loc = 0
    slice_size = int(5)
    while view_data != 'no':
        if start_loc >= len(df):
            print("You have already seen all trip data")
            break
        if start_loc+slice_size > df.size:
            end_loc = df.size
        else:
            end_loc = start_loc+slice_size
        print(tabulate(df.iloc[start_loc:end_loc, 1:len(df.columns)], headers="keys", tablefmt="psql"))
        start_loc += slice_size
        view_data = input("Do you wish to see more?: ").lower()


def main():
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 300)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty:
            print("No data available - please try again")
            continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input("\nWould you like to restart? Enter any key or \"no\" to exit.\n")
        if restart.lower() == 'no':
            break


if __name__ == "__main__":
    main()
