from db import db


class NewsArticleModel(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date())
    title = db.Column(db.String())
    description = db.Column(db.String())
    text = db.Column(db.Text())

    def __init__(self, date, title, description, text):
        self.date = date
        self.title = title
        self.description = description
        self.text = text

    def json(self):
        return {
            'id': self.id,
            'date': self.date.strftime("%d-%m-%Y"),
            'title': self.title,
            'description': self.description,
            'text': self.text,
        }

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).all()

    @classmethod
    def find_by_date_and_title(cls, date, title):
        return cls.query.filter_by(date=date, title=title).first()

    @classmethod
    def get_all_sorted_by_date(cls):
        return cls.query.order_by(cls.date.desc()).all()

    @classmethod
    def get_all_sorted_by_title(cls):
        return cls.query.order_by(cls.title).all()

    @classmethod
    def get_all_sorted_by_date_and_title(cls):
        return cls.query.order_by(cls.date.desc(), cls.title).all()

    @classmethod
    def delete_from_db_by_date(cls, date):
        bukl_delete_q = cls.__table__.delete().where(cls.date == date)
        db.session.execute(bukl_delete_q)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
