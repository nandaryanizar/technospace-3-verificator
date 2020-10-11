import os
import dotenv

dotenv.load_dotenv(verbose=True)

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

AUTH_SERVICE_ADDR = os.getenv("AUTH_SERVICE_ADDR")