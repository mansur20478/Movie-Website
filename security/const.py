import random


def gen_password():
    base = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    password_len = 8
    password = "".join(random.sample(base, password_len))
    return password


SECRET_KEY = "security_key"
TOKEN = "IMPOSSIBLE_TO_HACK_TOKEN"
DOMEN = "http://localhost:5000"
# RECAPTCHA_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
# RECAPTCHA_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
RECAPTCHA_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
RECAPTCHA_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
MAIL_SERVER = "smtp.yandex.ru"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = ""
FULL_MAIL_USERNAME = ""
MAIL_PASSWORD = ""
