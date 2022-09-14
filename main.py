"""This code scraps the information about articles published in Revista aceno,saves this information and returns a csv file"""

import csv
import os
from datetime import datetime

import wget
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

__authors__ = ["Nádia dos Santos Ossenkop, Eric Brasil"]
___copyleft___ = "Freedom 4"
__emails__ = ["nadia.aguiar@hotmail.com, ericbrasiln@protonmail.com"]

class Aceno:
    """function with the variables"""
    def __init__(self, driver):
        self.driver = driver
    
        self.url = "https://periodicoscientificos.ufmt.br/ojs/index.php/aceno/issue/archive"
        self.issue = "obj_issue_summary" #class
        self.date_issue = "title" # class
        self.issue_link = "href" # attribute

        self.list_articles = "obj_article_summary"# class  
        self.article_title_id = "[id^='article-']" #CSS Selector
        self.article_link = "href" #attribute

        self.box_info_text = "obj_article_details" #class
        self.number_issue = "a.title" #CSS Selector
        self.author_text = "authors" #class
        self.doi_text = "item.doi" #class
        self.abstract_text = "html body.pkp_page_article.pkp_op_view div.pkp_structure_page div.pkp_structure_content.has_sidebar div.pkp_structure_main div.page.page_article article.obj_article_details div.row div.main_entry section.item.abstract p" #CSS Selector
        self.abstract_title = "page_title" #class

        self.return_page_article = "/html/body/div[1]/div[1]/div[1]/div/article/div/div[2]/div[4]/section[1]/div/a" #XPATH
        self.box_next_page = "/html/body/div/div[1]/div[1]/div/div" #XPATH
        self.next_page = "next" #class

        self.pdf_article = ".obj_galley_link" #css
        self.pdf_url ="href" #attribute

    """function to open the link of the journal Aceno"""
    def navegate (self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)
        self.driver.get(self.url)
        print ("The party, ops Browser was started" )


    """function to get list of all issue links and return a list"""
    def get_all_issues(self):
        element_all_issues = self.driver.find_elements(By.CLASS_NAME, self.issue)
        link_list = []
        for element_issue in element_all_issues:
            element_issue_title = element_issue.find_element(By.CLASS_NAME, self.date_issue)
            element_link_issue = element_issue_title.get_attribute(self.issue_link)
            link_list.append(element_link_issue)
        return link_list 
    

    """function to click in the issue"""
    def click_issue(self):
        element_date_issue_click = self.driver.find_element(By.CLASS_NAME, self.date_issue)
        element_date_issue_click.click()       


    """function to get all article links and return a list"""
    def get_all_articles(self):
        elements_list_articles = self.driver.find_elements(By.CLASS_NAME, self.list_articles)
        link_list = []
        for element_list_article in elements_list_articles:
            element_id_article = element_list_article.find_element(By.CSS_SELECTOR, self.article_title_id)
            element_link_article = element_id_article.get_attribute(self.article_link)
            link_list.append(element_link_article)
        return link_list


    """function to get all information about the article and return a list"""
    def get_text_information(self): 
        element_box_info_text = self.driver.find_element(By.CLASS_NAME, self.box_info_text)
        try:
            element_number_issue = element_box_info_text.find_element(By.CSS_SELECTOR, self.number_issue).text 
        except NoSuchElementException:
            element_number_issue = " Number of issue not available."  
        try:
            element_author_text = element_box_info_text.find_element(By.CLASS_NAME, self.author_text).text
        except NoSuchElementException:
            element_author_text = " Author name is not available."
        try:
            element_doi_text = element_box_info_text.find_element(By.CLASS_NAME, self.doi_text).text
        except NoSuchElementException:
            element_doi_text = "  DOI of the text is not available."
        try:
            element_abstract_text = element_box_info_text.find_element(By.CSS_SELECTOR, self.abstract_text).text
        except NoSuchElementException:
            element_abstract_text = "  Abstract is not available."
        try:
            element_abstract_title = element_box_info_text.find_element (By.CLASS_NAME, self.abstract_title).text
        except NoSuchElementException:
            element_abstract_title = "Title is not available."
        
        text_information = [element_number_issue, element_author_text, element_doi_text, element_abstract_title, element_abstract_text]
        return text_information


    """function to save all article's information and return a csv file"""
    def save_text_information(self):
        text_information = self.get_text_information()
        dir = "aceno/texts"
        file_name = "aceno_texts.csv"
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(os.path.join(dir, file_name), "a", newline='') as file:
            writer = csv.writer(file) 
            writer.writerow(text_information)
            writer.writerow(" ")
            file.close()


    """function to save all informations and return a PDF file"""
    def save_files_pdf(self):
        element_box_info_text = self.driver.find_element(By.CLASS_NAME, self.box_info_text)
        element_pdf_link_article = element_box_info_text.find_element(By.CSS_SELECTOR, self.pdf_article)
        element_pdf_url = element_pdf_link_article.get_attribute("href")
        dir = "aceno/pdf"
        if not os.path.exists(dir):
            os.makedirs(dir)
        try:            
            wget.download(element_pdf_url, os.path.join(dir, wget.filename_from_url(element_pdf_url)))
        except NoSuchElementException:
            pass


    """function to go to the next page, if one exists"""
    def click_next_page (self):       
        try:
            element_box_next_page = self.driver.find_element(By.XPATH, self.box_next_page) 
            element_next_page = element_box_next_page.find_element(By.CLASS_NAME, self.next_page)
            element_next_page.click()
            self.url = self.driver.current_url
            self.to_iterate()
        except NoSuchElementException:
            print("That's all folks!")
     

    """function to iterate overall issues and articles"""
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
        self.driver.get(self.url)
        self.click_next_page()


    """function to iterate overall issues and articles and return a PDF file"""
    def to_iterate_pdf(self):
        self.navegate()
        element_all_issues = self.get_all_issues()
        for idx in range(len(element_all_issues)):
            self.driver.get(element_all_issues[idx])
            self.click_issue()
            link_articles = self.get_all_articles()
            for idx in range(len(link_articles)):
                self.driver.get(link_articles[idx])
                self.save_files_pdf()
        self.driver.get(self.url)
        self.click_next_page()


    """function to ask to user to save PDF's or not"""
    def pdf_or_no(self):
        pdf_or_no =" "
        while pdf_or_no != "pdf" or pdf_or_no != "no":
            pdf_or_no = input("Do you want to download the PDF files or not? (pdf or no): ").lower()
            if pdf_or_no == "no":
                self.to_iterate()
            else:
                self.to_iterate_pdf()

    """function to report the moment of the search and return a txt file"""
    def to_report(self):
        now = datetime.now()
        current_time = now.strftime("%D %H:%M:%S")
        dir = "aceno/reports"
        file_name = "aceno_report.txt"
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(os.path.join(dir,file_name), "a", newline='') as file:
            file.write (f"This search was made in {current_time}\n")
            file.close()
    
        
ff = webdriver.FirefoxOptions()
a = Aceno(ff)
a.pdf_or_no()
a.to_report() 
ff.quit()

