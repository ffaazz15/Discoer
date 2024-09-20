from selenium.webdriver.common.by import By

class Page_Locators:
    NEW_SESSION_BUTTON = (By.XPATH, "(//button[contains(text(), 'New Session')])[1]")
    TEXT_BOX = (By.XPATH, "//textarea[@id= 'chatInput']")
    CHART_BUTTON = (By.XPATH, "//button[@class='nav-link' and text()='Chart']")
    SOURCE_BUTTON = (By.XPATH, "//button[@class='nav-link' and text()='Source']")
    DISCOVER_ANSWER = (By.XPATH, "//div[contains(@class, 'bg-white')]/div/div")
    SQL_DISCOVER_ANSWER = (By.XPATH, "//div[@class='card m-2']/pre")
    DOCUMENTS_BUTTON = (By.XPATH, "(//a[text()='document'])[last()]")
    PDF_CONTENT = (By.CSS_SELECTOR, "embed[type='application/pdf']")
    email = (By.XPATH, "//input[@name='email']")
    password = (By.XPATH, "//input[@name='password']")
    submit_button  =(By.XPATH, "//button[@type='submit']")

