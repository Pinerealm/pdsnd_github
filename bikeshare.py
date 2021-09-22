import time

import pandas as pd


CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}

months = ['January', 'February', 'March', 'April', 'May', 'June']


def month_filter():
    """Gets input for the month of choice.

       Returns: (str) month
    """
    try:
        month = input("\nChoose a month from January to June"
                      ":\n").strip().title()
        while not (month in months):
            month = input("\n**Did you make a valid choice?**"
                          "\nPlease choose only from January to"
                          " June:\n").strip().title()
    except (EOFError, KeyboardInterrupt):
        print('\nNo valid input or you interrupted the program'
              '\nExiting!!!')
        exit()
    return month


def day_filter():
    """Gets input for the weekday of choice.

       Returns (str) day
    """

    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday']
    try:
        day = input("\nWhich day of the week?:\n").strip().title()
        while not (day in weekdays):
            day = input("\n**Did you make a valid choice?**"
                        "\nPlease choose from Sunday to"
                        " Saturday:\n").strip().title()
    except (EOFError, KeyboardInterrupt):
        print('\nNo valid input or you interrupted the program:'
              '\nExiting!!!')
        exit()
    return day


def get_apply_filters():
    """
    Asks user to specify a city and whether to filter by month, day, both
    month and day or to apply no filter. The filter is then applied.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or
                      "All" to apply no month filter
        (str) day - name of the day of week to filter by, or
                      "All" to apply no day filter
    """
    print('='*60, '='*60, sep='\n')
    print("Hello! Let's explore some US BIKESHARE DATA!\n"
          "\nWould you like to view data for Chicago,"
          " New York City or Washington?\n")
    time.sleep(2)

    # Get user input for city (Chicago, New York City, Washington).
    try:
        city = input("Type to choose a city;"
                     " then hit 'Enter'.\n").strip().title()
        while city not in CITY_DATA.keys():
            city = input("\n**It seems you made a wrong input!**\n"
                         "Make sure you typed in the chosen city"
                         " correctly:\n").strip().title()
    except (EOFError, KeyboardInterrupt):
        print('\nNo valid input or you interrupted the program'
              '\nExiting!!!')
        exit()

    # Get user input for filter (month, day, both or none)
    try:
        filter = input('\nWould you like to filter the data by "month",'
                       ' ""day", "both" or not at all? \nType "none" if'
                       ' you do not want any filter.\n').strip().title()

        while filter not in ['Month', 'Day', 'Both', 'None']:
            filter = input('\nPls enter the appropriate filter: "month,"'
                           ' "day", "both" or "none".\n').strip().title()
    except (EOFError, KeyboardInterrupt):
        print('\nNo valid input or you interrupted the program'
              '\nExiting!!!')
        exit()

    # Apply filter
    if filter == 'Month':
        month = month_filter()
        day = 'All'
    elif filter == 'Day':
        day = day_filter()
        month = 'All'
    elif filter == 'Both':
        month = month_filter()
        day = day_filter()
    elif filter == 'None':
        month = 'All'
        day = 'All'

    print('='*100)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day
    if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by,
              or "All" to apply no month filter
        (str) day - name of the day of week to filter by,
              or "All" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by
             month and day
    """

    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city], index_col=0)
    df.rename_axis(city, inplace=True)

    # Convert the `Start Time` column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # Series.dt.day_name() from Pandas version 1.1.0

    # Filter by month if applicable
    if month != 'All':
        # Use the index of the months list to get the corresponding integer
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'All':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    print('\nHere\'s a sample of the requested data:\n')
    time.sleep(2)
    print(df.sample(5))
    time.sleep(6)
    print('='*70)

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    time.sleep(3)
    start_time = time.time()

    # Display the most common month
    if month not in months:
        month_commonest = df['month'].mode()[0]
        month_commonest = months[month_commonest-1]
        print('The commonest month of travel is: \n{}'.format(
                                                        month_commonest))
        time.sleep(2)
    else:
        print('The commonest month of travel is:',
              f'\nYou already chose {month}')
        time.sleep(2)

    # Display the most common day of week
    if day not in df['day_of_week'].unique():
        day_commonest = df['day_of_week'].mode()[0]
        print(f'\nThe commonest day of travel is: \n{day_commonest}')
        time.sleep(2)
    else:
        print('\nThe commonest day of travel is:',
              f'\nYou already chose {day}')

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour_commonest = df['hour'].mode()[0]
    print('\nThe most frequently travelled hour is:',
          f'\n0{hour_commonest}:00 hours' if hour_commonest < 10
          else f'\n{hour_commonest}:00 hours')
    time.sleep(2)

    print("\nThis took {:.4f} seconds.".format(time.time() - start_time - 2))
    print('='*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    time.sleep(3)
    start_time = time.time()

    # Display the most commonly used start station
    commonest_start_station = df['Start Station'].mode()[0]
    print(f'The most common start station is: \n{commonest_start_station}')
    time.sleep(2)

    # Display most commonly used end station
    commonest_end_station = df['End Station'].mode()[0]
    print(f'\nThe most common end station is: \n{commonest_end_station}')
    time.sleep(2)

    # Display most frequent combination of start and end station trip
    commonest_start_end = df.groupby(
        ['Start Station', 'End Station'])['Start Time'].count().sort_values(
                                                    ascending=False).index[0]
    # df[['Start Station', 'End Station']].value_counts().index[0]
    # Above method was introduced to DataFrames in pandas version 1.1.0
    print('\nThe most frequent combination of start and end station',
          'is from: \n{c[0]} \n==TO== \n{c[1]}'.format(c=commonest_start_end))
    time.sleep(3)

    print("\nThis took {:.4f} seconds.".format(time.time() - start_time))
    print('='*70)


def trip_duration_stats(df):
    """Displays statistics on the total and average and
       median trip duration.
    """

    print('\nCalculating Trip Duration...\n')
    time.sleep(3)
    start_time = time.time()

    # Display total travel time
    travel_time_tot = df['Trip Duration'].sum()
    hours = travel_time_tot // 3600
    minutes = (travel_time_tot - (hours*3600)) // 60
    seconds = travel_time_tot - (hours*3600) - (minutes*60)

    print('Total travel time is: \n{:,.0f} hours'
          ' {:,.0f} minute(s) {:,.0f} second(s)'.format(hours,
                                                    minutes, seconds))
    time.sleep(2)

    # Display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('\nAverage travel time is: \n'
          '{:,.1f} minute(s)'.format(avg_travel_time/60))
    time.sleep(2)

    # Display median travel time
    median_travel_time = df['Trip Duration'].median()
    print('\nMedian travel time is:\n'
          '{:,.1f} minute(s)'.format(median_travel_time/60))
    time.sleep(2)

    print("\nThis took {:.4f} seconds.".format(time.time() - start_time))
    print('='*70)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    time.sleep(3)
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts().to_dict()
    print('Frequency of traveller types:\nSubscriber(s): {:,}'
          '\nCustomer(s): {:,} \nDependent(s): {}'.format(
                                      user_count['Subscriber'],
                                      user_count['Customer'],
                                      user_count.get('Dependent', 0)))
    time.sleep(2)

    if city in ['Chicago', 'New York City']:
        # Display counts of gender
        gender_count = df['Gender'].value_counts().to_dict()
        print('\nGender frequency among travellers:\n'
              'Male(s): {:,} \nFemale(s): {:,}'.format(
                                              gender_count['Male'],
                                              gender_count['Female']))
        time.sleep(2)

        # Display earliest, most recent, and most common year of birth
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birthyear = int(df['Birth Year'].mode()[0])
        print('\nThe earliest, most recent, and most common year of birth',
              'respectively are: \n{}, {}, and {}'.format(
                    earliest_birth, most_recent_birth, most_common_birthyear))
        time.sleep(2)

        # Display median birth year
        median_birth_year = int(df['Birth Year'].median())
        print('\nThe median birth year is:\n'
                '{}'.format(median_birth_year))
        time.sleep(2)
    else:
        print("\nUnfortunately, gender and birth year information is",
              f"is not available for {city} city.")

    print("\nThis took {:.4f} seconds.".format(time.time() - start_time))
    print('='*70)


def generate_raw_data(df):
    """Generates chunks of 5 rows from the DataFrame"""

    for no in range(0, df.shape[0], 5):
        yield df[no:no+5]


def display_raw_data(df):
    """Display chunks of the raw data"""

    try:
        # Ask if user wants to display more raw data
        generate_0 = input('\nWould you like to see more raw data?'
                           '\nEnter "yes" or "no"\n').strip().title()

        # Display data if 'Yes' and apply subsequent conditions
        if generate_0 == 'Yes':
            for rows in generate_raw_data(df):
                print('='*50, rows, '=*50', sep='\n')
                generate = input('\n\nWould you like to see still more data?'
                                 '\nEnter "yes" or "no"\n').strip().title()
                if generate == 'Yes':
                    continue
                elif generate != 'Yes':
                    print('\nWe will stop providing you with more'
                          ' data for now!!!')
                    break
        else:
            print('\nThanks for your time')
    except (EOFError, KeyboardInterrupt):
        print('\nNo valid input or you interrupted the program'
              '\nExiting!!!')
        exit()


def main():
    while True:
        city, month, day = get_apply_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? '
                        'Enter yes or no.\n').strip()
        if restart.lower() != 'yes':
            print('\nBYE FOR NOW!!!')
            print('**'*30, '**'*30, sep='\n')
            break
        else:
            print('**'*30)


if __name__ == "__main__":
    main()
