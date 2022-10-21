from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Custom selenium wait to find spin loader inside the ant design table
class IsTableLoading(object):
    def __init__(self, *args):
        pass

    def __call__(self, driver):
        loading_elemnts = driver.find_elements(By.CSS_SELECTOR, "span.ant-spin-dot.ant-spin-dot-spin")
        for loading_elem  in loading_elemnts:
            parent_elem = loading_elem.find_element(By.XPATH, '../../../..')
            if (parent_elem.get_attribute("class") == "ant-table-wrapper"):
                return  loading_elem
        return False


# Function which takes webDriver and waits until table loading mode to be false
def wait_to_finish_table_loading(driver):
    wait = WebDriverWait(driver,20)
    wait.until_not(IsTableLoading())

# A class to read all data on ant design table
class TableReader():
    def __init__(self, driver):
        self.table_data = []
        self.driver = driver

    def __get_current_page_data(self):
        rows = self.driver.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            col_data = []
            cols = row.find_elements(By.TAG_NAME, "td")
            for col in cols:
                col_data.append(col)
            self.table_data.append(col_data)

    def __get_table_data(self):
        self.__get_current_page_data()
        next_page_elem = self.driver.find_element(By.XPATH, '//li[@title="Next Page"]').find_element(By.TAG_NAME, "button")
        while next_page_elem != None and next_page_elem.is_enabled():
            next_page_elem.click()
            self.__get_current_page_data()
            next_page_elem = self.driver.find_element(By.XPATH, '//li[@title="Next Page"]').find_element(By.TAG_NAME, "button")

    def read(self):
        self.__get_table_data()
        return self.table_data




reader = TableReader()
data = reader.read()
pprint(data)


