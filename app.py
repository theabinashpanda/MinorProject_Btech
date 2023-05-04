from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import subprocess

popular_books = pd.read_pickle("popular_books.pkl")
book_pivot=pd.read_pickle("book_pivot.pkl")
books=pd.read_pickle("books.pkl")
similarity_score=pd.read_pickle("similarity_score.pkl")

# popular_books= pickle.load(open('popular_books.pkl', 'rb'))
# book_pivot= pickle.load(open('book_pivot.pkl', 'rb'))
# books= pickle.load(open('books.pkl', 'rb'))
# similarity_score= pickle.load(open('similarity_score.pkl', 'rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            book_names= list(popular_books['title'].values),
                            authors=list(popular_books['author'].values),
                            votes=list(popular_books['num_ratings'].values),
                            ratings=list(popular_books['avg_ratings'].values),
                            images=list(popular_books['image'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=["post"])
def recommend():
    user_input= request.form.get("user_input")
    book_index = np.where(book_pivot.index == user_input)[0][0]
    suggested_items = sorted(list(enumerate(similarity_score[book_index])), key=lambda x: x[1], reverse=True)[1:5]
    book_list = list(books["title"].values)

    data = []
    for i in suggested_items:
        item = []
        temp = books[books["title"] == book_pivot.index[i[0]]]
        item.extend(temp.drop_duplicates("title")['title'].values)
        item.extend(temp.drop_duplicates("title")['author'].values)
        item.extend(temp.drop_duplicates("title")['image'].values)

        data.append(item)
    return render_template('recommend.html', data=data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/Abinash.html')
def abinash():
    return render_template('Abinash.html')

@app.route('/Abhudaya.html')
def abhudaya():
    return render_template('Abhudaya.html')

@app.route('/Gautam.html')
def gautam():
    return render_template('Gautam.html')

@app.route('/Ankit.html')
def ankit():
    return render_template('Ankit.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/feedback_success.html')
def feedback_success():
    return render_template('feedback_success.html')

@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        feedback = request.form['feedback']

        # execute PHP script with feedback data
        php_script = 'submit_feedback.php'
        command = f'php {php_script} "{name}" "{email}" "{feedback}"'
        result = subprocess.check_output(command, shell=True)

        return render_template('feedback_success.html')
    else:
        return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)
