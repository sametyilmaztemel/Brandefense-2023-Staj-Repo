import praw
import psycopg2
import time
from flask import Flask, jsonify

# Reddit API kimlik bilgilerinizi buraya girin
# Reddit Developer konsolundan aldığınız veriler ile bu kısımları doldurunuz
client_id = "client id" 
client_secret = "client secret"
username = "username"
password = "password"
user_agent = "BranDefenseRedditApp:1.0"

# Servisin çalışabilmesi için PostgreSQL veritabanının sistemde kurulu olması ve veritabanını oluşturulmuş olması gerekmektedir.
# PostgreSQL bağlantı bilgilerinizi buraya girin
dbname = "mydatabase"  # Veritabanı adı
user = "postgres"  # PostgreSQL kullanıcı adı
password = "your_password"  # PostgreSQL kullanıcı parolası
host = "localhost"  # PostgreSQL sunucu adresi
port = "5432"  # PostgreSQL sunucu port numarası

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS posts
                 (title TEXT, content TEXT)''')

app = Flask(__name__)

@app.route('/posts', methods=['GET'])
def get_posts():
    cursor.execute("SELECT * FROM posts ORDER BY rowid DESC")
    results = cursor.fetchall()
    posts = []
    for result in results:
        post = {
            'title': result[0],
            'content': result[1]
        }
        posts.append(post)
    return jsonify(posts)

def print_last_10_posts():
    cursor.execute("SELECT * FROM posts ORDER BY rowid DESC LIMIT 10")
    results = cursor.fetchall()
    print("Son 10 Veri:")
    for result in results:
        print("Başlık:", result[0])
        print("İçerik:", result[1])
        print("--------------")

subreddit = reddit.subreddit("python") # " " içerisine hangi subredditten veri almak istediğinizi yazın bunu 84. satırda da düzenlemelisiniz.
posts_to_crawl = 10

for submission in subreddit.new(limit=posts_to_crawl):
    title = submission.title
    content = submission.selftext

    cursor.execute("SELECT * FROM posts WHERE title=%s", (title,))
    existing_post = cursor.fetchone()

    if existing_post is None:
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        print("\nYeni bir post eklendi:")
        print("Başlık:", title)
        print("İçerik:", content)
        print("--------------")

conn.commit()

print("\n----- Başlangıç Verileri -----")
print_last_10_posts()

if __name__ == '__main__':
    app.run(port=5001, threaded=True)

while True:
    subreddit = reddit.subreddit("python")
    posts_to_crawl = 10

    for submission in subreddit.new(limit=posts_to_crawl):
        title = submission.title
        content = submission.selftext

        cursor.execute("SELECT * FROM posts WHERE title=%s", (title,))
        existing_post = cursor.fetchone()

        if existing_post is None:
            cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
            print("\nYeni bir post eklendi:")
            print("Başlık:", title)
            print("İçerik:", content)
            print("--------------")

    conn.commit()
    
    print("\n----- Güncel Veriler -----")
    print_last_10_posts()

    time.sleep(60)

conn.close()
