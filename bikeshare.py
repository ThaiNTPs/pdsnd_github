import time
import pandas as pd
import numpy as np

#the first change

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Enter the city: ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input ("Choose between chicago, new york city OR washington: ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Enter month: ').lower()
    while month not in ['all','january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Enter month (all, january, february, ... , june) : ').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter day of week : ').lower()
    while day not in ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Enter day of week (all, monday, tuesday, ... sunday) : ').lower()

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
    df = pd.read_csv('{}.csv'.format(city))
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month

    if month != 'all':
        # use specify month of the year
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if day != 'all':
        #use specify day of the week
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The most common month is: ', df['month'].value_counts().idxmax())

    # TO DO: display the most common day of week
    print('The most common day is: ', df['day_of_week'].value_counts().idxmax())

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common hour is: ', df['hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most commonly start station is: ', df ['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
    print('The most commonly end station is: ', df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station trip is: ')
    most_common_start_and_end_stations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(most_common_start_and_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum() / 3600.0
    print('total travel time in hours is: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 3600.0
    print('mean travel time in hours is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    counts_of_user_types = df['User Type'].value_counts()
    print(counts_of_user_types)

    # TO DO: Display counts of gender
    if city != 'washington':
        counts_of_gender = df['Gender'].value_counts()
        print(counts_of_gender)
        year_of_birth_earliest = int(df['Birth Year'].min())
        most_recent_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].value_counts().idxmax())
        print('The earliest year of birth is: ',year_of_birth_earliest,
          ', the most recent one is: ',most_recent_year_of_birth,
           'and the most common one is: ',most_common_year_of_birth)
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the city use choose')

    # TO DO: Display earliest, most recent, and most common year of birth
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        view_data = input("Would you like to view the first 5 rows of individual trip data? Enter yes or no?\n").lower()
        while view_data not in ['yes', 'no', 'y', 'n']:
            view_data = input ("Choose between yes or no: ").lower()
        if view_data == 'yes' or view_data == 'y':
            start_loc = 0
            while (view_data == 'yes' or view_data == 'y'):
                end_loc = start_loc + 5
                print(df.iloc[start_loc:end_loc])
                view_data = input("Do you want to see the next 5 rows of individual trip data?: ").lower()
                while view_data not in ['yes', 'no', 'y', 'n']:
                    view_data = input ("Choose between yes or no: ").lower()
                if view_data == 'yes' or view_data == 'y':
                    start_loc += 5
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
