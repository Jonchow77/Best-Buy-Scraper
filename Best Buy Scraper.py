import requests, re, csv
from bs4 import BeautifulSoup
from collections import Counter

#Parses user input to correct query string format
def parseInput(mystring):
    # Removing extra spaces (if any)
    mystring = mystring.strip()
    while '  ' in mystring:
        mystring = mystring.replace('  ', ' ')
    return mystring.replace(' ', '%20')

list_brands = []
list_avg_rating = []
list_num_ratings = []
front_url = "https://www.bestbuy.com/site/searchpage.jsp?cp="
page_count = 1
middle_url = "&searchType=search&st="
user_input = parseInput(input("Enter search term please:"))
search_term = user_input
end_url = "&_dyncharset=UTF-8&id=pcat17071&type=page&sc=Global&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All%20Categories&ks=960&keys=keys"
url = front_url + str(page_count) + middle_url + search_term + end_url
print(url)
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

#While the next page exists:
while True:
    page = requests.get(url, headers=agent)
    soup = BeautifulSoup(page.text, 'html.parser')
    print('Page ' + str(page_count))

    #All results are stored in a div called list-items
    #Each individual result is stored in a div called "list-item"

    #Putting all brands into list
    for brand in soup.find_all(True, {'class': ['sku-title']}):
        if 'New' in brand.text:
            list_brands.append(brand.text[5:brand.text.find('-') - 1])
        else:
            list_brands.append(brand.text[:brand.text.find(" ")])

    #Putting all ratings and number of ratings into list
    for thing in soup.find_all(True, {'class': ['c-review-average', 'c-total-reviews', 'c-reviews-none']}):
        if '(' in thing.text:
            list_num_ratings.append(int(thing.text[1:-1].replace(',', '')))
        elif 'Not Yet' in thing.text:
            list_avg_rating.append(None)
            list_num_ratings.append(0)
        else:
            list_avg_rating.append(float(thing.text))
    
    page_count += 1 

    #Checks if the next page of results exists
    if soup.find(class_="pager-next") is None:
        break
    elif soup.find(class_="pager-next").find('a')['href']:
        url = front_url + str(page_count) + middle_url + search_term + end_url
    else:
        break
    

#Inputting into csv file
with open('data.csv', 'w', newline='') as mycsv:
    writer = csv.writer(mycsv)
    writer.writerow(list_brands)
    writer.writerow(list_avg_rating)
    writer.writerow(list_num_ratings)
    dict_writer = csv.DictWriter(mycsv, Counter(list_brands).keys())
    dict_writer.writeheader()
    dict_writer.writerow(Counter(list_brands))

