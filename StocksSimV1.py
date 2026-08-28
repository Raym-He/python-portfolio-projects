import yfinance as yf


def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.fast_info['lastPrice']
        return round(price, 2)
    except Exception:
        return None


portfolio = {
    'money': 10000.0,
    'holding_shares': {},
    'history': []
}

market_prices = {
    "AAPL": 185.50,
    "TSLA": 240.00,
    "MSFT": 410.25,
    "NVDA": 125.00,
    "BARC": 2.20
}


while True:
    user_action = input("\nEnter command (portfolio, buy, sell, ,history, exit): ").strip().lower()
#exit
    if user_action == 'exit':
        print("You have chosen to exit the program.")
        break

#history
    if user_action == 'history':
        if portfolio['history'] == []:
            print("You haven't made a transaction yet")
            continue
        else:
            print("\n--- Transaction History (New->Old) ---")
            for transaction in portfolio['history']:
                print(transaction)
                continue

#portfolio
    elif user_action == 'portfolio':
        print(f"Your current balance is: £{portfolio['money']}")
        if not portfolio["holding_shares"]:
            print("You do not currently hold any shares.")
        else:
            for ticker, shares in portfolio['holding_shares'].items():
                print(f"You hold {shares} shares of {ticker}.")

#buy
    elif user_action == 'buy':
        ticker = input('Enter which ticker you would like to buy:').strip().upper()
        try:
            number_of_shares = int(input('Enter the number of shares which you would like to buy'))
        except ValueError:
            print(f"You have entered a wrong answer this needs to be a positive interger (e.g 1,2,3)")
            continue

        confirmation = input(f"You want to buy {number_of_shares} shares of {ticker}. Confirm Yes or No.").strip().lower()

        if confirmation == 'yes':
            price = get_stock_price(ticker)
            if price == 'None':
                print(f"The ticker {ticker} you entered is not in the market")
                continue

            else:
                price_of_shares = price * number_of_shares 
                if portfolio['money'] >= price_of_shares:
                    portfolio['money'] -= price_of_shares
                    portfolio['history'].append({'Bought': ticker, 'Amount': price_of_shares}) 
                    if ticker in portfolio['holding_shares']:
                        portfolio['holding_shares'][ticker] += number_of_shares
                    else:
                        portfolio['holding_shares'][ticker] = number_of_shares
                    print(f"Your money is now {portfolio['money']} and you have just bought {number_of_shares} of {ticker}.")
                else:
                    print('You dont have enough money')
                    continue
        else:
            print('You have entered no or an incorrect answer')
            continue

#sell
    elif user_action == 'sell':
        sold_ticker = input(f"Which ticker would you like to sell").strip().upper()
        try:
            sold_ticker_amount = int(input(f"How many tickers would you like to sell"))
        except ValueError:
            print(f"You have entered a wrong answer. It needs to be a positive interger (e.g 1,2,3")
            continue

        if sold_ticker not in portfolio['holding_shares']:
            print(f"You dont own any {sold_ticker} stocks")
            continue

        else:
            if portfolio['holding_shares'][sold_ticker] < sold_ticker_amount:
                print(f"You dont have enough of this stock: {sold_ticker}")
                continue
            else:
                portfolio['money'] += (price * round(sold_ticker_amount,2))
                portfolio['holding_shares'][sold_ticker] -= sold_ticker_amount
                portfolio['history'].append({'Sold': ticker, 'Amount': price_of_shares})

                if portfolio['holding_shares'][sold_ticker] == 0:
                    del portfolio['holding_shares'][sold_ticker]

            print(f"You have gained {market_prices[sold_ticker] * sold_ticker_amount} and have {portfolio['money']} on total now")
            continue

