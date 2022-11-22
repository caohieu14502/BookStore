from sqlalchemy import Column, Float, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from bookstore import db, app


class BaseModel(db.Model):
    __abstract__ =True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Genre(BaseModel):
    __tablename__ = 'genre'

    name = Column(String(20), nullable=False)
    sachs= relationship('Book', backref='genre', lazy=True)

    def __str__(self):
        return self.name

class Book(BaseModel):
    __tablename__ = 'book'

    name = Column(String(40), nullable=False)
    author = Column(String(100))
    price = Column(Float, default=0)
    image = Column(String(200))
    active = Column(Boolean, default=True)
    pubic_year = Column(Integer)
    theloai_id = Column(Integer, ForeignKey(Genre.id), nullable=False)

    def __str__(self):
        return self.name


# with app.app_context():
#     if __name__ == '__main__':
        #db.create_all()

        # t1= Genre(name='Tâm lý')
        # t2= Genre(name='Trinh thám')
        # t3= Genre(name='Tiểu thuyết')
        # t4= Genre(name='Kĩ năng')
        # t5= Genre(name='Khoa học')
        #
        # db.session.add(t1)
        # db.session.add(t2)
        # db.session.add(t3)
        # db.session.add(t4)
        # db.session.add(t5)



        # for s in booklist:
        #     sach = Book(name=s['name'], author=s['description'], price=s['price'], image=s['image'], theloai_id=s['category_id'])
        #
        #     db.session.add(sach)
        #
        # db.session.commit()

