import os
from flexfillsapi import initialize

# creds to test enviroment 100000_german, password abc123

username = '100000_german'
password = 'abc123'

instruments = ["ETH/BTC", "BTC/USD", "BTC/EUR"]
currencies = ["USD", "ETH"]
statues = ["COMLETED", "REJECTED", "PARTIALLY_FILLED", "FILLED", "EXPIRED"]

date_from = "2022-12-01T00:00:00"
date_to = "2022-12-14T22:30:00"

order_data = {
    "globalInstrumentCd": "BTC/USD",
    "clientOrderId": "0989876565",
    "direction": "SELL",
    "orderType": "LIMIT",
    "timeInForce": "GTC",
    # "price": "0.215",
    "amount": "1.0"
}

direct_order_data = {
    "globalInstrumentCd": "BTC/USD",
    "exchangeName": "BITFINEX",
    "requestType": "DIRECT",
    "clientOrderId": "unique_order_id_005",
    "orderType": "LIMIT",
    "direction": "SELL",
    "timeInForce": "GTC",
    "amount": "0.001",
    "clientId": "100000",
    "price": "58000"
}

cancel_order_data = {
    "class": "Order",
    "exchange": "HUOBI",
    "globalInstrumentCd": "BTC/USDT",
    "clientOrderId": "11726077295786",
    "direction": "SELL",
    "orderType": "LIMIT",
    "price": 58000.0,
    "amount": 0.01,
    "orderStatus": "SUBMITTED",
    "exchangeOrderId": "1150093430133608",
    "filledPrice": 0.0,
    "filledAmount": 0.0,
    "orderDateTime": "2024-09-11T17:54:55Z"
}


def get_order_books_stream(resp):
    print(resp)


def main():
    flexfills = initialize(username, password, is_test=True)
    # resp = flexfills.get_balance(["USD", "ETH"])

    # resp = flexfills.get_order_history(
    #     date_from, date_to, instruments, statues)
    # resp = flexfills.subscribe_order_books(["BTC/USDT"])
    # resp = flexfills.get_trade_positions()

    # resp = flexfills.create_order(direct_order_data)
    # resp = flexfills.get_open_orders_list(['BTC/USDT'])
    resp = flexfills.cancel_order(cancel_order_data)
    # resp = flexfills.get_balance(currencies)

    # resp = flexfills.get_private_trades(instruments, get_order_books_stream)

    print(resp)


if __name__ == "__main__":
    main()
