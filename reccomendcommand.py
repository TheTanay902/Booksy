from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def recbok(mybook):
    books = pd.read_csv(r'C:\Users\tanay\Documents\Codes\python\RecoSys\data\bookcrossing\BX-Books.csv',
                        sep=';', error_bad_lines=False, encoding="latin-1")
    books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication',
                     'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
    users = pd.read_csv(r'C:\Users\tanay\Documents\Codes\python\RecoSys\data\bookcrossing\BX-Users.csv',
                        sep=';', error_bad_lines=False, encoding="latin-1")
    users.columns = ['userID', 'Location', 'Age']
    ratings = pd.read_csv(r'C:\Users\tanay\Documents\Codes\python\RecoSys\data\bookcrossing\BX-Book-Ratings.csv',
                          sep=';', error_bad_lines=False, encoding="latin-1")
    ratings.columns = ['userID', 'ISBN', 'bookRating']
    # plt.rc("font", size=15)
    # ratings.bookRating.value_counts(sort=True).plot(kind='bar')
    # plt.title('Rating Distribution\n')
    # plt.xlabel('Rating')
    # plt.ylabel('Count')
    # plt.savefig('system1.png', bbox_inches='tight')
    # plt.show()
    average_rating = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].mean())
    average_rating['ratingCount'] = pd.DataFrame(
        ratings.groupby('ISBN')['bookRating'].count())
    average_rating.sort_values('ratingCount', ascending=False).head()
    counts1 = ratings['userID'].value_counts()
    ratings = ratings[ratings['userID'].isin(counts1[counts1 >= 200].index)]
    counts = ratings['ISBN'].value_counts()
    ratings = ratings[ratings['ISBN'].isin(counts[counts >= 100].index)]
    ratings_pivot = ratings.pivot(index='userID', columns='ISBN').bookRating
    userID = ratings_pivot.index
    ISBN = ratings_pivot.columns
    # print(ratings_pivot.shape)
    # ratings_pivot.head()
    hahahha = "hahahah"
    combine_book_rating = pd.merge(ratings, books, on='ISBN')
    columns = ['yearOfPublication', 'publisher',
               'bookAuthor', 'imageUrlS', 'imageUrlM', 'imageUrlL']
    combine_book_rating = combine_book_rating.drop(columns, axis=1)
    # combine_book_rating.head()
    combine_book_rating = combine_book_rating.dropna(
        axis=0, subset=['bookTitle'])

    book_ratingCount = (combine_book_rating.
                        groupby(by=['bookTitle'])['bookRating'].
                        count().
                        reset_index().
                        rename(columns={'bookRating': 'totalRatingCount'})
                        [['bookTitle', 'totalRatingCount']]
                        )
    # book_ratingCount.head()
    rating_with_totalRatingCount = combine_book_rating.merge(
        book_ratingCount, left_on='bookTitle', right_on='bookTitle', how='left')
    # rating_with_totalRatingCount.head()
    popularity_threshold = 100
    rating_popular_book = rating_with_totalRatingCount.query(
        'totalRatingCount >= @popularity_threshold')
    # rating_popular_book.head()

    combined = rating_popular_book.merge(
        users, left_on='userID', right_on='userID', how='left')

    mymatirx = combined.drop('Age', axis=1)
    # mymatirx.head()
    mymatirx = mymatirx.drop_duplicates(['userID', 'bookTitle'])
    pivotedmatrix = mymatirx.pivot(
        index='bookTitle', columns='userID', values='bookRating').fillna(0)

    finalfit = csr_matrix(pivotedmatrix.values)

    model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
    model_knn.fit(finalfit)
    query_index = 98
    listreturner = []
    for i in range(99):
        newstring = pivotedmatrix.index[i]
        if mybook in newstring:
            query_index = i

    distances, indices = model_knn.kneighbors(
        pivotedmatrix.iloc[query_index, :].values.reshape(1, -1), n_neighbors=6)
    for i in range(0, len(distances.flatten())):
        if i == 0:
            listreturner.append('Recommendations for {0}:\n'.format(
                pivotedmatrix.index[query_index]))
        else:
            listreturner.append('{0}: {1}, with distance of {2}:'.format(
                i, pivotedmatrix.index[indices.flatten()[i]], distances.flatten()[i]))
    return listreturner
