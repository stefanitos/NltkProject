from newspaper import Article

# url = 'https://timesofmalta.com/article/km-malta-airlines-drops-maltese-requirement-due-80-passengers-foreign.1090251'
url = 'https://www.maltatoday.com.mt/news/national/128415/revealed_transport_malta_officials_at_centre_of_maritime_fines_corruption_racket_'
article = Article(url)
article.download()
article.parse()

print(article.text)