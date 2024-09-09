import os

import streamlit.components.v1 as components

# Use environment variable to control release status
IS_RELEASE = os.getenv("STREAMLIT_COMPONENT_RELEASE", "true").lower() == "true"

# Component name
COMPONENT_NAME = "web3_wallet"

# Local development server URL
DEV_URL = "http://localhost:5173/"


def declare_component():
    if not IS_RELEASE:
        print("Running in development mode.")
        return components.declare_component(COMPONENT_NAME, url=DEV_URL)
    else:
        print("Running in production mode.")
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        build_dir = os.path.join(parent_dir, "frontend", "dist")
        return components.declare_component(COMPONENT_NAME, path=build_dir)


_component_func = declare_component()


def st_wallet(height=480, key=None, **kwargs):
    """
    Create a Web3 wallet component.

    Args:
    height (int, optional): Height of the component in pixels.
    key (str, optional): Streamlit key for the component. Used for multiple instances on the same page.
    **kwargs: Additional parameters to pass to the component.

    Returns:
    dict: A dictionary containing wallet state and operation results.
    """
    component_value = _component_func(
        height=height,
        key=key,
        **kwargs
    )
    return component_value
