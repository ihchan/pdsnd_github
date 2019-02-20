import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!\n')

    # User input - select city
    city = None
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        if city in ('chicago', 'new york', 'washington'):
            print()
            break
        print('Input error. Please try again')

    # User input - filter by month and day if requested
    filter_type = None
    month = 'all'
    day = 'all'
    while True:
        filter_type = input('Would you like to filter the data? Enter month, day, both, or none.\n').lower()
        if filter_type in ('month', 'day', 'both', 'none'):
            print()
            break
        print('Input error. Please try again.\n')
    if filter_type in ('month', 'both'):
        while True:
            month = input('Which month - January, February, March, April, May, or June?\n').lower()
            if month in ('january', 'february', 'march', 'april', 'may', 'june'):
                print()
                break
            print('Input error. Please try again.')
    if filter_type in ('day', 'both'):
        while True:
            day = input('Which day of the week - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()
            if day in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                print()
                break
            print('Input error. Please try again.\n')

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Month - shown when month is not filtered
    if month == 'All':
        month_names = ['January', 'February', 'March', 'April', 'May', 'June']
        print('Most popular month:', month_names[df['month'].mode()[0]-1])

    # Day of week - shown when day of week is not filtered
    if day == 'All':
        print('Most popular day of week:', df['day_of_week'].mode()[0])

    # Start hour
    if df['Start Time'].dt.hour.mode()[0] <= 12:
        print('Most popular start hour: {} am'.format(df['Start Time'].dt.hour.mode()[0]))
    else:
        print('Most popular start hour: {} pm'.format(df['Start Time'].dt.hour.mode()[0] - 12))

    print("\nThis took %s seconds." % round((time.time() - start_time), 4))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Start station
    print('Most popular start station: {}\n'.format(df['Start Station'].mode()[0]))
    print(df['Start Station'].value_counts().head(5).to_string(),'\n')

    # End station
    print('Most popular end station: {}\n'.format(df['End Station'].mode()[0]))
    print(df['End Station'].value_counts().head(5).to_string(),'\n')

    # Trip
    route = df.groupby('Start Station')['End Station'].value_counts().sort_values(ascending=False).copy()
    print('Most popular trip: From {} to {}\n'.format(route.idxmax()[0], route.idxmax()[1]))
    print(route.head(5).to_string())

    print("\nThis took %s seconds." % round((time.time() - start_time), 4))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Convert 'Trip Duration' data type from float to timedelta
    total_time = pd.to_timedelta(df['Trip Duration'],unit='s')

    # Total travel time
    print('Total travel time\t{}d {}h {}m {}s'.format(
        total_time.sum().components[0],
        total_time.sum().components[1],
        total_time.sum().components[2],
        total_time.sum().components[3]
        )
    )

    # Mean travel time
    print('Average travel time\t{}m {}s'.format(
        total_time.mean().components[2],
        total_time.mean().components[3]
        )
    )

    print("\nThis took %s seconds." % round((time.time() - start_time), 4))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # User types
    print('User Types\n')
    print(df['User Type'].fillna('Not specified').value_counts().to_string(),'\n')

    # Gender - only for Chicago and New York
    print('Gender\n')
    if city == 'washington':
        print('Data not available for Washington.\n')
    else:
        print(df['Gender'].fillna('Not specified').value_counts().to_string(),'\n')

    # Year of birth - only for Chicago and New York
    print('Year of Birth\n')
    if city == 'washington':
        print('Data not available for Washington.\n')
    else:
        print('Earliest\t', df['Birth Year'].min().astype(int))
        print('Most common\t', df['Birth Year'].mode()[0].astype(int))
        print('Most recent\t', df['Birth Year'].max().astype(int))

    print("\nThis took %s seconds." % round((time.time() - start_time), 4))
    print('-'*40)


def view_data(df):
    """Displays raw data for user 5 rows at a time upon request."""

    row = 0
    view = None
    while True:
        if row == 0:
            view = input('Would you like to see the first 5 rows of raw data? Enter yes or no.\n')
        else:
            view = input('Would you like to see the next 5 rows of raw data? Enter yes or no.\n')
        if view.lower() == 'no':
            break
        elif view.lower() == 'yes':
            print(df[row:(row + 5)],'\n')
            row += 5
        else:
            print('Input error. Please try again.\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('\nGoodbye!\n')
            break


if __name__ == "__main__":
	main()
