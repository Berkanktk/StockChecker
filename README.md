# StockChecker
This is a simple selenium-based stock checker made with Python, that checks if a product is on stock on a specified platform.


## Usage
There is 7 different steps(TODOs) you have to follow in order for the script to function properly after your needs.
1. Make a copy of the `.env.example` so it becomes `.env` and fill in the values.
2. Insert product specific information. This includes both a name and link for the product.
3. Insert how often a lookup should be performed by the script. This value should be in seconds.
4. Fill in the what the script should look after (Find a product that is not in stock on the platform and add the description under the error_msg. Do the opposite and add the description to success_msg).
5. If you want to have email validations in order to assure the script is running, you can enable email validations by changing the value for the `choice` field to `True`. (This is on by default)
6. If you want to add CC recipients so multiple users can get notified by email, this can be done here. Remember to seperate e-mails by a comma.
7. If you want to setup discord announcements, a Discord Webhook URL has to be added inside the `.env` file, and the value for the `discord_announcement` field shoud be changed to `True`. (This is False by default)

## Installation
Run
```bash
> pip install -r requirements.txt
```

### Chromedriver
Chromedriver can be installed in two ways. 

1. By downloading it from the website and the specifying the path to the driver.
2. By using Service that comes with the ChromeDriver library and then specifying which driver manager that should be used so it can be downloaded automatically.

```python
# Automatic installation
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Manual installation 1/2
> sudo apt-get install chromium-chromedriver

# Now insert the path for the chromedriver 2/2
driver = webdriver.Chrome('usr/bin/chromedriver')  
```

#### Options
By default the script is being run in a headless manner, meaning the chrome GUI won't be shown. In short terms, the script is completely running in the background.

```python
# Chrome Driver options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Comment out if you want to have the GUI
```

## Hosting tips :)
You can upload the bot to different cloud service providers by following their deployment methods.

BUT, keep in mind that:
1. Linode blocks SMTP ports
2. Rasperry Pi's uses ARM, and that can be a pain in the ass when using the chromedriver. (There is a chromedriver for ARM though, but again it can get quite annoying.)
3. Amazon EC2 instances should be fine, but for some reason i could not make it to work properly.
4. Hosting it yourself. But its not optimal, so you have to do a little research yourself!