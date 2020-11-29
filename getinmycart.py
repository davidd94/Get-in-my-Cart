import requests
import time
import asyncio
import threading
import fuckcaptcha
from pyppeteer import launch
from colorama import init
from termcolor import colored

from custom_solver import MySolver
from utils.alerts import play_quiet_alert
from utils.email import email
from utils.scrape import PageContext
from utils.random import random_int
from settings import (
    headless,
    options,
    email_options,
    paypal_options,
    agent,
    item_data,
    alert_type,
)

init() # inits terminal color text


async def scrape_url(item):
    main_url = item["url"]
    item_url = item["item_url"]
    cart_url = item["cart_url"]
    item_btn_title = item["item_title"]
    item_name = item["name"]
    max_retry = 3

    browser = await launch(
        options=options,
        headless=headless,
    )

    # Set user-agent to all pages
    pages = await browser.pages()
    for page in pages:
        await page.setUserAgent(agent)
    page = pages[0]  # Set first page
    
    page_context = PageContext(page=page, item=item)
    await page_context.init_settings()

    await page_context.goto(main_url)
    await asyncio.sleep(1) # add delay variation
    await page_context.goto(item_url)

    await page_context.close_popup()

    while not page_context.item_added and max_retry >= 0:
        timestamp = round(time.time())
        add_results = False

        try:
            add_results = await page_context.add_item_to_cart()
        except Exception as e:
            print(e)
            await play_quiet_alert()
        
        if add_results:
            await page.screenshot({"path": f"./images/{item_name}-in-stock-{timestamp}.png"})
            # go to cart for last verification
            await page.goto(url=cart_url)
            results = await page_context.check_added_item_to_cart(
                added_text=item_btn_title
            )
            
            if results:
                await page.screenshot({"path": f"./images/added-{item_name}-to-cart-{timestamp}.png"})
                print(colored(f"{item_name}: ADDED TO CART", 'green'))
                page_context.item_added = True
                if alert_type == "email":
                    await page_context.login()
                email(item_name=item_name, item_url=item_url)
                await browser.close()
                return True
            else:
                max_retry -= 1
                print(colored(f"ERROR: {item_name} has been added but cannot be found in cart!", 'yellow'))
        else:
            print(colored(f"{item_name}: OUT OF STOCK", 'red'))
            await page_context.refresh_page()
            await asyncio.sleep(5)
    
    await browser.close()
    return False

async def run():
    tasks = [asyncio.create_task(scrape_url(item)) for item in item_data]
    await asyncio.gather(*tasks)


# def recaptcha_solver(
#     alert_type,
#     item_data,
#     email_options=None,
#     paypal_options=None,
#     test=False
#     ):
#     client = MySolver(
#         pageurl="https://www.newegg.com/",
#         lang="en-US",
#         options=options,
#         alert_type=alert_type,
#         item_data=item_data,
#         email_options=email_options,
#         paypal_options=paypal_options,
#     )

#     solution = client.loop.run_until_complete(client.start())
        
#     print(solution)
#     if solution:
#         print("Recaptcha solved! Executed alerts.")
#     print("Exiting script...")

if __name__ == "__main__":
    # recaptcha_solver(
    #     alert_type="sound",
    #     item_data=item_data,
    #     email_options=email_options,
    # )

    # loop = asyncio.get_event_loop()
    # future = asyncio.ensure_future(run())

    # loop.run_until_complete(future)

    loop = asyncio.get_event_loop()
    loop.create_task(run())
    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        print("Shutting down app...")
    finally:
        loop.stop()
        loop.run_until_complete(loop.shutdown_asyncgens())
