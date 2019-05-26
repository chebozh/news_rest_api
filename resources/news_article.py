import datetime

from flask import request
from flask_restful import Resource, reqparse

from models.news_article import NewsArticleModel


class NewsArticle(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('date',
                        type=str,
                        required=False,
                        help="Add a date with strict format of <day-month-year>."
                        )
    parser.add_argument('title',
                        type=str,
                        required=False,
                        help="Add article title."
                        )
    parser.add_argument('description',
                        type=str,
                        required=False,
                        help="Add a short description of the article."
                        )
    parser.add_argument('text',
                        type=str,
                        required=False,
                        help="Add article text."
                        )

    def get(self):
        """Method to retrieve one or many articles, depending on
        the URL query params.
        :return: JSON (or list of JSON) of an article(s).
        """
        date_query_param = request.args.get('date', '')
        date_query_param = self.to_date(date_query_param) if date_query_param else ''
        title_query_param = request.args.get('title', '')

        # find article by date and title
        if date_query_param and title_query_param:
            news_article = NewsArticleModel.find_by_date_and_title(date_query_param, title_query_param)
            return news_article.json()
        # find article(s) by date only
        elif date_query_param and not title_query_param:
            news_articles = NewsArticleModel.find_by_date(date_query_param)
            return {
                'news_articles': [news_article.json() for news_article in news_articles]
            }
        # find articles by title only
        elif title_query_param and not date_query_param:
            news_article = NewsArticleModel.find_by_title(title_query_param)
            return news_article.json()
        else:
            return {'message': 'Article not found'}, 404

    def post(self):
        """Method to create a new article resource.
        """
        news_article_data = self.parser.parse_args()
        news_title = news_article_data['title']

        if NewsArticleModel.find_by_title(news_title):
            return {'message': f'An article with name "{news_title}" already exists.'}

        news_article = NewsArticleModel(
            date=self.to_date(news_article_data['date']),
            title=news_article_data['title'],
            description=news_article_data['description'],
            text=news_article_data['text']
        )

        try:
            news_article.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the article.\n {e}"}

        return news_article.json(), 201

    def put(self):
        """Method to create a new article or modify an existing one.
        The article to be modified is found by its title or id,
        either of which is required as a url query param.
        """
        title_request_param = request.args.get('title', '')
        id_request_param = request.args.get('id', '')
        data = self.parser.parse_args()

        # find article by title only
        if title_request_param and not id_request_param:
            news_article = NewsArticleModel.find_by_title(title_request_param)
        # find article by id only
        elif id_request_param and not title_request_param:
            news_article = NewsArticleModel.find_by_id(id_request_param)
        # find article by title and id
        elif id_request_param and title_request_param:
            news_article = NewsArticleModel.find_by_id(id_request_param)
        else:
            return {'message': 'Add title or id query param of the article to modify'}, 404

        if news_article is None:
            # if the article doesn't exist, create it
            news_article = NewsArticleModel(
                date=self.to_date(data['date']),
                title=data['title'],
                description=data['description'],
                text=data['text']
            )
        else:
            # modify the article with the data from the PUT's body(json)
            for attribute, value in dict(data).items():
                if value is not None:
                    if attribute == 'date':
                        setattr(news_article, attribute, self.to_date(value))
                    else:
                        setattr(news_article, attribute, value)

        news_article.save_to_db()
        return news_article.json(), 200

    def delete(self):
        """Delete a new article using it's title or its id,
        which should be included in the url as query params.
        """
        date_query_param = request.args.get('date', '')
        title_query_param = request.args.get('title', '')
        id_query_param = request.args.get('id', '')

        if date_query_param:
            # delete one or more articles by date
            NewsArticleModel.delete_from_db_by_date(self.to_date(date_query_param))
            return {'message': 'Article(s) deleted.'}, 200

        # delete article by id
        if id_query_param and not title_query_param:
            article = NewsArticleModel.find_by_id(id_query_param)
        # delete article by title
        elif title_query_param and not id_query_param:
            article = NewsArticleModel.find_by_title(title_query_param)
        else:
            return {'message': 'Add title or id query param'}, 404

        if article:
            article.delete_from_db()
            return {'message': 'Article deleted.'}, 200
        else:
            return {'message': 'Article not found'}, 404

    @staticmethod
    def to_date(date_string):
        """Method to transform JSON string field into date object.
        :param date_string: string in format dd-mm-yyyy
        :return: datetime.date object
        """
        return datetime.datetime.strptime(date_string, "%d-%m-%Y").date()
