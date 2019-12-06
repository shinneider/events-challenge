from decouple import config

SYMPLA_EVENTS_URL = config('SYMPLA_EVENTS_URL')

USER_AGENT_STRING = ("Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>)" 
    "AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile" 
    "Safari/<WebKit Rev>"
)  # Android user string

BROWSER_HEADLESS = config('BROWSER_HEADLESS', cast=bool)

USER_ID = config('USER_ID', cast=bool)

MICRO_SERVICE_EVENT_URL = config('MICRO_SERVICE_EVENT_URL')

# Python Logging Dict Config
# https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'crawler': {
            'format': '[%(asctime)s] [%(levelname)s] Crawler - %(message)s',
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './logs/app.log',
            'formatter': 'crawler',
        },
    },
    'loggers': {
        'crawler': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}