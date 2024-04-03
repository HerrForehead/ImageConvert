from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import os
import time

# Start Chrome WebDriver
driver = webdriver.Edge(executable_path="bin/msedgedriver.exe")

# Open the HTML file
driver.get("http://127.0.0.1:5000/img2hex.html")

# Get the title of the page
title = driver.title

# Check if the title is correct
driver.implicitly_wait(5)

# Find the input element
image_input = driver.find_element(By.ID, "file-input")

# Send the image files
image_input.send_keys(os.path.abspath("output/output_black.bmp"))

# Clear the input element
image_input.clear()

# Send the image files
image_input.send_keys(os.path.abspath("output/output_red.bmp"))

# Set the identifier
identifier = driver.find_element(By.ID, "identifier")

# Empty the identifier
identifier.clear()

# Set the identifier
identifier.send_keys("img_")

# Find the generate button
generate_button = driver.find_element(By.CLASS_NAME, "generate-button")

# Click the generate button
generate_button.click()

# Copy output from textarea to file
output = driver.find_element(By.ID, "code-output")

# Remove content of Graphics.h if it already exists
if os.path.exists("output/Graphics.h"):
    os.remove("output/Graphics.h")

# Write the output to a file and clear the file if it already exists
with open("output/Graphics.h", "w") as file:
    file.write(output.get_attribute("value"))

print("3")

# Close the browser
driver.quit()