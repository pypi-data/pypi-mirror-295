from devvapi import App, AppConfig

# App Configuration
class ___AppName___Config(AppConfig):
    path = "/(___app_name___)"
    name = "(___app_name___)"
    version: int = "(___version___)"

# App
app = App(___AppName___Config)