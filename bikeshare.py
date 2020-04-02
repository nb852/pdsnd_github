import time
import pandas as pd
import numpy as np

#Dictionary containing datasets for the three cities.

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Lists of months and days for filters.

MONTH_DATA = { 'january',
               'february',
               'march',
               'april',
               'may',
               'june',
               'all' }

DAY_DATA = { 'monday',
             'tuesday',
             'wednesday',
             'thursday',
             'friday',
             'saturday',
             'sunday',
             'all'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #User input
    city = input("Would you like to analyse Chicago, New York City or Washington? Please enter: ").lower()
    while city not in CITY_DATA:
        print("Please enter one of the three cities.")
        city = input("Would you like to analyse Chicago, New York City or Washington? Please enter: ").lower()
    print("You have selected: {}".format(city).title())

    month = input("Which month from January through to June would you like to analyse? Enter 'all' for no filter. Please enter: ")
    while month not in MONTH_DATA:
        print("Please enter one month or 'all' for no filter.")
        month = input("Which month from January through to June would you like to analyse? Enter 'all' for no filter. Please enter: ")
    print("You have selected: {}".format(month).title())

    day = input("Which day of the week would you like to analyse? Enter 'all' for no filter. Please enter: ")
    while day not in DAY_DATA:
        print("Please enter the name of a day or 'all' for no filter.")
        day = input("Which day of the week would you like to analyse? Enter 'all' for no filter. Please enter: ")
    print("You have selected: {}".format(day).title())

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
    # Load selected city data
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if single month was selected
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    # Filter by day of week if single day was selected
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("Calculating The Most Frequent Times of Travel...")
    start_time = time.time()

    common_month = df['month'].mode()[0]
    # Added note for reference as month is listed numerically
    print("Note: January is 1, February is 2, March is 3, April is 4, May is 5, June is 6.")
    print("The most common month of travel is {}.".format(common_month))

    common_day = df['day_of_week'].mode()[0]
    print("The most common day of travel is {}.".format(common_day.title()))

    # Singling out hour into new column
    df['start_hour'] = df['Start Time'].dt.hour
    common_hour = df['start_hour'].mode()[0]
    print("The most common hour to start a ride is {}.".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common station to start a ride from is {}.".format(common_start_station.title()))

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common station to end a ride from is {}.".format(common_end_station.title()))

    # TO DO: display most frequent combination of start station and end station trip
    # Concatenating start and end columns to create a trip combination column
    df['trip_combo'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    # Calculating most common trip combination
    most_common_trip = df['trip_combo'].mode()[0]
    print("The most common trip combination is {}.".format(most_common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # Calculating sum of travel time in seconds
    total_travel_secs = df['Trip Duration'].sum()
    # Converting total travel time to hours and rounding to one decimal place
    total_travel_hrs = round(total_travel_secs / 3600, 1)
    print("The total travel time was {} hours.".format(total_travel_hrs))

    # TO DO: display mean travel time
    # Calculating average of travel time in seconds
    mean_travel_secs = df['Trip Duration'].mean()
    # Converting mean travel time to minutes and rounding to one decimal place
    mean_travel_mins = round(mean_travel_secs / 60, 1)
    print("The average travel time was {} minutes.".format(mean_travel_mins))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_count = df['User Type'].value_counts()
    print("The counts of the different user types are listed below:")
    print(user_count)

    # TO DO: Display counts of gender
    # Handling exception as there is no gender column for Washington
    try:
        gender_count = df['Gender'].value_counts()
        print("\nThe gender counts are listed below:")
        print(gender_count)
    except:
        print("There is no gender data for this dataset.")

    # TO DO: Display earliest, most recent, and most common year of birth
    #Handling exception as there is no year of birth column for Washington
    #Integers used to show only the four digits over the years
    try:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print("\nThe earliest year of birth is {}.".format(earliest_year))
        print("The most recent year of birth is {}.".format(recent_year))
        print("The most common year of birth is {}.".format(common_year))
    except:
        print("There is no data for year of birth for this dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    """Displays 5 rows of raw data until the user chooses not to continue."""
    #Creating list for of responses to the question
    response_list = ['yes', 'no']
    #Row number variable set to 0 initially. Variable will be used to cycle through the raw data.
    row_a = 0
    row_b = 5
    more_data = input("\nSee raw data? Enter yes or no: ").lower()
    while more_data not in response_list:
        print("Please select yes or no.")
        more_data = input("\nSee raw data? Enter yes or no: ").lower()
    print("\nPrinting raw data...")
    #Printing first five rows of data
    print(df.head())

    #Asking whether user wishes to continue
    while more_data == 'yes':
        print("Would you like to see more data? Yes or No: ")
        #Increasing row numbers by 5 to show next 5 rows
        row_a += 5
        row_b += 5
        more_data = input().lower()
        if more_data == 'yes':
        #Printing from current row number and next 4 rows
            print(df[row_a:row_b])
        #Breaking loop if user does not wish to continue
        elif more_data != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
