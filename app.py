from flask import Flask, render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
books = pickle.load(open('books.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
print(books)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/Recommand')
def recommend_ui():
    return render_template('recommand.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    try:
        user_input = request.form.get('user_input')
        index = np.where(pt.index == user_input)
        index=index[0][0]
        print(index)
    
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:7]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            print (temp_df)
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['num_ratings'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['avg_rating'].values))

            data.append(item)

        print(data)

        return render_template('Recommand.html',data=data)
    except IndexError:
        # Handle the case when the value is not found in pt.index
        print("Value not found in pt.index.")
        err="The book you trying does not exits in data base Please Find any other book...."
        return render_template('Recommand.html',error=err)

@app.route('/About')
def About():
    return render_template('About.html')
    
@app.route('/contact')
def Contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)