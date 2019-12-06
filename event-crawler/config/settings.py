from decouple import config

SYMPLA_EVENTS_URL = config('SYMPLA_EVENTS_URL')
USER_AGENT_STRING = ("Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>)" 
    "AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile" 
    "Safari/<WebKit Rev>"
)  # Android user string
BROWSER_HEADLESS = config('BROWSER_HEADLESS', cast=bool)