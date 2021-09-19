import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPEAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPEAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:
        print('Please enter the sales figures for today')
        print('Data should be in six figures seperated by a comma')
        print('Example: 10,20,30,40,50,60\n')
        data_str = input('Enter your data here: ')

        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print('Data input is valid')
            break


def validate_data(values):
    """
    Inside the try, convert all values to integers.
    Raise ValueError of the values can not be
    converted or if there arn't six values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 values required, you provided {len(values)}'
                )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again\n')
        return False

    return True


get_sales_data()
