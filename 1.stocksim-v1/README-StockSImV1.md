# python-projects
STOCK SIM V1

https://github.com/user-attachments/assets/d9bfdf86-ee15-433c-bbfb-f5ce33191b24

Stocks simulation starting with 10k with real stock data

1. get_stock_price function allows for it to be able to return the correct stock price rounded using yfinance. 
2. Created a portfolio dictionary to store user info
3. allowed user to input portfolio etc to perform an action
4. history function, allows for the user to view their portfolio buy/sell history, if empty returns nothing
5. portfolio function, shows the users portfolio with the shares and price included
6. buy function, asks the user which ticker to buy + amount, then this is checked against the yfinance to see if ticker is real, if yes, it checks to see if the user has enough money to purchase that specific amount of stock. Once its been bought information is added to the history, user money is updated, and their portfolio is also updated
7. sell function, asks the user which ticker they would like to sell and how many, the ticker is checked against the user's portfolio and if its in there the amount of it is also checked. If both go through, the user's money balance goes up accordingly, with their history and portfolio updated to match the new data.

NEXT STEP:
1. Learn pygame to have better UI
2. Learn some database method to store data

-28/08/2026
