import os

from flask import Flask
from flask_restful import Api

from resources.news_article import NewsArticle
from resources.sorted_news_articles import NewsArticlesSortedByDate, NewsArticlesSortedByTitle, \
    NewsArticlesSortedByDateAndTitle

app = Flask(__name__)
# use heroku PostgreSQL DB by default, and as a back-up the DB from elephantsql.com
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'postgres://chxbsfob:WnM3WwuOI6YyJShypSKP4rg3eDJNLgyq@manny.db.'
                                                       'elephantsql.com:5432/chxbsfob')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '25052019'
api = Api(app)

api.add_resource(NewsArticle, '/news')
api.add_resource(NewsArticlesSortedByDate, '/news/sorted_by_date')
api.add_resource(NewsArticlesSortedByTitle, '/news/sorted_by_title')
api.add_resource(NewsArticlesSortedByDateAndTitle, '/news/sorted_by_date_title')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=False)
