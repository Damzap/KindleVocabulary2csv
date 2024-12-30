import sqlite3
import requests

def read_books(db_path):
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Query
        query = f"SELECT id,title FROM BOOK_INFO;"
        cursor.execute(query)
        
        # Fetch all rows from the table
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

def fetch_word_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    #url = f"https://api.dictionaryapi.dev/api/v2/entries/en/hello"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
        data = response.json()
        

        # Assuming the API returns a list of meanings, we will get the first one
        if 'meanings' in data[0]:
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return definition

        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching definition for '{word}': {e}")
        return None

def select_words(db_path, book):
    if not book:
        print("No book selected.")
        return None

    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
        
    # Fetch words and usage based on the book
    query = """
    SELECT word, usage
    FROM WORDS
    JOIN LOOKUPS ON WORDS.id = LOOKUPS.word_key
    WHERE LOOKUPS.book_key = ?
    """
    
    cursor.execute(query, (book['id'],))

    # Fetch all rows from the table
    rows = cursor.fetchall()

    # Create an array of objects with 'word', 'usage', and 'definition' (if available)
    words = []
    seen_words = set()
    for row in rows:
        word = row[0].capitalize()
        usage = row[1]
            
        # Fetch the definition from the API
        definition = fetch_word_definition(word)
        # If no definition is found, skip the word
        if definition is None:
            continue
            
        if word not in seen_words:
            seen_words.add(word)
            #words.append({'word': word, 'usage': usage})
            words.append({'word': word, 'usage': usage, 'definition': definition})
            
    
    # words.sort(key=lambda x: x['word'])
    return words


if __name__ == "__main__":
    database_path = "/Users/damiano/Desktop/vocab.db"  
    books = read_books(database_path)
    book = select_book(books)
    words = select_words(database_path, book)
    definition = fetch_word_definition("hello")
    print(words)
    #flashcards = define_words(words)1
