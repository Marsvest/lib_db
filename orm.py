from peewee import *
from mimesis import *
import random
from username import *

conn = SqliteDatabase('C:\\Users\\mrart\\DataGripProjects\\test\\identifier.sqlite')


class BaseModel(Model):
    class Meta:
        database = conn


class Organisation(BaseModel):
    organisation_id = AutoField(column_name='organisation_id')
    name = TextField(column_name='name', null=False, unique=True)
    country = TextField(column_name='country', null=False)


class Magazines(BaseModel):
    magazine_id = AutoField(column_name='magazine_id')
    name = TextField(column_name='name', null=False, unique=True)


class Books(BaseModel):
    book_id = AutoField(column_name='book_id', unique=True)
    title = TextField(column_name='title', null=False)
    ISBN = IntegerField(column_name='ISBN', unique=True, primary_key=False)
    url = TextField(column_name='url', unique=True)
    organisation = ForeignKeyField(Organisation, backref='books')
    magazines = ForeignKeyField(Magazines, backref='books')
    language = TextField(column_name='language')
    page_count = IntegerField(column_name='page_count', null=False)
    date = DateTimeField(column_name='date', null=False)
    annotation = TextField(column_name='annotation')
    price = IntegerField(column_name='price')


class Authors(BaseModel):
    author_id = AutoField(column_name='author_id')
    name = TextField(column_name='name', null=False)
    surname = TextField(column_name='surname', null=False)
    organisation = ForeignKeyField(Organisation, backref='authors')
    country = TextField(column_name='country')


class Keywords(BaseModel):
    keyword_id = AutoField(column_name='keyword_id')
    keyword = TextField(column_name='keyword')
    book = ForeignKeyField(Books, backref='keywords')


class Users(BaseModel):
    user_id = AutoField(column_name='user_id')
    login = TextField(column_name='login', null=False, unique=True)
    password = TextField(column_name='password', null=False)
    email = TextField(column_name='email', null=False)
    confirmed_email = BitField(column_name='confirmed_email', default=0)


class BookAuthors(BaseModel):
    book_id = ForeignKeyField(Books)
    author_id = ForeignKeyField(Authors)

    class Meta:
        primary_key = CompositeKey('book_id', 'author_id')


class BookQuotes(BaseModel):
    quote_id = AutoField(column_name='quote_id')
    ref_book = ForeignKeyField(Books, backref='ref_books')
    in_ref_book = ForeignKeyField(Books, backref='in_ref_book')


class BookKeywords(BareField):
    book_id = ForeignKeyField(Books, backref='books')
    keyword_id = ForeignKeyField(Keywords, backref='keywords')

    class Meta:
        primary_key = CompositeKey('book_id', 'keyword_id')


class UsersBooks(BaseModel):
    book_id = ForeignKeyField(Books, backref='books')
    user_id = ForeignKeyField(Users, backref='users')
    state = TextField(constraints=[Check("state in ('paid', 'not paid')")], default='not paid')

    class Meta:
        primary_key = CompositeKey('book_id', 'user_id')


book_titles = [
    "Загадочный код",
    "Программирование на пути к успеху",
    "Приключения программиста",
    "Магия алгоритмов",
    "Искусство Python",
    "Тайны мастерства программирования",
    "Кодер и проклятие Дракона",
    "Путеводитель по Python",
    "Секреты эффективного кодирования",
    "Приключения в виртуальной реальности",
    "Алгоритмы: от новичка до профессионала",
    "Искусство решения задач",
    "Приключения в мире байтов",
    "Python: От новичка к эксперту",
    "Тайны хакера",
    "Программисты и драконы",
    "Мир алгоритмов",
    "Приключения в цифровой реальности",
    "Искусство программирования",
    "Путешествие в мир Python"
]
science_magazines = ["Scientific American", "National Geographic",
                     "Discover", "New Scientist", "Popular Science",
                     "Science", "Nature", "Smithsonian", "Physics Today",
                     "Chemical & Engineering News"]
info = ['paid', 'not paid']
inf = Choice()
book_titles1 = Choice()
book_isbn = Code()
book_url = Internet()
organisation = Finance(locale=Locale.RU)
magazine = Choice()
language = Person()
book_date = Datetime()
annotation = Text(locale=Locale.RU)

org_country = Address()

author_name = Person(locale=Locale.RU)
author_sur = Person(locale=Locale.RU)
author_country = Address()

keyword = Text(locale=Locale.RU)

login = Person(locale=Locale.EN)
password = random.getrandbits(128)
email = Person()
email_conf = bool(random.getrandbits(1))

for i in range(5):
    org = Organisation.create(name=organisation.company(), country=org_country.country())
    mag = Magazines.create(name=magazine(science_magazines))
    book = Books.create(book_id=i, title=book_titles1(book_titles), ISBN=book_isbn.isbn(), url=book_url.url(),
                        organisation=org, magazines=mag, language=language.language(),
                        page_count=random.randint(15, 70), date=book_date.datetime(), annotation=annotation.text(),
                        price=random.randint(234, 3540))
    author = Authors.create(name=author_name.name(), surname=author_sur.surname(), organisation=org,
                            country=author_country.country())
    Keywords.create(keyword=keyword.word(), book=book)
    Keywords.create(keyword=keyword.word(), book=book)
    Keywords.create(keyword=keyword.word(), book=book)
    user = Users.create(login=login.username(), password=random.getrandbits(128), email=email.email(),
                        confirmed_email=bool(random.getrandbits(1)))
    BookAuthors.create(book_id=book, author_id=author)
    UsersBooks.create(book_id=book, user_id=user, state=inf(info))
