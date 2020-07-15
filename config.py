class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = "YOUR SECRET KEY"
    RECAPTCHA_PUBLIC_KEY = "YOUR PUBLIC KEY"
    RECAPTCHA_PRIVATE_KEY = "YOUR PRIVATE KEY"

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
