import tls_client
import bs4

class EasyQuote:
    def __init__(self,page=None,keyword=None,amount=1):
        if page != None and keyword != None:
            self.url = f'https://www.goodreads.com/quotes/search?commit=Search&page={{}}&q={{}}&utf8=%E2%9C%93'.format(str(page), keyword)
        elif keyword != None and page == None:
            self.url = f'https://www.goodreads.com/quotes/search?commit=Search&page=1&q={{}}&utf8=%E2%9C%93'.format(keyword)
        elif keyword == None and page != None:
            self.url = f'https://www.goodreads.com/quotes?page={{}}'.format(str(page))
        else:
            return 'Missing required easyquote-init params'
        
        self.amount = amount
        
        self.headers = {
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
        }
        self.session = tls_client.Session(
            client_identifier="safari_15_6_1"
        )

    def generate(self):
        parsed=[

        ]
        html = self.session.get(self.url,headers=self.headers).text
        quotes = bs4.BeautifulSoup(html, 'html.parser').find_all('div',class_='quoteText')

        i=0
        for quote in quotes:
            q = quote.get_text(strip=True).split('―')[0].strip('“”')
            if ',' in quote.get_text(strip=True).split('―')[1]:
                a = quote.get_text(strip=True).split('―')[1].split(',')[0]
            else:
                a = quote.get_text(strip=True).split('―')[1]
            parsed.append({
                'quote':q,
                'author':a
            })
            i+=1
            if i == self.amount:
                break
        return parsed
