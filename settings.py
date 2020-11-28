from fake_useragent import UserAgent


alert_type = "email"
item_data = [
    {
        "name": "ASUS TUF GeForce RTX 3080",
        "url": "https://www.newegg.com/",
        "cart_url": "https://secure.newegg.com/shop/cart",
        "item_url": "https://www.newegg.com/asus-geforce-rtx-3080-tuf-rtx3080-o10g-gaming/p/N82E16814126452?Description=rtx%203080&cm_re=rtx_3080-_-14-126-452-_-Product",
        "login_url": "https://secure.newegg.com/NewMyAccount/AccountLogin.aspx",
        "item_title": "ASUS TUF Gaming GeForce RTX 3080 TUF-RTX3080-O10G-GAMING Video Card"
    },
    # {
    #     "name": "MSI GeForce RTX 3080 X TRIO",
    #     "url": "https://www.newegg.com/",
    #     "item_url": "https://www.newegg.com/msi-geforce-rtx-3080-rtx-3080-gaming-x-trio-10g/p/N82E16814137597",
    #     "cart_url": "https://secure.newegg.com/shop/cart",
    #     "login_url": "https://secure.newegg.com/NewMyAccount/AccountLogin.aspx",
    #     "item_title": "MSI GeForce RTX 3080 DirectX 12 RTX 3080 GAMING X TRIO 10G 10GB 320-Bit GDDR6X PCI Express 4.0 HDCP Ready Video Card",
    # },
    {
        "name": "WD Blue 3D NAND 500GB",
        "url": "https://www.newegg.com/",
        "item_url": "https://www.newegg.com/western-digital-blue-500gb/p/N82E16820250087",
        "cart_url": "https://secure.newegg.com/shop/cart",
        "login_url": "https://secure.newegg.com/NewMyAccount/AccountLogin.aspx",
        "item_title": "WD Blue 3D NAND 500GB Internal SSD - SATA III 6Gb/s 2.5\"/7mm Solid State Drive - WDS500G2B0A",
    },
    # {
    #     "name": "ASUS ROG Strix GeForce RTX 3080",
    #     "url": "https://www.newegg.com/",
    #     "item_url": "https://www.newegg.com/asus-geforce-rtx-3080-rog-strix-rtx3080-o10g-gaming/p/N82E16814126457",
    #     "cart_url": "https://secure.newegg.com/shop/cart",
    #     "login_url": "https://secure.newegg.com/NewMyAccount/AccountLogin.aspx",
    #     "item_title": "ASUS ROG Strix GeForce RTX 3080 DirectX 12 ROG-STRIX-RTX3080-O10G-GAMING 10GB 320-Bit GDDR6X PCI Express 4.0 x16 HDCP Ready Video Card",
    # },
    # {
    #     "name": "MSI GeForce RTX 3080 VENTUS 3X",
    #     "url": "https://www.newegg.com/",
    #     "item_url": "https://www.newegg.com/msi-geforce-rtx-3080-rtx-3080-ventus-3x-10g/p/N82E16814137600",
    #     "cart_url": "https://secure.newegg.com/shop/cart",
    #     "login_url": "https://secure.newegg.com/NewMyAccount/AccountLogin.aspx",
    #     "item_title": "MSI GeForce RTX 3080 DirectX 12 RTX 3080 VENTUS 3X 10G 10GB 320-Bit GDDR6X PCI Express 4.0 HDCP Ready Video Card",
    # },
    # {
    #     "name": "EVGA GeForce RTX 3080",
    #     "url": "https://www.newegg.com/",
    #     "item_url": "https://www.newegg.com/evga-geforce-rtx-3080-10g-p5-3897-kr/p/N82E16814487518",
    #     "cart_url": "https://secure.newegg.com/shop/cart",
    #     "login_url": "https://secure.newegg.com/NewMyAccount/AccountLogin.aspx",
    #     "item_title": "EVGA GeForce RTX 3080 FTW3 ULTRA GAMING Video Card, 10G-P5-3897-KR, 10GB GDDR6X, iCX3 Technology, ARGB LED, Metal Backplate",
    # },
    # {
    #     "name": "ASUS Radeon RX 6800 XT",
    #     "url": "https://www.newegg.com/",
    #     "item_url": "https://www.newegg.com/asus-radeon-rx-6800-xt-rx6800xt-16g/p/N82E16814126472",
    #     "cart_url": "https://secure.newegg.com/shop/cart",
    #     "login_url": "https://secure.newegg.com/NewMyAccount/AccountLogin.aspx",
    #     "item_title": "ASUS Radeon RX 6800 XT RX6800XT-16G 16GB 256-Bit GDDR6 PCI Express 4.0 Video Card",
    # },
    # {
    #     "name": "GIGABYTE Radeon RX 6800 XT",
    #     "url": "https://www.newegg.com/",
    #     "item_url": "https://www.newegg.com/gigabyte-radeon-rx-6800-xt-gv-r68xt-16gc-b/p/N82E16814932373",
    #     "cart_url": "https://secure.newegg.com/shop/cart",
    #     "login_url": "https://secure.newegg.com/NewMyAccount/AccountLogin.aspx",
    #     "item_title": "GIGABYTE Radeon RX 6800 XT DirectX 12 GV-R68XT-16GC-B 16GB 256-Bit GDDR6 PCI Express 4.0 x16 ATX Video Card",
    # },
    # {
    #     "name": "ASUS TUF Gaming Radeon RX 6800",
    #     "url": "https://www.newegg.com/",
    #     "item_url": "https://www.newegg.com/asus-radeon-rx-6800-tuf-rx6800-o16g-gaming/p/N82E16814126478",
    #     "cart_url": "https://secure.newegg.com/shop/cart",
    #     "login_url": "https://secure.newegg.com/NewMyAccount/AccountLogin.aspx",
    #     "item_title": "ASUS TUF Gaming Radeon RX 6800 TUF-RX6800-O16G-GAMING 16GB 256-Bit GDDR6 PCI Express 4.0 HDCP Ready Video Card",
    # },
]

agent = UserAgent(verify_ssl=False).random
args = [
    '--cryptauth-http-host ""',
    '--disable-accelerated-2d-canvas',
    '--disable-background-networking',
    '--disable-background-timer-throttling',
    '--disable-browser-side-navigation',
    '--disable-client-side-phishing-detection',
    '--disable-default-apps',
    '--disable-dev-shm-usage',
    '--disable-device-discovery-notifications',
    '--disable-extensions',
    '--disable-features=site-per-process',
    '--disable-hang-monitor',
    '--disable-java',
    '--disable-popup-blocking',
    '--disable-prompt-on-repost',
    '--disable-setuid-sandbox',
    '--disable-sync',
    '--disable-translate',
    '--disable-web-security',
    '--disable-webgl',
    '--metrics-recording-only',
    '--no-first-run',
    '--safebrowsing-disable-auto-update',
    '--no-sandbox',
    '--timeout 5',
    # Automation arguments
    '--enable-automation',
    '--password-store=basic',
    '--use-mock-keychain',
    '--lang="en-US"',
    f'--user-agent="{agent}"'
]
options = {
    "ignoreHTTPSErrors": True,
    "defaultViewport": None,
    "args": args,
}
email_options = {
    "email": "getinmycart1@gmail.com",
    "password": "Mouse31@",
    "recipients": ["investmentracker1@gmail.com"],
}
email_subject = "*** ITEM ADDED TO YOUR CART ***"
email_body = "Item has been added to your cart. Hurry and buy it now: https://newegg.com"
paypal_options = None
