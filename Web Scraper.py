import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Function to send email
def send_email(price_data):
    from_email = "your_email@gmail.com"
    to_email = "your_email@gmail.com"
    subject = "Flight Price Data"
    body = f"Here is the flight price data:\n\n{price_data}"

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        # Use App Password or enable less secure apps
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, 'your_app_password')  # Use App Password here
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


# Set up Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL for flight search (example: Kayak)
flight_search_url = 'https://www.kayak.com/flights'

# Navigate to the flight search page
driver.get(flight_search_url)

# Wait for the page to load (increase the time if needed)
time.sleep(10)  # 10 seconds should be enough for dynamic content to load

# Now scrape the flight prices using BeautifulSoup
content = driver.page_source
soup = BeautifulSoup(content, features="html.parser")

# Extract flight data (Example: let's assume we are scraping price and flight details)
flight_prices = []
flight_details = []

# Inspect the page and update these class names as needed
for flight in soup.find_all('div', {'class': 'price-container'}):  # Replace with correct HTML structure
    price = flight.find('span', {'class': 'price'})  # Replace with correct HTML structure
    if price:
        flight_prices.append(price.text)

# Extract other details (Example: flight details like departure time, etc.)
for details in soup.find_all('div', {'class': 'flight-details'}):  # Replace with correct HTML structure
    detail = details.find('span', {'class': 'detail'})  # Replace with correct HTML structure
    if detail:
        flight_details.append(detail.text)

# Save data to a DataFrame
flight_data = pd.DataFrame({'Price': flight_prices, 'Details': flight_details})

# Print the data
print(flight_data)

# Save to CSV for analysis later
flight_data.to_csv('flight_prices.csv', index=False, encoding='utf-8')

# Send email with the scraped data
send_email(flight_data)

# Close the browser
driver.quit()
