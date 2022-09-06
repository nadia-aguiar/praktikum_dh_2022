from selenium import webdriver
from selenium.webdriver.common.by import By

class Aceno:
    def __init__(self, driver):
        self.driver = driver
    
        self.url = "https://periodicoscientificos.ufmt.br/ojs/index.php/aceno/issue/archive"
        self.box = ".page" #CSS Selector
        self.box_texts = "obj_issue_summary" #class
        self.box_title = "title" # class

        self.page_articles = "page.page_issue" #class
        self.box_articles = "sections" #class
        self.list_articles = " div.section:nth-child(2)" #CSS SELECTOR    
        self.article_title_id = "[id^='article-']" #CSS Selector

    def navegate (self):
        self.driver.get(self.url)

    def open_journal(self): 
        element_box =  self.driver.find_element(By.CSS_SELECTOR, self.box)
        element_box_texts = element_box.find_element(By.CLASS_NAME, self.box_texts)
        element_title_click = element_box_texts.find_element(By.CLASS_NAME, self.box_title)
        element_title_click.click()

    def open_text(self):
        element_page_articles = self.driver.find_element(By.CLASS_NAME, self.page_articles)
        element_box_articles = element_page_articles.find_element(By.CLASS_NAME, self.box_articles)            
        elelemts_list_articles = element_box_articles.find_element(By.CSS_SELECTOR, self.list_articles)
        element_article_title_id = elelemts_list_articles.find_element(By.CSS_SELECTOR, self.article_title_id)
        element_article_title_id.click()  

    #def get_text_information(self):     



        
        
ff = webdriver.Firefox()
a = Aceno(ff) 
a.navegate()  
a.open_journal() 
a.open_text() 
ff.quit() 


