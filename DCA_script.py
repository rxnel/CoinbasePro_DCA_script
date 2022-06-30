import cbpro
import time
import json
import pprint as pp

with open("config.json", "r") as f:
    config = json.load(f)

auth_client = cbpro.AuthenticatedClient(
    config["cbpro_api_key"],
    config["cbpro_secret"],
    config["cbpro_passphrase"],
)

# makes a deposit before making market buys
def daily_buy(pairs: dict):
    payment_ids = {}
    opt_num = 1
    total_amt = 0

    for size in pairs.values():
        total_amt += size

    for funding_account in auth_client.get_payment_methods():
        payment_ids[opt_num] = (funding_account["id"], funding_account["name"])
        opt_num += 1

    print("----------- RELOADING BALANCE BEFORE DAILY BUYS -----------")
    pp.pprint(payment_ids)

    payment_selected = int(input("Select payment method to reload balance"))

    (selected_id, selected_name) = payment_ids[payment_selected]

    reload_confirmation = input(
        "Are you sure you want to deposit ${} from {}?".format(total_amt, selected_name)
    )

    if reload_confirmation.upper() == "Y":
        print("Depositing ${} from {}".format(total_amt, selected_name))
        response = auth_client.deposit(
            amount=total_amt, currency="USD", payment_method_id=selected_id
        )
        pp.pprint(response)

    print("Sleeping for 5 seconds before making market orders")
    time.sleep(5)
    for pair, size in pairs.items():
        try_market_buy(product_id=pair, amt=size)


# tries to create a market order for product_id. if there are insufficient funds,
# the user will be prompted if they want to reload their balance. If they must
# select their preferred payment method and then their market-buy will be attempted
# again after depositing.
def try_market_buy(product_id: str, amt: int):
    response = auth_client.place_market_order(
        product_id=product_id, side="buy", funds=amt
    )

    message = response.get("message")

    if amt < 10:
        return "Amount must be greater than 10"

    if message and message == "Insufficient funds":
        # attempt to add funds to account
        payment_ids = {}
        opt_num = 1
        print("----------- INSUFFICIENT FUNDS --------------")

        for funding_account in auth_client.get_payment_methods():
            payment_ids[opt_num] = (funding_account["id"], funding_account["name"])
            opt_num += 1

        pp.pprint(payment_ids)
        payment_selected = int(input("Select payment method to reload balance"))
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


# change pairs to your liking
daily_buy(
    pairs={"AVAX-USD": 10, "BTC-USD": 10, "LINK-USD": 10},
)
