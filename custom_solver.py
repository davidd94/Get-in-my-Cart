import time
from datetime import datetime

from goodbyecaptcha.solver import Solver
from pydub import AudioSegment
from pydub.playback import play

from utils.email import send_email

timestamp = round(time.time())


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
        item_url,
        lang,
        options,
        alert_type,
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
        self.alert_type = alert_type
        self.success_sleep_timer = success_sleep_timer
        self.email_options = email_options
        self.paypal_options = paypal_options
        self.original_url = pageurl

        super(MySolver, self).__init__(
            pageurl=pageurl,
            lang=lang,
            options=options
        )

    async def on_start(self):
        # Set or Change data
        print(f"Set URL: {self.url}")
        print(f"Current URL on_start: {self.page.url}")
        
        # await self.navigate_to_item()

        # await self.add_item_to_cart()

        # await self.page.screenshot({"path": f"./images/on_start_ss-{timestamp}.png"})
        # await self.page.type('input[name="input1"]', 'value')
    
    async def on_finish(self):
        print("finshing inside solver")
        time.sleep(10)
        js_func_empty = "window.find('No item in your shopping cart');"
        js_func_added = "window.find('Item has been added to cart.');"
        
        found_empty_cart_text = await self.page.evaluate(js_func_empty)
        found_added_cart_text = await self.page.evaluate(js_func_added)

        print(f"Cart empty: {found_empty_cart_text}")
        print(f"Added to Cart: {found_added_cart_text}")

        await self.page.screenshot({"path": f"./images/on_finish_ss-{timestamp}.png"})

        if not found_empty_cart_text and found_added_cart_text:
            print(f"Successfully added to cart at: {datetime.now()}")

            if self.alert_type == "sound":
                await self.success_alert()
                print(f"Sleeping for {self.success_sleep_timer}...")
                time.sleep(self.success_sleep_timer)
            elif self.alert_type == "email" and self.email_options:
                await self.login()
                await send_email(self.email_options.get("email"))
            elif self.alert_type == "paypal":
                pass

            return True

        return False

    async def navigate_to_item(self):
        print(f"Redirecting to Set URL... {self.item_url}")
        await self.page.goto(url=self.item_url)
        # await self.page.waitForNavigation({'waitUntil': 'load'})
        await self.page.screenshot({"path": f"./images/on_navigate_ss-{timestamp}.png"})

    async def add_item_to_cart(self):
        print("adding item to cart...")
        btn_title = await self.existing_element(
            elem_tag="button",
            elem_attr="title",
            elem_attr_val="btn-wide",
        )
        print("button title below...")
        print(btn_title)
        await self.page.click('button[class="btn-wide"]')

    async def success_alert(self):
        print("Alerting user....")
        audio_clip = AudioSegment.from_mp3("audio/annoying_alarm.mp3")
        play(audio_clip)

    async def login(self):
        await self.goto("https://secure.newegg.com/NewMyAccount/AccountLogin.aspx")

        # login
        login_email = self.email_options.get("email")
        login_pass = self.email_options.get("password")

        print("Entering login email...")
        await self.page.type('input[name="signEmail"]', login_email)
        await self.page.click('button[id="signInSubmit"]')

        # email_code_elem = await self.existing_element(
        #     elem_tag="div",
        #     elem_attr="class",
        #     elem_attr_val="form-v-code"
        # )

        # recaptcha_elem = await self.existing_element(
        #     elem_tag="textarea",
        #     elem_attr="id",
        #     elem_attr_val="g-recaptcha-response"
        # )

        # if email_code_elem:
        #     print("Require email code to login...")
        #     time.sleep(240)
        #     await self.page.click('button[id="signInSubmit"]')
        
        # if recaptcha_elem:
        #     print("Solving recaptcha for login...")
        #     await self.solve()
        
        password_input = await self.existing_element(
            elem_tag="input",
            elem_attr="id",
            elem_attr_val="labeled-input-password",
        )

        if not password_input:
            result = await self.solve()
            print(result)


        await self.page.waitForSelector('#labeled-input-password', {"timeout": 60000})

        print("Entering login pass...")
        await self.page.type('input[name="password"]', login_pass)
        await self.page.click('button[id="signInSubmit"]')

        print("Logging in...")
        await self.page.waitForNavigation()
    
    async def existing_element(self, elem_tag, elem_attr, elem_attr_val):
        element = await self.page.querySelector(elem_tag)
        print(f"Evaluating element ({elem_tag} - {elem_attr_val}) results below")
        print(element)
        eval_element = await self.page.evaluate(f"(element) => element.{elem_attr}", element)
        print(f"Evaluated element ({elem_tag} - {elem_attr_val}) results below")
        print(eval_element)

        if elem_attr_val == eval_element:
            print("ELEMENT FOUND!!")
            return True

        return False
