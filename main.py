from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import csv

class Aceno:
    def __init__(self, driver):
        self.driver = driver
    
        self.url = "https://periodicoscientificos.ufmt.br/ojs/index.php/aceno/issue/archive"
        self.all_journals = ".page" #CSS Selector 
        self.journal = "obj_issue_summary" #class
        self.date_journal = "title" # class

        self.page_articles = "page.page_issue" #class
        self.box_articles = "sections" #class
        self.list_articles = " div.section:nth-child(2)" #CSS SELECTOR   
        self.article_title_id = "[id^='article-']" #CSS Selector

        self.box_info_text = "obj_article_details" #class
        self.author_text = "authors" #class
        self.doi_text = "item.doi" #class
        self.abstract_text = "item.abstract" #class



    def navegate (self):
        self.driver.get(self.url)

    def open_journal(self): 
        element_all_journals =  self.driver.find_element(By.CSS_SELECTOR, self.all_journals)
        element_journal = element_all_journals.find_element(By.CLASS_NAME, self.journal)
        element_date_journal_click = element_journal.find_element(By.CLASS_NAME, self.date_journal)
        element_date_journal_click.click()

    def open_text(self):
        element_page_articles = self.driver.find_element(By.CLASS_NAME, self.page_articles)
        element_box_articles = element_page_articles.find_element(By.CLASS_NAME, self.box_articles)            
        elements_list_articles = element_box_articles.find_element(By.CSS_SELECTOR, self.list_articles)
        element_article_title_id = elements_list_articles.find_element(By.CSS_SELECTOR, self.article_title_id)
        element_article_title_id.click()  

    def get_text_information(self):
        element_box_info_text = self.driver.find_element(By.CLASS_NAME, self.box_info_text)
        element_author_text = element_box_info_text.find_element(By.CLASS_NAME, self.author_text).text
        element_doi_text = element_box_info_text.find_element(By.CLASS_NAME, self.doi_text).text
        element_abstract_text = element_box_info_text.find_element(By.CLASS_NAME, self.abstract_text).text
        list_text_information = [element_author_text, element_doi_text, element_abstract_text]
        return list_text_information        
         

    def save_text_information(self):
        text_information = self.get_text_information()
        #print(text_information)
        if not os.path.exists("Aceno"):
            os.makedirs("Aceno")
        with open("aceno_texts.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(text_information)
                    
        
ff = webdriver.Firefox()
a = Aceno(ff) 
a.navegate()  
a.open_journal() 
a.open_text() 
a.get_text_information()
a.save_text_information()
ff.quit() 


