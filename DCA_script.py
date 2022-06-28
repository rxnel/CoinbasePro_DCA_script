import cbpro
import time
import pprint as pp

""" paste your coinbase api info into into the variables below within
the quote marks. """
cbpro_apikey = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
cbpro_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
cbpro_passphrase = "your_passphrase"

auth_client = cbpro.AuthenticatedClient(
    cbpro_apikey,
    cbpro_secret,
    cbpro_passphrase,
)

# change daily buys as you like
def daily_buy():
    try_market_buy(product_id="BTC-USD", amt="10")
    try_market_buy(product_id="AVAX-USD", amt="10")
    try_market_buy(product_id="LINK-USD", amt="10")


# tries to create a market order for product_id. if there are insufficient funds, user will be prompted if they want to reload their balance and then try to purchase again if they do.
def try_market_buy(product_id, amt):
    response = auth_client.place_market_order(
        product_id=product_id, side="buy", funds=amt
    )

    message = response.get("message")
    print(message)

    if int(amt) < 10:
        return "Amount must be greater than 10"

    if message and message == "Insufficient funds":
        # attempt to add funds to account
        payment_ids = {}
        opt_num = 1
        print("----------- INSUFFICIENT FUNDS --------------")

        for funding_account in auth_client.get_payment_methods():
            payment_ids[opt_num] = (funding_account["id"], funding_account["name"])
            opt_num += 1

        print("Select payment method to reload balance")
        pp.pprint(payment_ids)
        payment_selected = int(input())
        (selected_id, selected_name) = payment_ids[payment_selected]
        reload_confirmation = input(
            "Are you sure you want to deposit ${} from {}?".format(amt, selected_name)
        )

        if reload_confirmation.upper() == "Y":
            print("Depositing ${} from {}".format(amt, selected_name))
            pp.pprint(
                auth_client.deposit(
                    amount=amt, currency="USD", payment_method_id=selected_id
                )
            )
            print("Waiting 10 seconds before placing market-order...")
            time.sleep(10)
            pp.pprint(
                auth_client.place_market_order(
                    product_id=product_id, side="buy", funds=amt
                )
            )

    else:
        pp.pprint(response)


daily_buy()
