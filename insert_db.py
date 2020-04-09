import sqlite3
import zipfile

import numpy as np
from tqdm import tqdm

docs = []
with zipfile.ZipFile('kompas.zip') as f:
    for file_ in f.namelist():
        if file_.endswith('.txt'):
            with f.open(file_, 'r') as tf:
                docs.append(tf.read().decode('utf-8'))

with zipfile.ZipFile('tempo.zip') as f:
    for file_ in f.namelist():
        if file_.endswith('.txt'):
            with f.open(file_, 'r') as tf:
                docs.append(tf.read().decode('utf-8'))

top5 = np.load('top5.npy')

db = sqlite3.connect('ui/db.sqlite3')
print('creating table news')
qry = """
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY,
    title TEXT,
    body TEXT,
    rels TEXT
)
"""
cursor = db.cursor()
cursor.execute(qry)
db.commit()

insert_qry = """
INSERT INTO news (id, title, body, rels)
VALUES (?, ?, ?, ?)
ON CONFLICT DO NOTHING
"""

print('inserting data')
for i in tqdm(range(len(docs)), total=len(docs)):
    full_doc = docs[i]
    splitted = full_doc.split('\n')
    title = splitted[0]
    body = '\n'.join(splitted[1:]).strip()
    top5_rels = ','.join([str(rel) for rel in top5[i, :]])
    cursor.execute(insert_qry, (i, title, body, top5_rels))

db.commit()
cursor.close()
db.close()
