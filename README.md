# Description
`KindleVocabularyToCsv.py` is a Python script that extracts vocabulary words and their usage examples from a Kindle Vocabulary Builder Database, fetches their definitions using the Merriam-Webster Dictionary API, and exports the data into a CSV file. 

This tool is perfect for Kindle users who want to consolidate their vocabulary into a structured format for study or review.

The generated CSV file can be imported into any software that supports flashcard creation, allowing for easy integration into your study routine.
# Requirements

- Python 3.x
- SQLite database containing Kindle vocabulary data.
- Merriam-Webster Collegiate Dictionary API key. 

# Installation

1. Clone this repository:
```
git clone https://github.com/Damzap/KindleVocabularyToCsv.git
cd KindleVocabularyToCsv
```

2. Install required Python libraries:
```
pip install requests
```

## Retrieve `vocab.db` from Kindle

To use this script, you need the `vocab.db` file from your Kindle device:

1. Connect your Kindle to your computer via USB.    
2. Open the Kindle storage on your computer.
3. Navigate to the `system` folder. Note: This folder might be hidden. Ensure you enable viewing of hidden files and folders.
4. Locate the `vocab.db` file and copy it to your computer.

# Usage

Run the script with the following command:
```
python KindleVocabularyToCsv.py <database_path> <api_key>
```

## Parameters

- `<database_path>`: The path to your Kindle SQLite database.
- `<api_key>`: Your Merriam-Webster Collegiate Dictionary API key.


The script will:
1. Display a menu of available books.
2. Prompt you to select a book.
3. Extract and process the words, fetching definitions.
4. Export the results to a CSV file named `<book_title>_words.csv`.

## Output Example

A sample entry in the CSV file:

| Word    | Usage                                                              | Definition                                                |
| ------- | ------------------------------------------------------------------ | --------------------------------------------------------- |
| Adage   | “Studio musicians have this adage: ‘The tape doesn’t lie.’"        | A saying often in metaphorical form that embodies a truth |
| Advisor | "I had set up a meeting with my advisor to discuss my job search." | Someone who gives advice                                  |
