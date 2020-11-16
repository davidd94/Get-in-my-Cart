import requests
import time
import asyncio
from pyppeteer import launch

from custom_solver import MySolver


def recaptcha_solver(
    alert_type,
    item_id,
    item_qty,
    email_options=None,
    paypal_options=None,
    test=False
    ):
    keep_looping = True
    newegg_item_url = f"https://secure.newegg.com/Shopping/AddToCart.aspx?Submit=ADD&ItemList={item_id}|{item_qty}"
    newegg_url = f"https://secure.newegg.com/Shopping/AddToCart.aspx?Submit=ADD&ItemList={item_id}|{item_qty}"
    # newegg_item_url = f"https://www.newegg.com/v-color-16gb-288-pin-ddr4-sdram/p/0RN-00MB-00061?Item=9SIAMCMCHG2313&nspcid=345295&nspgid=345296"
    # newegg_url = "https://www.newegg.com/"

    # if alert_type == "sound":
    #     newegg_url = f"https://secure.newegg.com/Shopping/AddToCart.aspx?Submit=ADD&ItemList={item_id_test}|{qty}"
    # elif alert_type == "email":
    #     newegg_url = newegg_url = "https://www.newegg.com/"
    # elif alert_type == "paypal":
    #     newegg_url = newegg_url = "https://www.newegg.com/"
    
    # newegg_url_test = "https://www.newegg.com/evga-geforce-rtx-2080-ti-11g-p4-2487-rx/p/N82E16814487515?Description=rtx%202080&cm_re=rtx_2080-_-14-487-515-_-Product&quicklink=true"

    args = ["--timeout 5"]
    options = {
        "ignoreHTTPSErrors": True,
        "args": args,
        "target_url": newegg_url,
    }
    client = MySolver(
        pageurl=newegg_url,
        item_url=newegg_item_url,
        lang="en-US",
        options=options,
        alert_type=alert_type,
        email_options=email_options,
        paypal_options=paypal_options
    )

    while keep_looping:
        solution, cart_results = client.loop.run_until_complete(client.start())

        if solution and solution.get("status") == "detected":
            print("Recaptcha solved!")
            print(solution)

            if cart_results:
                keep_looping = False

        else:
            print("No solving required!")
            print(solution)

            if cart_results:
                keep_looping = False
        
        print("Attempting to add to cart again in 10 seconds...")
        time.sleep(10)

if __name__ == "__main__":
    email_options = {
        "email": "m0usiexdavid@hotmail.com",
        "password": "miceyman31@"
    }
    item_id = "N82E16814126457"
    item_id_test = "9SIAMCMCHG2313"
    qty = 1
    recaptcha_solver(
        alert_type="email",
        item_id=item_id_test,
        item_qty=qty,
        email_options=email_options,
    )
