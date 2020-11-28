import sys
import json
import asyncio
import fuckcaptcha
import traceback
from datetime import datetime
from pyppeteer.errors import PyppeteerError, PageError

from settings import email_options
from utils.asyncio import get_event_loop


class PageContext():
    def __init__(self, page, item):
        self.page = page
        self.item = item
        self.item_btn_title = item["item_title"]
        self.language = "en-US"
        # self.loop = get_event_loop()
        self.page_load_timeout = 30 # in seconds
        self.item_added = False

    async def goto(self, url):
        # jquery_js = await load_file(self.jquery_data)
        # await self.page.evaluateOnNewDocument("() => {\n%s}" % jquery_js)  # Inject JQuery
        await self.page.setExtraHTTPHeaders({'Accept-Language': self.language})  # Forced set Language
        await fuckcaptcha.bypass_detections(self.page)  # bypass reCAPTCHA detection in pyppeteer

        await self.page.goto(
            url,
            timeout=0,
            waitUntil=['load'],
        )

        await self.close_popup()

        # await self.page.waitForNavigation({'waitUntil': 'load'})

        # retry = 3  # Go to Page and Retry 3 times
        # while True:
        #     try:
        #         await self.page.goto(
        #             url, timeout=self.page_load_timeout * 1000,
        #             waitUntil=["networkidle0", "domcontentloaded"]
        #         )
        #         break
        #     except asyncio.TimeoutError as ex:
        #         traceback.print_exc(file=sys.stdout)
        #         print('Error timeout: ' + str(ex) + ' retry ' + str(retry))
        #         if retry > 0:
        #             retry -= 1
        #         else:
        #             raise TimeoutError("Page loading timed-out")
        #     except PyppeteerError as ex:
        #         traceback.print_exc(file=sys.stdout)
        #         print(f"Pyppeteer error: {ex}")
        #         if retry > 0:
        #             retry -= 1
        #         else:
        #             raise ex
        #     except Exception as ex:
        #         traceback.print_exc(file=sys.stdout)
        #         print('Error unexpected: ' + str(ex) + ' retry ' + str(retry))
        #         if retry > 0:
        #             retry -= 1
        #         else:
        #             raise PageError(f"Page raised an error: `{ex}`")


    async def add_item_to_cart(self):
        existing_btn_elem = await self.existing_element(
            elem_tag="button",
            elem_attr="textContent",
            elem_attr_values=["Add to Cart", "Add to cart"],
        )

        text_content = await self.get_element_text_content("h1", "textContent", "product-title")
        if text_content != self.item_btn_title:
            raise RuntimeError("Item titles aren't matching!")

        if existing_btn_elem:
            elem_title = f"Add {self.item_btn_title} to cart"
            elem_title = json.dumps(elem_title) # escapes quotes in item titles
            element = await self.page.querySelector(f'button[title={elem_title}]')
            
            await self.page.evaluate(f"(element) => element.click()", element)

            # await self.page.querySelector(f'button[title="{elem_title}"]').click()

            await asyncio.sleep(1)

            return True
        return False

    async def check_added_item_to_cart(self, added_text):
        js_func_added = f"window.find('{added_text}');"
        
        found_added_cart_text = await self.page.evaluate(js_func_added)

        # print(f"Added to Cart Text Found: {found_added_cart_text}")
        
        if found_added_cart_text:
            print(f"Successfully added to cart at: {datetime.now()}")
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
        await self.page.type('input[name="signEmail"]', login_email)
        await self.page.waitForNavigation({'waitUntil': 'load'})
        await asyncio.sleep(1)
        await self.page.click('button[id="signInSubmit"]')
        await asyncio.sleep(1)
        
        # email_code_elem = await self.existing_element(
        #     elem_tag="div",
        #     elem_attr="class",
        #     elem_attr_values=["form-v-code]"
        # )

        # recaptcha_elem = await self.existing_element(
        #     elem_tag="textarea",
        #     elem_attr="id",
        #     elem_attr_values=["g-recaptcha-response]"
        # )

        # if email_code_elem:
        #     print("Require email code to login...")
        #     await asyncio.sleep(240)
        #     await self.page.click('button[id="signInSubmit"]')
        
        # if recaptcha_elem:
        #     print("Solving recaptcha for login...")
        #     await self.solve()

        password_input = await self.existing_element(
            elem_tag="input",
            elem_attr="id",
            elem_attr_values=["labeled-input-password"],
        )
        print("checking password input element...")
        await asyncio.sleep(10)
        print(password_input)
        print("Entering login pass...")
        await asyncio.sleep(5)
        await self.page.type('input[name="password"]', login_pass)
        await self.page.waitForNavigation({'waitUntil': 'load'})
        await asyncio.sleep(1)
        await self.page.click('button[id="signInSubmit"]')

        print("Logging in...")
        await self.page.waitForNavigation()

    async def close_popup(self):
        popup = await self.existing_element("div", "id", ["popup"])
        popup_close = await self.existing_element("a", "id", ["popup-close"])
        if popup and popup_close:
            print("Popup closed!")
            await self.page.click('a[id="popup-close"]')

    async def refresh_page(self):
        await self.page.reload({
            "waitUntil": [
                "domcontentloaded",
            ]
        })
