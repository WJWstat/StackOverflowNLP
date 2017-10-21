import re
import pickle
from nltk.stem.porter import PorterStemmer


def stem_posts():
    with open('pickles/posts.pkl', 'rb') as f:
        posts = pickle.load(f)

    with open('data_analysis/stop_words.txt', 'r') as f:
        stop_words = [line.rstrip() for line in f]

    porter_stemmer = PorterStemmer()
    stems = {}  # dictionary of stems {stem: { 'orig_words': (set), 'count': 123 }, ...}

    for post in posts:
        post = re.sub(r'<code>.*</code>', '', post)  # remove inline code snippets
        for paragraph in post.split('\n'):
            paragraph = paragraph.lower()  # lowercase
            paragraph = re.sub(r'[^a-z]', ' ', paragraph)  # replace non-alphabet characters with ' '
            paragraph = paragraph.strip()
            for word in paragraph.split(' '):
                if word in stop_words or word == '':
                    continue

                stem = porter_stemmer.stem(word)

                if stem in stems:
                    stems[stem]['count'] += 1
                    stems[stem]['orig_words'].add(word)
                else:
                    stems[stem] = {}
                    stems[stem]['count'] = 1
                    stems[stem]['orig_words'] = set([word])

    # counter = 50
    # for s in sorted(stems.items(), key=lambda k_v: k_v[1]['count'], reverse=True):
    #     print(s)
    #     counter -= 1
    #     if counter == 0:
    #         break

    with open('pickles/stems.pkl', 'wb') as f:
        pickle.dump(stems, f)

if __name__ == '__main__':
    stem_posts()
