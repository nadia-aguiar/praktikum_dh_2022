from selenium import webdriver
from selenium.webdriver.common.by import By

class Aceno:
    def __init__(self, driver):
        self.driver = driver
    
        self.url = "https://periodicoscientificos.ufmt.br/ojs/index.php/aceno/issue/archive"
        self.box = ".page" #CSS Selector
        #self.box_two = "issues_archive" #class
        #self.box_article = "li" #CSS Selector 
        self.box_texts = "obj_issue_summary" #class
        self.box_title = "title" # class

    def navegate (self):
        self.driver.get(self.url)

    def search(self): 
        element_box =  self.driver.find_element(By.CSS_SELECTOR, self.box)
        #element_box_two = element_box.find_element(By.CLASS_NAME, self.box_two)
        #element_box_articles = element_box.find_elements(By.TAG_NAME, self.box_article)
        element_box_texts = element_box.find_element(By.CLASS_NAME, self.box_texts)
        element_title_click = element_box_texts.find_element(By.CLASS_NAME, self.box_title)
        element_title_click.click()

        
        
        
ff = webdriver.Firefox()
a = Aceno(ff) 
a.navegate()  
a.search()  
ff.quit() 