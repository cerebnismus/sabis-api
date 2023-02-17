# This project aims to provide a simple news feed reader 
# Sakarya University Computer Science Department.

from bs4 import BeautifulSoup
import requests

# Get the news feed from the Sakarya University Computer Science Department website.
url = "https://cs.sakarya.edu.tr/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Get the news feed from the Sakarya University Computer Science Department website.
title_strings = soup.find_all("h5", {"class": "blog-list-title"})

# Get the news feed from the Sakarya University Computer Science Department website.
title_detail_strings = soup.find_all("p", {"class": "blog-list-meta small-text"})

# Get the news feed from the Sakarya University Computer Science Department website.
title_date_strings = soup.find_all("div", {"class": "calendar-haber"})


# print the news feed. title and title detail.
print('SAU HABERLER')
print('-'*64)
for i in range(4):
		print(title_date_strings[i].text, title_strings[i].text)
		print(title_detail_strings[i].text)
		print()
  
# print the announcements feed. title and title detail. from 4 to 9.
print('SAU DUYURULAR')
print('-'*64)
for i in range(4, 9):
		print(title_date_strings[i].text, title_strings[i].text)
		print(title_detail_strings[i].text)
		print()
  
# Output:
# 2022-2023 Eğitim-Öğretim Yılı