import sqlite3

conn = sqlite3.connect('autocomplete.db')
cursor = conn.cursor()

# Total word count
cursor.execute('SELECT COUNT(*) FROM words')
total_words = cursor.fetchone()[0]
print(f'Total words: {total_words}')

# Top categories
cursor.execute('SELECT category, COUNT(*) FROM words GROUP BY category ORDER BY COUNT(*) DESC LIMIT 15')
print('\nTop categories:')
for cat, count in cursor.fetchall():
    print(f'  {cat}: {count}')

# Sample words from each category
cursor.execute('SELECT DISTINCT category FROM words')
categories = [row[0] for row in cursor.fetchall()]

print('\nSample words from each category:')
for category in categories[:10]:  # Show first 10 categories
    cursor.execute('SELECT word FROM words WHERE category = ? LIMIT 5', (category,))
    words = [row[0] for row in cursor.fetchall()]
    print(f'  {category}: {", ".join(words)}')

conn.close()
