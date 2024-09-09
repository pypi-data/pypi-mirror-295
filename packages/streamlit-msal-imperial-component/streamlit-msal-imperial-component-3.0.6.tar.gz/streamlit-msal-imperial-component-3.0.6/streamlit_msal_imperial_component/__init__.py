import os
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
import os
from io import BytesIO
import streamlit as st
import requests
import pandas as pd
import base64

# Configuration for the component
_USE_WEB_DEV_SERVER = False
_WEB_DEV_SERVER_URL = os.getenv("WEB_DEV_SERVER_URL", "http://localhost:5173/")
COMPONENT_NAME = "msal_authentication"

if _USE_WEB_DEV_SERVER:
    _component_func = components.declare_component(name=COMPONENT_NAME, url=_WEB_DEV_SERVER_URL)
else:
    build_dir = str(Path(__file__).parent / "frontend" / "dist")
    _component_func = components.declare_component(name=COMPONENT_NAME, path=build_dir)

def msal_authentication(
        base_url,
        auth,
        cache,
        login_request=None,
        logout_request=None,
        login_button_text="Login",
        logout_button_text="Logout",
        class_name=None,
        html_id=None,
        key=None
):
    return _component_func(
        base_url=base_url,
        auth=auth,
        cache=cache,
        login_request=login_request,
        logout_request=logout_request,
        login_button_text=login_button_text,
        logout_button_text=logout_button_text,
        class_name=class_name,
        html_id=html_id,
        default=None,
        key=key
    )
