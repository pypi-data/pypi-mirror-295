import streamlit as st

from st_wallet import st_wallet

if __name__ == "__main__":
    st.write("## Example of custom component")
    value = st_wallet()
    st.write(value)
