import time
import pandas as pd
import numpy as np

# In addition to the CITY_DATA dictionary, I create lists for all possible months and days including 'all', if the user does not want to filter at all.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s look at some US bikeshare data!')
    # I want to get user input for the city choice using a while loop to handle inputs that are not part of CITY_DATA.
    # I want to get user input for the city choice using a while loop to handle inputs that are not part of CITY_DATA.
    while True:
        city = input("\nDo you want analyze data from Chicago, New York City, or Washington? Answer with the name of the requested city!\n").lower()
        if city in CITY_DATA:
            break
        else:
            print("\nPlease enter a valid city name (Chicago, New York City, or Washington.\n")

    # I want to get user input for the month filter using a while loop to handle inputs that are not part of MONTH_DATA.
    while True:
        month = input("\nWhich month do you want to filter? January, Feburary, March, April, May, or June? Type all if you do not want to filter by month.\n").lower()
        if month in MONTH_DATA:
            break
        else:
            print("\nPlease enter a valid month or all if you do not want to filter.\n")

    # I want to get user input for the weekday filter using a while loop to handle inputs that are not part of DAY_DATA.
    while True:
        day = input("\nWhich weekday do you want to see? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? Type all if you do not want to filter by weekday.\n").lower()
        if day in DAY_DATA:
            break
        else:
            print("\nPlease enter a valid weekday or all if you do not want to filter.\n")

    print('-'*40)
    return city, month, day

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
    # I upload the data from the file for the city chosen by the user into the dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # To handle the data with pandas, I need to convert 'Start Time' to datetime. Afterwards, I create seperate columns for month, weekday, and start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # If the user did not input 'all', the data is filtered by the chosen month.
    # As I asked for the name of the month earlier, I use the index function to get the integer from the list.
    # As the list starts with 'all', the index of January is 1, February 2 etc.
    if month != 'all':
        month = MONTH_DATA.index(month)
        df = df[df['month'] == month]

    # Same for weekdays
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month using 'mode'
    popular_month = df['month'].mode()[0]
    print('The most popular month: ', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular day: ', popular_day)

    # display the most common start hour
    popular_start_hour = df['hour'].mode()[0]
    print('The most popular start hour: ', popular_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    combined_trip = (df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    print('The most frequent combination of start station and end station trip: ', combined_trip)

    ("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

     # display total travel time as the sum of the 'Trip Duration' column, given the filters. The time is given in seconds and therefore divided by 60 to transform it to minutes.
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time: ', total_travel_time/60, 'minutes')

    # display mean travel time as the mean of the 'Trip Duration' column, given the filters. The time is given in seconds and therefore divided by 60 to transform it to minutes.
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time: ', mean_travel_time/60, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The distribution of user types:\n', user_types)

   # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('The distribution of genders:\n', gender)
    else:
        print('There is no data on gender for this city/the selected time.')

    # Display earliest, most recent, and most common year of birth. Using integers for the years
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        print('The earliest birth year: ', int(earliest_birth_year))
        most_recent_birth_year = df['Birth Year'].max()
        print('The most recent birth year: ', int(most_recent_birth_year))
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('The most common birth year: ', int(most_common_birth_year))
    else:
        print("There is no data on birth years for this city/the selected time.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):

    # Asking the user if they want to see some lines of raw data. If they answer 'yes' they are asked if they want to see another five lines etc. until they say no.

    data = 0

    while True:
        user_input = input('Would you like to see the first/next 5 lines of raw data? Enter yes or no: ').lower()
        if user_input not in ['yes', 'no', 'yeah']:
            print('Please type either yes, yeah or no.\n')

        elif user_input == 'yes' or 'yeah':
            print(df.iloc[data : data+5])
            data += 5

        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
