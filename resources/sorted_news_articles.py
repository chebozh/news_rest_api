from flask_restful import Resource

from models.news_article import NewsArticleModel


class NewsArticlesSortedByDate(Resource):
    def get(self):
        return {
            'news_articles': [news_article.json() for news_article in NewsArticleModel.get_all_sorted_by_date()]
        }


class NewsArticlesSortedByTitle(Resource):
    def get(self):
        return {
            'news_articles': [news_article.json() for news_article in NewsArticleModel.get_all_sorted_by_title()]
        }


class NewsArticlesSortedByDateAndTitle(Resource):
    def get(self):
        return {
            'news_articles': [news_article.json() for news_article in
                              NewsArticleModel.get_all_sorted_by_date_and_title()]
        }
