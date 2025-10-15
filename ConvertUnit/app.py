import streamlit as st
import requests

# -----------------------
# Streamlit configuration
# -----------------------
st.set_page_config(page_title="Unit Converter", page_icon="🌡️", layout="centered")
st.title("🌡️ Unit Converter App")
st.caption("Convert temperature, length, weight, and currency easily!")

# -----------------
# Utility functions
# -----------------

# Temperature 
def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32

# Length 
def convert_length(value, from_unit, to_unit):
    factors = {
        "Meter": 1.0,
        "Kilometer": 1000.0,
        "Centimeter": 0.01,
        "Millimeter": 0.001,
        "Mile": 1609.34,
        "Yard": 0.9144,
        "Foot": 0.3048,
        "Inch": 0.0254
    }
    return value * factors[from_unit] / factors[to_unit]

# Weight
def convert_weight(value, from_unit, to_unit):
    factors = {
        "Kilogram": 1.0,
        "Gram": 0.001,
        "Milligram": 0.000001,
        "Pound": 0.453592,
        "Ounce": 0.0283495
    }
    return value * factors[from_unit] / factors[to_unit]

# Currency (using free API)
def convert_currency(value, from_currency, to_currency):
    url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}"
    try:
        res = requests.get(url, timeout=5)
        data = res.json()
        rate = data["info"]["rate"]
        return value * rate
    except Exception:
        return None

# -------
# Main UI
# -------
option = st.selectbox(
    "Select Conversion Type:",
    ["Temperature", "Length", "Weight", "Currency"]
)

value = st.number_input("Enter value to convert:", value=0.0)

if option == "Temperature":
    from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
    to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])
    if st.button("Convert"):
        result = convert_temperature(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.2f} {to_unit}")

elif option == "Length":
    from_unit = st.selectbox("From", ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"])
    to_unit = st.selectbox("To", ["Meter", "Kilometer", "Centimeter", "Millimeter", "Mile", "Yard", "Foot", "Inch"])
    if st.button("Convert"):
        result = convert_length(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")

elif option == "Weight":
    from_unit = st.selectbox("From", ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"])
    to_unit = st.selectbox("To", ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"])
    if st.button("Convert"):
        result = convert_weight(value, from_unit, to_unit)
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")

elif option == "Currency":
    st.caption("💰 Using Free API: https://api.exchangerate.host/")
    from_currency = st.selectbox("From", ["USD", "EUR", "VND", "JPY", "GBP", "AUD"])
    to_currency = st.selectbox("To", ["USD", "EUR", "VND", "JPY", "GBP", "AUD"])
    if st.button("Convert"):
        result = convert_currency(value, from_currency, to_currency)
        if result is not None:
            st.success(f"{value} {from_currency} = {result:,.2f} {to_currency}")
        else:
            st.error("⚠️ Failed to fetch exchange rate. Try again later.")

