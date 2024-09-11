"""Settings for custom user model"""

import os


USERNAME_MAX_LENGTH = os.getenv('USERNAME_MAX_LENGTH', 30)

MIN_PASSWORD_LENGTH = os.getenv('MIN_PASSWORD_LENGTH', 8)
