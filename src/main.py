from utils.yfinance_api_interactor import YFinanceAPI
from utils.reddit_api_interactor import RedditAPI
from utils.finnhub_api_interactor import FinnhubAPI

from rich.console import Console
from rich.table import Table
from rich.color import Color
from rich.style import Style
from rich.live import Live
from rich.table import Table

from utils.secrets import REDDIT_API_TOKEN, REDDIT_API_CLIENT_ID, REDDIT_USERNAME, REDDIT_PASSWORD
from utils.secrets import FINNHUB_API_KEY as API_KEY

import random
import time


def render_default_terminal():
    pass


def render_yfinance_terminal():
    # Retrieving available stock parameters
    print("Welcome to the ifi_terminal's fundamental financial information terminal, here we offer a myriad of live information as indicated below! ")
    yfinance_api_sample = YFinanceAPI("APPL")
    fast_info_choices = [choice for choice in yfinance_api_sample.fast_info]

    valid_selection = False
    choices = ""
    count = 1
    
    for choice in fast_info_choices:
        choices += f"{count}. {choice}\n"
        count += 1

    # Validating user selections
    while not valid_selection:
        user_choice_selection = input(f"{choices}Please enter a comma-separated list of integers within the range [1, {count - 1}] to select filters: ").replace(" ", "")
        selection_arr = user_choice_selection.split(",")

        try:
            for selection in selection_arr:
                x = int(selection)
                assert x > 0 and x < count
            
            valid_selection = True
        except:
            print(f"Invalid selection! Enter a comma-separated list of integers within the valid range [1, {count - 1}] to select filters.")
            time.sleep(3)

    # Removing duplicate selections
    selection_arr = [*set(selection_arr)]

    # Maps columns to specified colors
    colorMapping = {
        "dayHigh": "green",
        "dayLow": "red",
        "exchange": "blue",
        "fiftyDayAverage": "purple"
    }

    # Stock validation - checking if valid stock and if already in cache
    stock_cache = []

    while True:
        stock = input("Enter stock (enter 'break' to stop) or enter 'default' to use our watchlist: ").upper()
        if stock == "BREAK":
            break
        elif stock == "DEFAULT":
            stock = "AAPL,MSFT,GOOG,AMZN,TSLA,JPM,NVDA,META,UNH,DIS"
            stock_cache = stock.split(",")
            break
        try:
            yfinance_api = YFinanceAPI(stock)
            yfinance_api.get_high()

            try: 
                if stock in stock_cache:
                    raise ValueError()
                stock_cache.append(stock)
            except:
                print(f"{stock} has already been added!")

        except Exception as e:
            print("Invalid stock!")

    # Generates new table for live stock updates
    def generate_table() -> Table:
        column_cache = []

        table = Table(title="Stock Data")
        table.add_column("STOCK", style="bold cyan")

        for selection in selection_arr:
            column = fast_info_choices[int(selection) - 1]
            
            style = Style(color=Color.from_rgb(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
            style = colorMapping.get(column, style)

            table.add_column(column.upper(), style=style, justify="center")  
            column_cache.append(column) 

        for stock in stock_cache:
            yfinance_api = YFinanceAPI(stock)
            row_values = [stock] + [str(yfinance_api.fast_info[column]) for column in column_cache]
            table.add_row(*row_values)

        return table
    
    # Asking user for time constraints
    selected_time = False
    while not selected_time:
        try:
            frequency = int(input("Please enter how often (seconds) to update table: "))
            duration = int(input("Please enter the lifespan (seconds) of the table: "))
            assert frequency > 0 and duration > 0

            selected_time = True
        except:
            print("Please enter positive integers only.")
    
    # Updates table with live data
    with Live(generate_table(), refresh_per_second=4) as live:
        for _ in range(duration // frequency):
            time.sleep(frequency)
            live.update(generate_table())


def render_reddit_terminal():
    # User login
    # REDDIT_API_TOKEN = input("Enter your Reddit API Token: ")
    # REDDIT_API_CLIENT_ID = input("Enter your Reddit API Client ID: ")
    # REDDIT_USERNAME = input("Enter your Reddit username: ")
    # REDDIT_PASSWORD = input("Enter your Reddit password: ")
    reddit_api = RedditAPI(REDDIT_API_TOKEN, REDDIT_API_CLIENT_ID, REDDIT_USERNAME, REDDIT_PASSWORD)

    # Asking user for input
    subreddit = input("Enter a subreddit: ")
    post_limit = int(input("Enter the hot post limit: "))
    post_arr = reddit_api.get_hot_posts(subreddit, post_limit)

    comment_limit = int(input("Enter the comment limit: "))

    table = Table(title="Reddit Testing")
    table.add_column("Post")
    table.add_column("Comments")

    # Generating table
    for post in post_arr:
        comment_arr = reddit_api.get_post_top_comments(post, comment_limit)
        comment_str = ""

        for comment in comment_arr:
            comment_str += comment.body + "\n"

        style = Style(color=Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        table.add_row(post.title, comment_str, style=style)
    
    console = Console()
    console.print(table)


def render_finnhub_terminal():
    print("Welcome to the ifi_terminal's decision helper where we currently offer 4 major services: ")
    print("1. Latest news about the financial market")
    print("2. Crypto Currency Data")
    print("3. Technical Indicators for thsoe who would like to perform technical analysis")
    print("4. Analytical bots: currently we only have one option, but we are woking on more!")
    choice = input("Please enter the number of the service you would like to use: ")

    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        print("Sample bot 0: Is the low of the day higher than the closing price of the previous day?")
        stock_cache = []

        api_obj = FinnhubAPI(API_KEY)

        while True:
            stock = input("Enter stock (enter 'break' to stop) or enter 'default' to use our watchlist: , invalid entries will be ignored").upper()
            if stock == "BREAK":
                break
            elif stock == "DEFAULT":
                stock = "AAPL,MSFT,GOOG,AMZN,TSLA,JPM,NVDA,META,UNH,DIS"
                stock_cache = stock.split(",")
                break
            try:
                api_obj.get_quote(stock)


                try: 
                    if stock in stock_cache:
                        raise ValueError()
                    stock_cache.append(stock)
                except:
                    print(f"{stock} has already been added!")

            except Exception as e:
                print("Invalid stock!")

        table = Table(title="Decision Helper")
        table.add_column("Stock")
        table.add_column("Trend Details")

        for stock in stock_cache:
            status = api_obj.get_quote(stock)
            
            if status["l"] > status["pc"]:
                table.add_row(stock, "Low of the day is higher than the closing price of the previous day", style="green")
            else:
                table.add_row(stock, "Low of the day is lower than the closing price of the previous day", style="red")

        console = Console()
        console.print(table)
            
    else:
        print("Invalid choice! Exiting decision helper!")


if __name__ == "__main__":
    while True:
        try:
            selection = input("Select \n [D] for default ifi_terminal display \n [Y] for <yfinance> (traditional financial information) \n [R] for reddit data \n [F] for <yfinance> modern indicators (crypto/ news/ technical tickers) and a sample trend bot: press anything else to exit application ").upper()

            if selection == "D":
                render_default_terminal()
            
            elif selection == "Y":
                render_yfinance_terminal()

            elif selection == "R":
                render_reddit_terminal()

            elif selection == "F":
                render_finnhub_terminal()

            else:
                print("Exiting Program!")
                break
        except:
            print("ERROR!")
            print("Some issue has occured, please try again!")






        
