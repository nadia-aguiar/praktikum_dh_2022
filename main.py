from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
from selenium.common.exceptions import NoSuchElementException 


class Aceno:
    def __init__(self, driver):
        self.driver = driver
    
        self.url = "https://periodicoscientificos.ufmt.br/ojs/index.php/aceno/issue/archive"
        self.all_journals = ".page" #CSS Selector 
        self.journal = "obj_issue_summary" #class
        self.date_journal = "title" # class

        self.page_articles = "page.page_issue" #class
        self.box_articles = "sections" #class
        self.list_articles = "/html/body/div/div[1]/div[1]/div"# div.section:nth-child(2)" #CSS SELECTOR  
        self.article_title_id = "[id^='article-']" #CSS Selector

        self.box_info_text = "obj_article_details" #class
        self.number_journal = "a.title" #CSS Selector
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
        elements_list_articles = element_box_articles.find_element(By.XPATH, self.list_articles)
        element_article_title_id = elements_list_articles.find_element(By.CSS_SELECTOR, self.article_title_id)
        element_article_title_id.click()  

    def get_text_information(self):
        element_box_info_text = self.driver.find_element(By.CLASS_NAME, self.box_info_text)
        try:
            element_number_journal = element_box_info_text.find_element(By.CSS_SELECTOR, self.number_journal).text 
        except NoSuchElementException:
            pass  
        try:
            element_author_text = element_box_info_text.find_element(By.CLASS_NAME, self.author_text).text
        except NoSuchElementException:
            pass
        try:
            element_doi_text = element_box_info_text.find_element(By.CLASS_NAME, self.doi_text).text
        except NoSuchElementException:
            pass
        try:
            element_abstract_text = element_box_info_text.find_element(By.CLASS_NAME, self.abstract_text).text
        except NoSuchElementException:
            pass

        list_text_information = [element_number_journal, element_author_text, element_doi_text, element_abstract_text]
        return list_text_information
        
                
         

    def save_text_information(self):
        text_information = self.get_text_information()
        print(text_information)
        if not os.path.exists("Aceno"):
            os.makedirs("Aceno")
        with open("aceno_texts.csv", "w", newline='') as file:
            writer = csv.writer(file)            
            writer.writerow(text_information)
            writer.writerow()

    def to_iterate(self):
        open_one_journal = self.open_journal()
        open_one_text = self.open_text()
        get_one_text = self.get_text_information()
        save_file =self.save_text_information()
        for i in range(len(self.element_journal)):
            for i in range(len(self.element_article_title_id)):
                open_one_journal()
                open_one_text()
                get_one_text()
                save_file()
        print("It's done!")


        
ff = webdriver.Firefox()
a = Aceno(ff) 
a.navegate()  
a.open_journal() 
a.open_text() 
a.get_text_information()
a.save_text_information()
a.to_iterate()
ff.quit() 


