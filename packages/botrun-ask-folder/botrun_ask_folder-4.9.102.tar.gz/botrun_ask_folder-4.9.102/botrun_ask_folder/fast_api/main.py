from fastapi import FastAPI, Request
from chainlit.utils import mount_chainlit
from botrun_ask_folder.fast_api.router_botrun_ask_folder import router
from botrun_ask_folder.fast_api.drive_api import (
    drive_api_router,
)
from botrun_ask_folder.fast_api.storage_api import (
    storage_api_router,
)
from botrun_ask_folder.fast_api.queue_api import (
    queue_api_router,
)
from botrun_ask_folder.fast_api.router_linebot import (
    linebot_router,
)
from botrun_ask_folder.fast_api.line_oauth_provider import LineOAuthProvider
from botrun_ask_folder.fast_api.fief_oauth_provider import FiefOAuthProvider
from chainlit.oauth_providers import providers
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
api_botrun = FastAPI()


api_botrun.include_router(router)
api_botrun.include_router(drive_api_router)
api_botrun.include_router(storage_api_router)
api_botrun.include_router(queue_api_router)
api_botrun.include_router(linebot_router)
app.mount("/api/botrun", api_botrun)

# 注册 LINE OAuth provider
providers.append(LineOAuthProvider())

# 注册 Fief OAuth provider
providers.append(FiefOAuthProvider())

# Chainlit OAuth 配置
os.environ["OAUTH_LINE_CLIENT_ID"] = os.getenv("OAUTH_LINE_CLIENT_ID", "")
os.environ["OAUTH_LINE_CLIENT_SECRET"] = os.getenv("OAUTH_LINE_CLIENT_SECRET", "")
os.environ["OAUTH_LINE_REDIRECT_URI"] = os.getenv("OAUTH_LINE_REDIRECT_URI", "")

# Fief OAuth 配置
os.environ["FIEF_CLIENT_ID"] = os.getenv("FIEF_CLIENT_ID", "")
os.environ["FIEF_CLIENT_SECRET"] = os.getenv("FIEF_CLIENT_SECRET", "")
os.environ["FIEF_BASE_URL"] = os.getenv("FIEF_BASE_URL", "")
os.environ["FIEF_REDIRECT_URI"] = os.getenv("FIEF_REDIRECT_URI", "")

# Mount Chainlit app
current_dir = os.path.dirname(os.path.abspath(__file__))
chainlit_path = os.path.join(current_dir, "chainlit_app.py")
mount_chainlit(app=app, target=chainlit_path, path="/botrun_chat")
