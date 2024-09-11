from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from os import getcwd

# Setting up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--headless=new")  # Running in headless mode

# Initializing the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Defining the path for the local HTML file
website = "https://allorizenproject1.netlify.app/"
driver.get(website)

# Defining the path for the output file
rec_file = f"{getcwd()}\\input.txt"

def listen():
    try:
        # Wait for the start button to become clickable and then click it
        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()
        print("Start button clicked.")
        print("Listening...")

        output_text = ""
        is_second_click = False
        
        while True:
            # Wait for the output element to appear and get its text content
            output_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, 'output'))
            )
            current_text = output_element.text.strip()

            # Check the text of the start button to see if listening has stopped
            if "Start Listening" in start_button.text and is_second_click:
                if output_text:
                    is_second_click = False
            elif "Listening..." in start_button.text:
                is_second_click = True

            # If the output text has changed, write the new text to the file
            if current_text != output_text:
                output_text = current_text
                with open(rec_file, "w") as file:
                    file.write(output_text.lower())
                    print("Aryan : " + output_text)  # Only keeping this line to show the final result
    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)


