import time
import asyncio
from datetime import datetime

from goodbyecaptcha.solver import Solver
from pydub import AudioSegment
from pydub.playback import play
from colorama import init
from termcolor import colored

timestamp = round(time.time())
init()


class MySolver(Solver):
    # async def on_goto(self):
    #     # Set Cookies and other stuff
    #     # await self.page.setCookie({
    #     #     'name': 'cookie1',
    #     #     'value': 'value1',
    #     #     'domain': '.google.com'
    #     # })
    #     # self.log('Cookies ready!')
    #     pass

    def __init__(self,
        pageurl,
        lang,
        options,
        alert_type,
        item_url,
        cart_url,
        item_btn_title,
        item_name,
        success_sleep_timer=3600,
        email_options=None,
        paypal_options=None,
    ):
        """
        Email options: {
            "email": <INSERT LOGIN EMAIL>,
            "password": <INSERT LOGIN PASS>
        }
        
        Paypal options: {
            "email": <INSERT PAYPAL LOGIN>,
            "password": <INSERT PAYPAL PASS>,
            "oauth": ?????
        }
        """
        self.item_url = item_url
        self.cart_url = cart_url
        self.item_btn_title = item_btn_title
        self.item_name = item_name

        self.alert_type = alert_type # sound/email/paypal
        self.success_sleep_timer = success_sleep_timer
        self.email_options = email_options
        self.paypal_options = paypal_options

        self.item_added = False

        super(MySolver, self).__init__(
            pageurl=pageurl,
            lang=lang,
            options=options
        )

    async def on_start(self):
        # Set or Change data
        # while not self.item_added:
        #     await asyncio.sleep(5) # sleep here is required to bypass newegg auto bot detection

        add_results = False

        await self.solve()
        await self.navigate_to_item()
        
        try:
            add_results = await self.add_item_to_cart()
        except Exception as e:
            print(e)
            await self.execute_minor_alert()
        
        if add_results:
            # go to cart for last verification
            await self.page.goto(url=self.cart_url)
            results = await self.check_added_item_to_cart(
                added_text=self.item_btn_title
            )
            if results:
                self.item_added = True
                # break
        
        print(colored(f"{self.item_name}: OUT OF STOCK", 'red'))

            # await self.refresh_page()

        # await self.page.screenshot({"path": f"./images/on_start_ss-{timestamp}.png"})
    
    async def on_finish(self):
        if self.item_added:
            print(colored(f"{self.item_name}: ADDED TO CART", 'green'))
            await self.execute_alert()

    async def navigate_to_item(self):
        if self.page.url != self.item_url:
            print(f"Redirect from {self.page.url} to {self.item_url}")
            await self.page.goto(url=self.item_url)
            # await self.page.waitForNavigation({'waitUntil': 'domcontentload'})
            await self.page.screenshot({"path": f"./images/on_navigate_ss-{timestamp}.png"})

    async def refresh_page(self):
        await self.page.reload({
            "waitUntil": [
                "domcontentloaded",
            ]
        })

    async def add_item_to_cart(self):
        existing_btn_elem = await self.existing_element(
            elem_tag="button",
            elem_attr="textContent",
            elem_attr_values=["Add to Cart", "Add to cart"],
        )

        text_content = await self.get_element_text_content("h1", "textContent", "product-title")
        if text_content != self.item_btn_title:
            await self.execute_minor_alert()
            raise RuntimeError("Item titles aren't matching!")

        if existing_btn_elem:
            elem_title = f"Add {self.item_btn_title} to cart"
            # await self.page.click(f'button[title="{elem_title}"]')

            element = await self.page.querySelector(f'button[title="{elem_title}"]')
            await self.page.evaluate(f"(element) => element.click()", element)

            # await self.page.querySelector(f'button[title="{elem_title}"]').click()

            await asyncio.sleep(1)

            return True
        return False

    async def check_added_item_to_cart(
        self,
        added_text,
        ):
        js_func_added = f"window.find('{added_text}');"
        
        found_added_cart_text = await self.page.evaluate(js_func_added)

        # print(f"Added to Cart Text Found: {found_added_cart_text}")
        
        if found_added_cart_text:
            print(f"Successfully added to cart at: {datetime.now()}")
            return True

        return False

    async def execute_alert(self):
        if self.alert_type == "sound":
            print("Alerting user....")
            audio_clip = AudioSegment.from_mp3("audio/annoying_alarm.mp3")
            play(audio_clip)
            print(f"Sleeping for {self.success_sleep_timer}...")
            await asyncio.sleep(self.success_sleep_timer)
        elif self.alert_type == "email" and self.email_options:
            await self.login()
        elif self.alert_type == "paypal":
            pass
    
    async def execute_minor_alert(self):
        audio_clip = AudioSegment.from_mp3("audio/short_ringtone_alert.mp3")
        play(audio_clip)

    async def login(self):
        await self.goto("https://secure.newegg.com/NewMyAccount/AccountLogin.aspx")

        # login
        login_email = self.email_options.get("email")
        login_pass = self.email_options.get("password")

        print("Entering login email...")
        await self.page.type('input[name="signEmail"]', login_email)
        await self.page.waitForNavigation({'waitUntil': 'load'})
        await self.page.click('button[id="signInSubmit"]')
        print("sleeping before solving login captcha")
        await asyncio.sleep(5)
        results = await self.solve()
        print(f"Login solving results: {results}")

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
        if not password_input:
            result = await self.solve()
            print(result)
        print("Entering login pass...")
        await asyncio.sleep(5)
        await self.page.type('input[name="password"]', login_pass)
        await self.page.waitForNavigation({'waitUntil': 'load'})
        await self.page.click('button[id="signInSubmit"]')

        print("Logging in...")
        await self.page.waitForNavigation()
    
    async def existing_element(self, elem_tag, elem_attr, elem_attr_values):
        elements = await self.page.querySelectorAll(elem_tag)
        for element in elements:
            eval_element = await self.page.evaluate(f"(element) => element.{elem_attr}", element)
            eval_element = eval_element.rstrip()
            if eval_element in elem_attr_values:
                print("Add Button Found!!!")
                return True

        return False

    async def get_element_text_content(self, elem_tag, elem_attr, elem_attr_value):
        elements = await self.page.querySelectorAll(elem_tag)
        for element in elements:
            eval_element = await self.page.evaluate(f"(element) => element.{elem_attr}", element)
            if eval_element == self.item_btn_title:
                return eval_element

        return False
