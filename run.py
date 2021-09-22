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
    return sales_data


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


def calculate_surplus_data(sales_row):
    """
    Surplus sales based on items sold on market day and items in stock

    Positive number means stock left over
    Negative number means stock ran out and new items had to be made
    """

    print('Calutlating surplus data\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data


def update_worksheet(data, worksheet):
    """
    Update the worksheet data in the spreadsheet based on
    data and worksheet provided
    """
    print(f'Updating {worksheet} worksheet\n')
    worksheet_update = SHEET.worksheet(worksheet)
    worksheet_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully\n')


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet,
    collecting only the last 5 entries and returns a list of lists
    """
    sales = SHEET.worksheet('sales')

    columns = []
    for i in range(1, 7):
        column = sales.col_values(i)
        columns.append(column[-5:])

    return columns


def calculate_stock_data(data):
    """
    Calculate the recommended stock for the next market
    """
    print('Calculating stock data...\n')
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        avarege = sum(int_column) / len(int_column)
        stock_num = avarege * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data


def main():
    """
    Runs the main functions and statements of the program
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')


main()
