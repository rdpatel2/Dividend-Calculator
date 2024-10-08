import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class data:

  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
  } 

  def __init__ (self):
    self.driver = webdriver.Chrome()

  def get_etf_price(self, ticker): # Gets the current price of the ETF

    url = f"https://etfdb.com/etf/{ticker}/#etf-ticker-profile"
        
    # Set up the Selenium WebDriver (Chrome in this case)
    self.driver.get(url)

    # Wait for the page to load (adjust time if necessary)
    WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "stock_price_value")))

    # Get the page source after the JavaScript has executed
    soup = BeautifulSoup(self.driver.page_source, "html.parser")
    price = soup.find("span", id="stock_price_value").text
    price = price.replace("\n", "")
    price = price.replace("$", "")
    time.sleep(5)
    return float(price)

  def get_dividend_yield(self, ticker): # Gets the annual dividend yield of the ETF
    url = f"https://etfdb.com/etf/{ticker}/#etf-ticker-profile"
        
    # Set up the Selenium WebDriver (Chrome in this case)
    self.driver.get(url)

    # Wait for the page to load (adjust time if necessary)
    # Get the page source after the JavaScript has executed
    soup = BeautifulSoup(self.driver.page_source, "html.parser")
    dividendYields = soup.find_all("td", class_="center")
    dividendYield = dividendYields[70].text
    dividendYield = dividendYield.replace("\n", "")
    dividendYield = dividendYield.replace("$", "")

    return float(dividendYield)

  def get_dividend_rate(self, ticker): # Gets the dividend percentage of the ETF
    price = self.get_etf_price(ticker)
    dividendYield = self.get_dividend_yield(ticker)
    dividendRate = dividendYield / price
    return round(dividendRate, 4)
  
  def get_etf_growth(self, ticker): # Gets the YTD growth of the ETF
    url = f"https://etfdb.com/etf/{ticker}/#etf-ticker-profile"
        
    # Set up the Selenium WebDriver (Chrome in this case)
    self.driver.get(url)

    # Wait for the page to load (adjust time if necessary)

    # Get the page source after the JavaScript has executed
    soup = BeautifulSoup(self.driver.page_source, "html.parser")
    growthPercent = soup.find_all("td", class_="col-lg-4 col-xs-4")
    growth = growthPercent[6].text
    growth = growth.replace("\n", "")
    growth = growth.replace("%", "")
    return float(growth) / 100

  def get_dividend_payouts(self, ticker): # Gets the price per dividend paid
    url = f"https://etfdb.com/etf/{ticker}/#etf-ticker-profile"
        
    # Set up the Selenium WebDriver (Chrome in this case)
    self.driver.get(url)

    # Wait for the page to load (adjust time if necessary)

    # Get the page source after the JavaScript has executed
    soup = BeautifulSoup(self.driver.page_source, "html.parser")
    payouts = soup.find_all("td", class_="center")
    payout = payouts[64].text
    payout = payout.replace("\n", "")
    payout = payout.replace("$", "")
    return float(payout)

  def get_num_payouts(ticker):
    return (data.get_dividend_yield(ticker) / data.get_dividend_payouts(ticker))
  
class Prediction:
  def __init__(self, data_instance):
    self.data = data_instance

  def get_future_ETF_price(self, ticker, years):
    price = self.data.get_etf_price(ticker)
    growth = self.data.get_etf_growth(ticker)
    for _ in range(years):
      price = price * (1 + growth)
    return round(price, 2)

  def get_future_dividend_yield(self, ticker, years):
    future_price = self.get_future_ETF_price(ticker, years)
    dividend_rate = self.data.get_dividend_rate(ticker)
    future_dividend_yield = future_price * dividend_rate
    return round(future_dividend_yield, 2)

