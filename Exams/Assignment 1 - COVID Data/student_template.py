import sys

"""
Create a program which will provide answers to the questions posed in the assignment description.
We've provided a function which will parse the NYT covid database file (named "us-counties.csv"); 
however, its correct implementation will be up to you. DO NOT MODIFY THIS FUNCTION.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.
"""


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date,county, state, fips, cases, deaths) information

    ____________________ DO NOT MODIFY THIS FUNCTION ___________________
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date,county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, fips, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

### YOUR CODE HERE ###


def get_county_data(data, county_name, state_name):
    """
    Pull out only the records for one county
    :param data: List of tuples from parse_nyt_data()
    :param county_name: Name of the county as it appears in the data
    :param state_name: Name of the state as it appears in the data
    :return: List of tuples for just that county, in the same date order as the file
    """
    county_data = []

    # each entry is (date, county, state, fips, cases, deaths)
    for entry in data:

        # need to check the state too since other states have a Rockingham county
        if entry[1] == county_name and entry[2] == state_name:
            county_data.append(entry)

    return county_data


def find_first_case(county_data):
    """
    Find the first date where the county had a positive case
    :param county_data: List of tuples for one county
    :return: Date of the first positive case
    """
    for entry in county_data:

        # the first record with more than 0 cases (index 4) is the first positive case
        if entry[4] > 0:
            return entry[0]

    # no positive cases were found
    return None


def get_new_cases(county_data):
    """
    Calculate the number of new cases for each day. The data only has the total
    (cumulative) cases, so new cases = today's total - yesterday's total
    :param county_data: List of tuples for one county
    :return: List of new cases for each day (same order as county_data)
    """
    new_cases = []

    # use 0 as the previous total for the first record

    for entry in county_data:
        cases = entry[4]

        # find the change in cumulative cases to get the number of new cases
        new_cases.append(cases - previous_cases)

        # save today's total to use for the next day
        previous_cases = cases

    return new_cases


def find_largest_day(county_data, new_cases):
    """
    Find the day with the greatest number of new cases
    :param county_data: List of tuples for one county
    :param new_cases: List of new cases for each day
    :return: (largest number of new cases, date it happened)
    """
    # start with the first day and then compare against the rest
    largest_cases = new_cases[0]
    largest_date = county_data[0][0]

    for i in range(1, len(new_cases)):
        if new_cases[i] > largest_cases:
            largest_cases = new_cases[i]
            largest_date = county_data[i][0]

    return largest_cases, largest_date


def find_worst_week(county_data, new_cases):
    """
    Find the seven day period with the most new cases
    :param county_data: List of tuples for one county
    :param new_cases: List of new cases for each day
    :return: (total new cases in that week, start date, end date)
    """
    largest_total = 0
    start_date = ''
    end_date = ''

    # check every group of 7 days in a row. The last group starts 7 days
    # from the end of the list so we don't go past the end
    for start in range(0, len(new_cases) - 6):

        # add up the new cases for these 7 days
        seven_day_total = 0
        for i in range(start, start + 7):
            seven_day_total += new_cases[i]

        # if this week is worse than the worst so far, save it
        if seven_day_total > largest_total:
            largest_total = seven_day_total
            start_date = county_data[start][0]
            end_date = county_data[start + 6][0]

    return largest_total, start_date, end_date


if __name__ == "__main__":

    # load the NYT data (path is relative to this file's folder)
    data = parse_nyt_data("../../data/covid/us-counties.csv")

    # Step 1: separate out the Harrisonburg and Rockingham records
    harrisonburg_data = get_county_data(data, "Harrisonburg city", "Virginia")
    rockingham_data = get_county_data(data, "Rockingham", "Virginia")

    # Step 2: calculate the new cases for each day in each location
    harrisonburg_new_cases = get_new_cases(harrisonburg_data)
    rockingham_new_cases = get_new_cases(rockingham_data)

    # Question 1: first positive case
    print("Question 1")
    print("Harrisonburg first positive case:", find_first_case(harrisonburg_data))
    print("Rockingham County first positive case:", find_first_case(rockingham_data))
    print()

    # Question 2: day with the most new cases
    (harrisonburg_largest, harrisonburg_date) = find_largest_day(harrisonburg_data, harrisonburg_new_cases)
    (rockingham_largest, rockingham_date) = find_largest_day(rockingham_data, rockingham_new_cases)

    print("Question 2")
    print("Harrisonburg greatest number of new cases:", harrisonburg_largest, "on", harrisonburg_date)
    print("Rockingham County greatest number of new cases:", rockingham_largest, "on", rockingham_date)
    print()

    # Question 3: worst seven day period
    (harrisonburg_total, harrisonburg_start, harrisonburg_end) = find_worst_week(harrisonburg_data, harrisonburg_new_cases)
    (rockingham_total, rockingham_start, rockingham_end) = find_worst_week(rockingham_data, rockingham_new_cases)

    print("Question 3")
    print("Harrisonburg worst seven-day period:", harrisonburg_start, "through", harrisonburg_end)
    print("Total new cases during period:", harrisonburg_total)
    print()
    print("Rockingham County worst seven-day period:", rockingham_start, "through", rockingham_end)
    print("Total new cases during period:", rockingham_total)