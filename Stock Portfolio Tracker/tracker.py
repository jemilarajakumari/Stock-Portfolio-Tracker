from stock_price_tracker import StockPriceTracker
import requests
import json

class StockPortfolioTracker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.stocks = {}

    def add_stock(self, symbol):
        try:
            response = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}')
            response.raise_for_status()
            stock_info = response.json()['Global Quote']
            self.stocks[symbol] = {
                'price': stock_info['05. price'],
                'symbol': symbol
            }
            print(f"Added {symbol} to portfolio.")
        except requests.exceptions.RequestException as e:
            print(f"Error adding {symbol}: {e}")

    def remove_stock(self, symbol):
        if symbol in self.stocks:
            del self.stocks[symbol]
            print(f"Removed {symbol} from portfolio.")
        else:
            print(f"{symbol} not found in portfolio.")

    def track_performance(self):
        for symbol, stock in self.stocks.items():
            try:
                response = requests.get(f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}')
                response.raise_for_status()
                stock_info = response.json()['Global Quote']
                current_price = float(stock_info['05. price'])
                purchase_price = float(stock['price'])
                performance = (current_price - purchase_price) / purchase_price * 100
                print(f"{symbol}: {performance:.2f}%")
            except requests.exceptions.RequestException as e:
                print(f"Error tracking {symbol}: {e}")

def main():
    api_key = 'YOUR_API_KEY'
    tracker = StockPortfolioTracker(api_key)

    while True:
        print("1. Add stock")
        print("2. Remove stock")
        print("3. Track performance")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ")
            tracker.add_stock(symbol)
        elif choice == '2':
            symbol = input("Enter stock symbol: ")
            tracker.remove_stock(symbol)
        elif choice == '3':
            tracker.track_performance()
        elif choice == '4':
            break
        else:
            print("Invalid option.")


if __name__ == '__main__':
    main()

