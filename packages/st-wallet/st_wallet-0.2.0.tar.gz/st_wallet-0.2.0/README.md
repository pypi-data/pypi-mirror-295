# Streamlit Web3 Wallet Plugin 🌈💼

This is a Web3 wallet plugin designed for Streamlit applications. It provides Streamlit users with a simple yet powerful way to add Web3 wallet functionality to their data apps. 🚀

## Introduction 🎉

This plugin is a highly customizable base template that allows Streamlit developers to easily integrate Web3 wallet connection features into their applications. It offers a modern, user-friendly wallet connection interface, making blockchain interactions simple and intuitive. As a template, it provides developers with great flexibility to customize and extend according to specific needs. 🛠️

### Key Features ✨:

- Highly Customizable: Easily adjust and extend functionality based on your specific requirements 🔧
- Simple Integration: As a template, it can be quickly integrated into existing Streamlit projects 🔌
- Flexibility: Provides basic functionality while allowing developers to add custom logic and UI components 🎨

## Tech Stack 💻

- **Streamlit**: As the main application framework 🖥️
- **React**: For building user interface components ⚛️
- **Vite**: Provides fast development and build experience ⚡
- **RainbowKit**: Implements simple and intuitive wallet connection functionality 🌈
- **Ethers**: For interacting with Ethereum blockchain 🔗

## Installation 📦

To install the Streamlit Web3 Wallet Plugin, you can use pip:

```
pip install git+https://github.com/RSS3-Network/st-wallet.git
```

After installation, you can import and use the plugin in your Streamlit app.

## Getting Started 🚀

Here's a quick example of how to use the plugin in your Streamlit app:

```python
import streamlit as st

from st_wallet import st_wallet

if __name__ == "__main__":
    st.write("## Example of custom component")
    value = st_wallet()
    st.write(value)

```