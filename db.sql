Create Table Books
(
    book_id      int primary key,
    title        text not null,
    ISBN         int unique,
    url          text unique,
    organisation int references Organisation (organisation_id),
    magazines    int references Magazines (magazine_id),
    language     text,
    page_count   int,
    date         date,
    annotation   text not null ,
    price        int
);

Create Table Magazines
(
    magazine_id int primary key,
    name        text unique not null
);

Create Table Organisation
(
    organisation_id int primary key,
    name            text unique not null,
    country         text
);

Create Table BookQuotes
(
    quote_id    int primary key,
    ref_book    int references Books (book_id),
    in_ref_book int references Books (book_id)
);

Create Table Authors
(
    author_id    int primary key,
    name         text not null,
    surname      text not null,
    organisation int references Organisation (organisation_id),
    country      text
);

Create Table BookAuthors
(
    book_id   int references Books (book_id),
    author_id int references Authors (author_id),
    primary key (book_id, author_id)
);

Create Table Keywords
(
    keyword_id int primary key,
    keyword    text not null
);

Create Table BookKeywords
(
    book_id    int references Books (book_id),
    keyword_id int references Keywords (keyword_id),
    primary key (book_id, keyword_id)
);

Create Table Users
(
    user_id            int primary key,
    login              varchar(10) unique not null,
    password           varchar(16) not null,
    email              text unique,
    confirmed_email    boolean,
    owned_publications int references UsersBooks (book_id)
);

Create Table UsersBooks
(
    book_id references Books (book_id),
    user_id references Users (user_id),
    state text check (state in ('paid', 'not paid')) default 'not paid',
    primary key (book_id, user_id)
);

Select distinct * from Books join UsersBooks ON Books.book_id == UsersBooks.book_id JOIN Users ON UsersBooks.user_id == Users.user_id;
Select * from Books join BookQuotes on Books.book_id == BookQuotes.ref_book where BookQuotes.in_ref_book == 3;
Select * from Authors join Organisation on Authors.organisation = Organisation.organisation_id where Organisation.name == 'Organisation 1';
Select DISTINCT Books.book_id from Books join BookAuthors on BookAuthors.author_id == 2;
SELECT DISTINCT Authors.author_id, Authors.name, Authors.surname, Authors.organisation, Authors.country from Authors join BookAuthors on BookAuthors.book_id in (Select Books.book_id from Books join BookAuthors on BookAuthors.author_id == 2) WHERE Authors.author_id != 2;

INSERT INTO Books (book_id, title, ISBN, url, organisation, magazines, language, page_count, date, annotation, price) VALUES
(1, 'Book 1', 1234567890, 'https://www.book1.com', 1, NULL, 'English', 300, '2023-01-01', 'Annotation 1', 20),
(2, 'Book 2', 2345678901, 'https://www.book2.com', 2, NULL, 'English', 250, '2023-02-01', 'Annotation 2', 25),
(3, 'Book 3', 3456789012, 'https://www.book3.com', NULL, NULL, 'Spanish', 200, '2023-03-01', 'Annotation 3', 30);

INSERT INTO Magazines (magazine_id, name) VALUES
(1, 'Magazine 1'),
(2, 'Magazine 2');

INSERT INTO Organisation (organisation_id, name, country) VALUES
(1, 'Organisation 1', 'USA'),
(2, 'Organisation 2', 'UK');

INSERT INTO BookQuotes (quote_id, ref_book, in_ref_book) VALUES
(1, 1, 2),
(2, 1, 3),
(3, 2, 3);

INSERT INTO Authors (author_id, name, surname, organisation, country) VALUES
(1, 'Author 1', 'Surname 1', 1, 'USA'),
(2, 'Author 2', 'Surname 2', 2, 'UK');

INSERT INTO BookAuthors (book_id, author_id) VALUES
(1, 1),
(1, 2),
(2, 2),
(3, 1),
(3, 2);

INSERT INTO Keywords (keyword_id, keyword) VALUES
(1, 'Keyword 1'),
(2, 'Keyword 2');

INSERT INTO BookKeywords (book_id, keyword_id) VALUES
(1, 1),
(1, 2),
(2, 1),
(3, 2);

INSERT INTO Users (user_id, login, password, email, confirmed_email, owned_publications) VALUES
(1, 'user1', 'password1', 'user1@example.com', true, 1),
(2, 'user2', 'password2', 'user2@example.com', false, 2);

INSERT INTO UsersBooks (book_id, user_id, state) VALUES
(1, 1, 'paid'),
(2, 1, 'not paid'),
(3, 2, 'paid');
