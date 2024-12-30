import sqlite3
import requests
import csv
import argparse

def read_books(db_path):
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        query = f"SELECT id,title FROM BOOK_INFO;"
        cursor.execute(query)
        rows = cursor.fetchall()
        
        books = [{"id": row[0], "title": row[1]} for row in rows]
        books = sorted(books, key=lambda book: book['title'])

        return books

        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        if connection:
            connection.close()

def select_book(book):
    if not books:
        print("No books available.")
        return None

    print("\nAvailable Books:")
    for idx, book in enumerate(books, start=1):
        print(f"{idx}. {book['title']}")
        
    while True:
        try:
            choice = int(input("\nEnter the number of the book you want to select: "))
            if 1 <= choice <= len(books):
                return books[choice - 1]
            else:
                print("Invalid choice. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def fetch_word_definition(word, api_key):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
        data = response.json()
        
        # Check if the response contains valid definition(s)
        if isinstance(data, list) and "shortdef" in data[0]:
            definition = "; ".join(data[0]["shortdef"])
            return definition
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching definition for '{word}': {e}")
        return None

def select_words(db_path, book, api_key):
    if not book:
        print("No book selected.")
        return None

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
        
    query = """
    SELECT word, usage
    FROM WORDS
    JOIN LOOKUPS ON WORDS.id = LOOKUPS.word_key
    WHERE LOOKUPS.book_key = ?
    """
    
    cursor.execute(query, (book['id'],))

    rows = cursor.fetchall()

    words = []
    seen_words = set()

    for row in rows:
        word = row[0].capitalize()
        usage = row[1]
            
        # Fetch the definition using the Merriam-Webster API 
        definition = fetch_word_definition(word, api_key)
        
        # If no definition is found, skip the word
        if definition is None:
            continue
            
        if word not in seen_words:
            seen_words.add(word)
            words.append({'word': word, 'usage': usage, 'definition': definition})
            
    words.sort(key=lambda x: x['word'])
    return words

def export_to_csv(data, file_name):
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            # Extract the keys from the first dictionary as column names
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(data)

        print(f"Data successfully exported to {file_name}")
    except Exception as e:
        print(f"An error occurred while exporting to CSV: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("database_path", help="Path to the SQLite database.")
    parser.add_argument("api_key", help="Merriam-Webster API key.")
    args = parser.parse_args()
    
    database_path = args.database_path
    api_key = args.api_key
    
    books = read_books(database_path)
    book = select_book(books)
    words = select_words(database_path, book, api_key)
    filename = f"{(book['title'])}.csv"
    export_to_csv(words, filename)