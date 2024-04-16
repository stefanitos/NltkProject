from newspaper import Article, Config

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0'
urls = [
    "https://www.timesofmalta.com/article/km-malta-airlines-drops-maltese-requirement-due-80-passengers-foreign.1090251",
    "https://www.maltatoday.com.mt/news/national/128415/revealed_transport_malta_officials_at_centre_of_maritime_fines_corruption_racket_",
    "https://www.independent.com.mt/articles/2024-03-31/local-news/A-look-back-Air-Malta-shuts-down-after-years-of-turbulence-6736259853",
    "https://www.lovinmalta.com/opinion/survey/survey-do-you-think-maltas-party-owned-tv-stations-should-be-shut-down/",
    "https://www.tvmnews.mt/en/news/unemployment-up-by-55-during-february-totaled-1096/",
    "https://theshiftnews.com/2024/03/06/disinformation-watch-framing-the-sofia-public-inquiry-narrative/",
]

config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10

for url in urls:
    article = Article(url, config=config)
    article.download()
    article.parse()
    text = article.text
    title = article.title
    print(title)
    print("/\/\/\/\ ")
    print(text)
    print("--------------------------------------------------")

