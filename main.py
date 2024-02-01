import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


base_url = 'https://www.google.com/maps/search/'
categories = ['restaurants', 'hotels','medicals','petrol pump','peter england']  

work= Workbook()
ws = work.active
ws.append(['Name', 'Address', 'Phone', 'Website', 'Category','description'])


def scrape_gmb(category):
    url = base_url + category
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
   
    business_list = soup.find_all('div', class_='section-result-content')
    for business in business_list:
        name = business.find('h3').text.strip()
        
        address_tag = business.find('span', class_='section-result-location')
        address = address_tag.text.strip() if address_tag else ''
        
        phone_tag = business.find('span', class_='section-result-phone-number')
        phone = phone_tag.text.strip() if phone_tag else ''
        
        website_tag = business.find('div', class_='section-result-website')
        website = website_tag.a['href'].strip() if website_tag and website_tag.a else ''
        
        ws.append([name, address, phone, website, category])

# Main function to loop through categories and scrape data
def main():
    for category in categories:
        scrape_gmb(category)

    # Save the Excel file
    work.save("local_business_details.xlsx")

if __name__ == '__main__':
    main()
