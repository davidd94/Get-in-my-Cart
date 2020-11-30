import sys
import json
import asyncio
import fuckcaptcha
import traceback
from datetime import datetime
from pyppeteer.errors import PyppeteerError, PageError

from utils.logging import logger
from utils.alerts import play_quiet_alert
from settings import email_options


class PageContext():
    def __init__(self, page, item):
        self.page = page
        self.item = item
        self.item_btn_title = item["item_title"]
        self.language = "en-US"
        self.page_load_timeout = 30 # in seconds
        self.item_added = False

    async def init_settings(self):
        self.page.setDefaultNavigationTimeout(0)

    async def goto(self, url):
        # jquery_js = await load_file(self.jquery_data)
        # await self.page.evaluateOnNewDocument("() => {\n%s}" % jquery_js)  # Inject JQuery
        await self.page.setExtraHTTPHeaders({'Accept-Language': self.language})  # Forced set Language
        await fuckcaptcha.bypass_detections(self.page)  # bypass reCAPTCHA detection in pyppeteer

        await self.page.goto(
            url,
            waitUntil=[
                "load",
                # "networkidle0",
                # "networkidle2",
            ],
        )

    async def add_item_to_cart(self):
        existing_btn_elem = await self.existing_element(
            elem_tag="button",
            elem_attr="textContent",
            elem_attr_values=["Add to Cart", "Add to cart"],
        )

        text_content = await self.get_element_text_content("h1", "textContent", "product-title")
        if text_content != self.item_btn_title:
            logger.exception(f"Item set title ({self.item['name']}) aren't matching with website title ({text_content})!")
            await play_quiet_alert()
            return False

        if existing_btn_elem:
            elem_title = f"Add {self.item_btn_title} to cart"
            elem_title = json.dumps(elem_title) # escapes quotes in item titles
            element = await self.page.querySelector(f'button[title={elem_title}]')

            if element:
                await self.page.evaluate(f"(element) => element.click()", element)
                logger.info(f"Attempting to add item ({self.item["name"]}) to cart")
                await asyncio.sleep(1)
                return True
        return False

    async def check_added_item_to_cart(self, added_text):
        js_func_added = f"window.find('{added_text}');"
        found_added_cart_text = await self.page.evaluate(js_func_added)
        
        if found_added_cart_text:
            logger.info(f"Successfully added item ({self.item["name"]}) to cart")
            return True

        return False

    async def existing_element(self, elem_tag, elem_attr, elem_attr_values):
        elements = await self.page.querySelectorAll(elem_tag)
        for element in elements:
            eval_element = await self.page.evaluate(f"(element) => element.{elem_attr}", element)
            eval_element = eval_element.strip()
            if eval_element in elem_attr_values:
                return True

        return False

    async def get_element_text_content(self, elem_tag, elem_attr, elem_attr_value):
        elements = await self.page.querySelectorAll(elem_tag)
        for element in elements:
            eval_element = await self.page.evaluate(f"(element) => element.{elem_attr}", element)
            eval_element = eval_element.strip()
            if eval_element == self.item_btn_title:
                return eval_element

        return False
    
    async def login(self):
        await self.goto(self.item["login_url"])

        # login
        login_email = email_options.get("email")
        login_pass = email_options.get("password")

        print("Entering login email...")
        logger.info(f"Entering login email... for ({self.item["name"]})")
        await self.page.type('input[name="signEmail"]', login_email)
        await asyncio.sleep(2)
        await self.page.click('button[id="signInSubmit"]')
        await asyncio.sleep(2)

        await self.existing_element(
            elem_tag="input",
            elem_attr="id",
            elem_attr_values=["labeled-input-password"],
        )
        print("Entering login pass...")
        logger.info(f"Entering login pass... for ({self.item["name"]})")
        await self.page.type('input[name="password"]', login_pass)
        await asyncio.sleep(2)
        await self.page.click('button[id="signInSubmit"]')
        print("Logging in...")
        logger.info(f"Logging in... for ({self.item["name"]})")
        await self.page.waitForNavigation()
        print("Successfully logged in!")
        logger.info(f"Successfully logged in!!! ({self.item["name"]})")
        await play_quiet_alert()

    async def close_popup(self):
        popup = await self.existing_element("div", "id", ["popup"])
        popup_close = await self.existing_element("a", "id", ["popup-close"])
        if popup and popup_close:
            print("Popup closed!")
            await self.page.click('a[id="popup-close"]')

    async def refresh_page(self):
        # await self.page.goto(self.item["item_url"], {
        #     "waitUntil": [
        #         # "domcontentloaded",
        #         # "networkidle0",
        #         # "networkidle2",
        #         "load",
        #     ]
        # })

        # await self.page.waitForNavigation({
        #     "waitUntil": [
        #         # "domcontentloaded",
        #         # "networkidle0",
        #         # "networkidle2",
        #         "load",
        #     ]
        # })

        await asyncio.wait(
            [
                self.page.waitForNavigation(waitUntil=["load"]),
                self.page.reload(waitUtil=["load"]),
            ]
        )
