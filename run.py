import os
from app import create_app

app = create_app(os.environ['APP_SETTINGS'])
app.run()

