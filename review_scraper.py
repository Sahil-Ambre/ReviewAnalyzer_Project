from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
import datetime
import dateutil.relativedelta



def get_df(page):
    names = []
    review_titles = []
    ratings = []
    dates = []
    reviews = []

    u = 0

    for n in range(1,101):
        # url maker
        product_url1 = page.replace("/p/","/product-reviews/")
        product_url_split = product_url1.split("?")
        product_url2 = product_url_split[0]
        product_url3 = product_url_split[1].split("&")[0]
        product_url_final = f"{product_url2}?{product_url3}&page={n}"
        
        # get soup
        r = requests.get(product_url_final)    
        soup = bs(r.content, 'html.parser')
        
        rows = soup.find_all('div',attrs={'class':'col _2wzgFH K0kLPL'})
        
        
        
        
        if len(rows) > 0:
            # get data from soup
            for row in rows:

                # finding all rows within the block
                sub_row = row.find_all('div',attrs={'class':'row'})

                # extracting text from 1st and 2nd row
                rating = sub_row[0].find('div').text
                summary = sub_row[0].find('p').text
                review = sub_row[1].find_all('div')[2].text
                date = sub_row[3].find_all('p',attrs={'class':'_2sc7ZR'})[1].text
                
                u += 1
                names.append(f"User{u}")
                review_titles.append(summary)
                ratings.append(int(rating))
                dates.append(date)
                reviews.append(review)

        else:
            break
            
    data_dict = {"Name": names, 
                "Review_Title": review_titles, 
                "Rating": ratings, 
                "Date": dates, 
                "Review_content": reviews}
    df = pd.DataFrame(data_dict)

    def date_fix(x):
        splitted_date = x.split(" ")
        d = datetime.datetime.today()
        if len(splitted_date) > 2:
            period_freq = splitted_date[1].replace("s", "")
            actual_period = int(splitted_date[0])
    #         print(period_freq)
            if period_freq == "month":
                d2 = d - dateutil.relativedelta.relativedelta(months=actual_period)
                return d2.strftime('%m-%d-%Y')
            if period_freq == "day":
                d2 = d - dateutil.relativedelta.relativedelta(days=actual_period)
                return d2.strftime('%m-%d-%Y')
        elif len(splitted_date) == 2:
            d2 = datetime.datetime.strptime(x, '%b, %Y')
            return d2.strftime('%m-%d-%Y')
    df["Date"] = df["Date"].apply(lambda x: date_fix(x))

    return df









