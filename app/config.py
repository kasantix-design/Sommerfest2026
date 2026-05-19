import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        'change-this-in-production'
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///sommerfest.db'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')

    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    LANGUAGES = ['no', 'en']

    EVENT_NAME = 'Sommerfest 2026'

    GRILLING_START = '2026-07-04 15:00:00'
    GRILLING_END = '2026-07-04 19:00:00'

    EVENING_START = '2026-07-04 20:00:00'
    EVENING_END = '2026-07-05 00:00:00'

    ADMIN_EMAIL = 'kasantix@gmail.com'

    EXPORT_FOLDER = 'exports'

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
