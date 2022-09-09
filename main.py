from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import os
from selenium.common.exceptions import NoSuchElementException 


class Aceno:
    def __init__(self, driver):
        self.driver = driver
    
        self.url = "https://periodicoscientificos.ufmt.br/ojs/index.php/aceno/issue/archive"
        self.all_journals = ".issues_archive" #CSS Selector 
        self.journal = "obj_issue_summary" #class
        self.date_journal = "title" # class
        self.issue_link = "href" # attribute

        self.page_articles = "page.page_issue" #class
        self.box_articles = "sections" #class
        self.list_articles = "obj_article_summary"# class  
        self.article_title_id = "[id^='article-']" #CSS Selector
        self.article_link = "href" #attribute

        self.box_info_text = "obj_article_details" #class
        self.number_journal = "a.title" #CSS Selector
        self.author_text = "authors" #class
        self.doi_text = "item.doi" #class
        self.abstract_text = "html body.pkp_page_article.pkp_op_view div.pkp_structure_page div.pkp_structure_content.has_sidebar div.pkp_structure_main div.page.page_article article.obj_article_details div.row div.main_entry section.item.abstract p"
        #CSS Selector
        self.return_page_article = "/html/body/div[1]/div[1]/div[1]/div/article/div/div[2]/div[4]/section[1]/div/a" #XPATH


    def navegate (self):
        self.driver.get(self.url)

    #function to get list of all issue links
    def get_all_issues(self):
        element_issues_box = self.driver.find_element(By.CSS_SELECTOR, self.all_journals)
        element_all_issues = element_issues_box.find_elements(By.CLASS_NAME, self.journal)
        link_list = []
        for element_issue in element_all_issues:
            element_issue_title = element_issue.find_element(By.CLASS_NAME, self.date_journal)
            element_link_issue = element_issue_title.get_attribute(self.issue_link)
            link_list.append(element_link_issue)
        return link_list # return a list of all issue links
    
    # function to click in the issue
    def click_issue(self):
        element_date_issue_click = self.driver.find_element(By.CLASS_NAME, self.date_journal)
        element_date_issue_click.click()       

    #function to get all article links and return a list
    def get_all_articles(self):
        element_page_articles = self.driver.find_element(By.CLASS_NAME, self.page_articles)
        element_box_articles = element_page_articles.find_element(By.CLASS_NAME, self.box_articles)            
        elements_list_articles = element_box_articles.find_elements(By.CLASS_NAME, self.list_articles)
        link_list = []
        for element_list_article in elements_list_articles:
            element_id_article = element_list_article.find_element(By.CSS_SELECTOR, self.article_title_id)
            element_link_article = element_id_article.get_attribute(self.article_link)
            link_list.append(element_link_article)
        return link_list

    #def open_text(self):
    #    element_article_title_id = self.driver.find_element(By.CSS_SELECTOR, self.article_title_id)
    #    element_article_link = element_article_title_id.get_attribute(article_link)
    #    element_article_title_id.click()

    def get_text_information(self): 
        text_information = []
        element_box_info_text = self.driver.find_element(By.CLASS_NAME, self.box_info_text)
        try:
            element_number_journal = element_box_info_text.find_element(By.CSS_SELECTOR, self.number_journal).text 
        except NoSuchElementException:
            element_number_journal = " Number of Journal not available"  
        try:
            element_author_text = element_box_info_text.find_element(By.CLASS_NAME, self.author_text).text
        except NoSuchElementException:
            element_author_text = " Author name is not available"
        try:
            element_doi_text = element_box_info_text.find_element(By.CLASS_NAME, self.doi_text).text
        except NoSuchElementException:
            element_doi_text = "  DOI of the text is not available"
        try:
            element_abstract_text = element_box_info_text.find_element(By.CSS_SELECTOR, self.abstract_text).text
        except NoSuchElementException:
            element_abstract_text = "  Abstract is not available"
        text_information = [element_number_journal, element_author_text, element_doi_text, element_abstract_text]
        return text_information
        

    def save_text_information(self):
        text_information = self.get_text_information()
        list_text_information = text_information.copy()
        list_text_information.append(text_information)
        if not os.path.exists("Aceno"):
            os.makedirs("Aceno")
        with open("aceno_texts.csv", "a", newline='') as file:
            writer = csv.writer(file) 
            writer.writerow(list_text_information)
            writer.writerow(" ")
            file.close()
        


    def to_iterate(self):
        self.navegate()
        element_all_issues = self.get_all_issues()
        for idx in range(len(element_all_issues)):
            self.driver.get(element_all_issues[idx])
            self.click_issue()
            link_articles = self.get_all_articles()
            for idx in range(len(link_articles)):
                self.driver.get(link_articles[idx])
                self.save_text_information()

        print("It's done!")

ff = webdriver.Firefox()
a = Aceno(ff) 
a.to_iterate()
ff.quit() 
