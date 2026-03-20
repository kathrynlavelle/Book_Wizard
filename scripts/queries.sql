/* SQL Queries */

/* Retrieve the list of all books */
SELECT
    b.book_id,
    b.title,
    GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS author,
    b.published_year,
    b.price,
    MAX(i.quantity) AS inventory
FROM books b
LEFT JOIN inventory i ON b.book_id = i.book_id
LEFT JOIN book_author ba ON b.book_id = ba.book_id
LEFT JOIN authors a ON ba.author_id = a.author_id
GROUP BY
	b.book_id,
    b.title,
    b.published_year,
    b.price;


/* Add a new book to inventory */
-- Insert into books
INSERT INTO books (title, isbn, published_year, price, publisher_id)
VALUES ('What the Dog Saw', '978-0316084659', 2009, 29.99, 1);

-- Insert into inventory
INSERT INTO inventory (book_id, quantity, location)
SELECT book_id, 10, 'Warehouse A'
FROM books
WHERE title = 'What the Dog Saw' AND isbn = '978-0316084659';

-- If author doesn't exist, insert into authors
INSERT INTO authors (first_name, last_name, bio)
SELECT 'Malcolm', 'Gladwell', 'Author of "What the Dog Saw"'
WHERE NOT EXISTS (
    SELECT 1
    FROM authors
    WHERE first_name = 'Malcolm' AND last_name = 'Gladwell'
);

-- Insert into book_author bridge
INSERT INTO book_author (book_id, author_id)
SELECT b.book_id, a.author_id
FROM books b
JOIN authors a ON a.first_name = 'Malcolm' AND a.last_name = 'Gladwell'
WHERE b.title = 'What the Dog Saw' AND b.isbn = '978-0316084659';


/* Select query to retrieve details of a specific book using its ID */
SELECT
    b.book_id,
    b.title,
    GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS author,
    b.published_year,
    b.price,
    MAX(i.quantity) AS inventory
FROM books b
LEFT JOIN inventory i ON b.book_id = i.book_id
LEFT JOIN book_author ba ON b.book_id = ba.book_id
LEFT JOIN authors a ON ba.author_id = a.author_id
WHERE b.book_id = 3
GROUP BY
	b.book_id;


/* Update query to change an existing book's details */
-- Update quantity
UPDATE inventory SET quantity = 5 WHERE book_id = 1;
-- Update price
UPDATE books SET price = 19.99 WHERE book_id = 1;


/* Delete query to remove a book from the inventory */
DELETE FROM book_author WHERE book_id = 1;
DELETE FROM book_genre WHERE book_id = 1;
DELETE FROM inventory WHERE book_id = 1;
DELETE FROM books WHERE book_id = 1;
