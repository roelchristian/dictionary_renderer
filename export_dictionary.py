# Creates an html file based on data exported from the database

import psycopg2
import pandas as pd
import yaml
import sqlalchemy
import config

# create connection to postgresql database
connection_string = config.connection_string

engine = sqlalchemy.create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(**connection_string))
print(engine)

query_string = "select * from wordlist order by word asc"

df = pd.read_sql_query(query_string, engine)

html_string = ""

for index, row in df.iterrows():
    print(row['word'], row['definition'])

    word = row['word']

    part_of_speech = row['part_of_speech']
    definition = row['definition']


    html_string += f"""
        <div class="word">
            <span class="word_main_entry">{word}</span>
            <span class="word_part_of_speech">{part_of_speech}</span>
            <span class="word_definition">{definition}</span>
        </div>
    """

# Open index.html file and write the html_string to it by replacing the placeholder text "{{content}}"
# Save index.html as dictionary.html

# Delete dictionary.html if it already exists
import os
if os.path.exists("dictionary.html"):
    os.remove("dictionary.html")


with open("template.html", "r") as f:
    template_html = f.read()


template_html = template_html.replace("{{content}}", html_string)
print(template_html)

with open("dictionary.html", "w") as f:
    f.write(template_html)



# close engine
engine.dispose()

