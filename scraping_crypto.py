from bs4 import BeautifulSoup
import requests
import pandas as pd

name = []
symbol = []
price = []
change_24h = []
value_24h = []
market_cap = []

for i in range(1, 11):
    # website
    website = 'https://crypto.com/price/pl?page=' + str(i)

    # request to website
    response = requests.get(website)

    # soup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # results
    results = soup.find('table', {'class': 'css-1qpk7f7'}).find('tbody').find_all('tr')

    # extract values from website
    for result in results:
        # Name
        try:
            name.append(result.find('p', {'class': 'css-rkws3'}).get_text())
        except:
            name.append('n/a')

        # Symbol
        try:
            symbol.append(result.find('span', {'class': 'css-1jj7b1a'}).get_text())
        except:
            symbol.append('n/a')

        # Price
        try:
            price.append(result.find('p', {'class': 'css-13hqrwd'}).get_text())
        except:
            price.append('n/a')

        # Change 24h
        try:
            td_element = result.find('td', {'class': 'css-vtw5vj'})

            # Check for both 'css-dg4gux' and 'css-yyku61' classes
            p_element = None
            for class_name in ['css-dg4gux', 'css-yyku61']:
                p_element = td_element.find('p', {'class': class_name})
                if p_element:
                    break

            # Append and print the text if the paragraph is found
            if p_element:
                change_24h.append(p_element.get_text())

            else:
                print("Paragraph with class 'css-dg4gux' or 'css-yyku61' not found")

        except:
            change_24h.append('n/a')

        # Value 24h
        try:
            caps_value = result.find_all('td', {'class': 'css-15lyn3l'})
            caps_text = [td.get_text(strip=True) for td in caps_value]
            value_24h.append(caps_text[0])
        except:
            value_24h.append('n/a')

        # Market Cap
        try:
            caps_value = result.find_all('td', {'class': 'css-15lyn3l'})
            caps_text = [td.get_text(strip=True) for td in caps_value]
            market_cap.append(caps_text[1])
        except:
            market_cap.append('n/a')


# create DataFrame
crypto_df = pd.DataFrame({'Coin_name': name, 'Symbol': symbol, 'Price': price, 'Change_24h': change_24h, 'Value_24h': value_24h, 'Market_Cap': market_cap})

# set display options to see all columns
pd.set_option('display.max_columns', None)
# print(crypto_df)


# export DataFrame to Excel file
crypto_df.to_excel('crypto_list.xlsx', index=False)
print('--------------------------------------------')
print('Export to Excel file completed successfully.')
print('--------------------------------------------')
