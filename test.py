from newspaper import Article


urls = ['https://timesofmalta.com/article/km-malta-airlines-drops-maltese-requirement-due-80-passengers-foreign.1090251',
        'https://www.maltatoday.com.mt/news/national/128415/revealed_transport_malta_officials_at_centre_of_maritime_fines_corruption_racket_',
        'https://www.independent.com.mt/articles/2024-03-31/local-news/A-look-back-Air-Malta-shuts-down-after-years-of-turbulence-6736259853',
        'https://lovinmalta.com/opinion/survey/survey-do-you-think-maltas-party-owned-tv-stations-should-be-shut-down/']

for url in urls:
    article = Article(url).download()
    article.parse()
    print(article.title)
    print(article.text)
    print('-------------------')
