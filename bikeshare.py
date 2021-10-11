import time
import pandas as pd
import numpy as np

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
    city = input('Which city would you like to see data for? Chicago , New York City or Washington: ')
    city = city.casefold()
    while city not in CITY_DATA:
        city = input('Invalid entry: Enter Chicago , New York City or Washington to proceed: ')
        city = city.casefold()

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Which month from January to June would you like? Enter "All" for the entire period: ')
    month = month.casefold()
    while month not in months:
        month = input('Invalid entry: Enter a month from January to June, or All to proceed: ')
        month = month.casefold()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Which day of the week, from Sunday to Saturday, would you like? Enter "All" for the all days: ')
    day = day.casefold()
    while day not in days:
        day = input('Invalid entry: Enter a day from Sunday to Saturday, or All to proceed: ')
        day = day.casefold()

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
    # Load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert start time to datetime then place month and day of week into separate columns 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    
    
    # Filter data by month and day of week into new dataframes
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    most_common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('Most Common Month:', months[most_common_month-1])

    # TO DO: display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    most_common_day = df['day_of_week'].mode()[0]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    print('Most Common Day:', days[most_common_day])


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', most_common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most Popular Start Station: ', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('Most Popular End Station: ', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print('\nMost Frequent Combination of Start and End Station Trips:\n\n',df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total Travel Time:', df['Trip Duration'].sum())


    # TO DO: display mean travel time
    print('Mean Travel Time:', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:    
        gender = df['Gender'].value_counts()
        print(gender,'\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of Birth:', int(df['Birth Year'].min()))
        print('Most Recent year of Birth:', int(df['Birth Year'].max()))
        print('Most Common year of Birth:', int(df['Birth Year'].mode()[0]))

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

        # Ask if user would like want to see the raw data
        response = ['yes','no']
        view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no?\n')
        
        while view_data.lower() not in response:
            view_data = input('Enter Yes or No:\n')
            view_data = view_data.lower()
        n = 0        
        while True :
            if view_data.lower() == 'yes':
        
                print(df.iloc[n : n + 5])
                n += 5
                view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no?\n')
                while view_data.lower() not in response:
                    view_data = input('Enter Yes or No:\n')
                    view_data = view_data.lower()
            else:
                break           
        
        
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
