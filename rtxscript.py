import requests
import time
import asyncio
import threading
import fuckcaptcha
from pyppeteer import launch
from colorama import init
from termcolor import colored

from custom_solver import MySolver
from utils.alerts import play_quiet_alert, execute_alert
from utils.scrape import PageContext
from utils.random import random_int
from settings import (
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

    browser = await launch(headless=False, args=options["args"])

    # Set user-agent to all pages
    pages = await browser.pages()
    for page in pages:
        await page.setUserAgent(agent)
    page = pages[0]  # Set first page
    
    page_context = PageContext(page=page, item=item)

    await page_context.goto(main_url)
    await asyncio.sleep(1) # add delay variation
    await page_context.goto(item_url)

    while not page_context.item_added and max_retry >= 0:
        add_results = False

        try:
            add_results = await page_context.add_item_to_cart()
        except Exception as e:
            print(e)
            await play_quiet_alert()
        
        if add_results:
            # go to cart for last verification
            await page.goto(url=cart_url)
            results = await page_context.check_added_item_to_cart(
                added_text=item_btn_title
            )
            
            if results:
                print(colored(f"{item_name}: ADDED TO CART", 'green'))
                page_context.item_added = True
                if alert_type == "email":
                    await page_context.login()
                await execute_alert()
                await browser.close()
                return True
            else:
                max_retry -= 1
                print(colored(f"ERROR: {item_name} has been added but cannot be found in cart!", 'red'))
        else:
            print(colored(f"{item_name}: OUT OF STOCK", 'red'))
            await page_context.refresh_page()
            print("Sleeping for 5 seconds...")
            await asyncio.sleep(5)
    
    await browser.close()
    return False

async def run():
    # while len(item_data) > 0:
    #     tasks = []
    #     for item in item_data:
    #         task = asyncio.create_task(scrape_url(item))
    #         tasks.append(task)
        
    #     response = await asyncio.gather(*tasks)
    #     while True in response: # remove completed task(s)
    #         idx = response.index(True)
    #         response.pop(idx)
    #         item_data.pop(idx)
    
    tasks = []
    for item in item_data:
        task = asyncio.create_task(scrape_url(item))
        tasks.append(task)
    
    response = await asyncio.gather(*tasks)
    print(response)


def recaptcha_solver(
    alert_type,
    item_data,
    email_options=None,
    paypal_options=None,
    test=False
    ):
    client = MySolver(
        pageurl="https://www.newegg.com/",
        lang="en-US",
        options=options,
        alert_type=alert_type,
        item_data=item_data,
        email_options=email_options,
        paypal_options=paypal_options,
    )

    solution = client.loop.run_until_complete(client.start())
        
    print(solution)
    if solution:
        print("Recaptcha solved! Executed alerts.")
    print("Exiting script...")

if __name__ == "__main__":
    # recaptcha_solver(
    #     alert_type="sound",
    #     item_data=item_data,
    #     email_options=email_options,
    # )

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run())

    loop.run_until_complete(future)

    # pending = asyncio.all_tasks()
    # loop.run_until_complete(asyncio.gather(*pending))
