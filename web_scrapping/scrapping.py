
import requests
import re
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

def vacancys_search(main_soup, list):
     main_content = main_soup.find("div", id="a11y-main-content")
     vacancys_info = main_content.find_all("div", class_="vacancy-serp-item-body__main-info")

     for vacancy_info in vacancys_info:
          vacancy_tag = vacancy_info.find("h3")
          v_tag = vacancy_tag.find("a")
          link = v_tag['href']
          
          
          article_vacancy = requests.get(link, headers=headers_gen.generate()).text
          article_full_soup = BeautifulSoup(article_vacancy, "lxml")

          article_full_tag = article_full_soup.find("div", id="HH-React-Root")
          
          content = article_full_tag.find('div', class_="g-user-content")
          if content!=None:
               content_text = content.text

               if re.findall(r'Django|Flask', content_text) != []:

                    vacancy_title = article_full_tag.find('div', class_="vacancy-title")
                    section_salary = vacancy_title.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite")
                    if section_salary==None:
                         section_salar_text = "Не указана"
                    else:      
                         section_salar_text = section_salary.text 
                    salar_text = section_salar_text

                    company_details = article_full_tag.find('div', class_="vacancy-company-details")
                    company = company_details.find("span", class_="bloko-header-section-2 bloko-header-section-2_lite")  
                    company_text = company.text
                              
                    city_company = article_full_tag.find('div', class_="vacancy-company-redesigned")
                    city = city_company.find("p")
                    if city!=None:
                         city_text = city.text
                    else:
                         city_company_teg=city_company.find("a", class_="bloko-link bloko-link_kind-tertiary bloko-link_disable-visited")
                         city_text = city_company_teg.text 
                              
                    vacancys.append({
                              "link": link,
                              "salary": salar_text,
                              "company": company_text,
                              "city": city_text,})
     return list




headers_gen = Headers(os="win", browser="chrome")

base_url = "https://spb.hh.ru/search/vacancy?area=1&area=2&ored_clusters=true&text=python&search_period=1"

  
main_habr = requests.get(base_url, headers=headers_gen.generate())
main_habr_html = main_habr.text
main_soup = BeautifulSoup(main_habr_html, "lxml")
    
vacancys = []

vacancys1 = vacancys_search(main_soup, vacancys)

pager = main_soup.find('div', class_="pager")
pager2=pager.find("a", class_="bloko-button")
pager_text = pager2.text 
for page in range(1, int(pager_text)+1):
     current_url = base_url + f"&page={page}" 
     main_habr2 = requests.get(current_url, headers=headers_gen.generate())
     main_habr_html2 = main_habr2.text
     main_soup2 = BeautifulSoup(main_habr_html, "lxml")
     vacancys2 = vacancys_search(main_soup2, vacancys1)

     
with open('vacancys.json', 'w', encoding='utf-8') as file:
     json.dump(vacancys2, file, ensure_ascii=False, indent=4)


          
     
          