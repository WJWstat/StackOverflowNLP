import re
import pickle
import nltk


def stem_posts():
    with open('pickles/posts.pkl', 'rb') as f:
        posts = pickle.load(f)

    with open('data_analysis/stop_words.txt', 'r') as f:
        stop_words = [line.rstrip() for line in f]

    porter_stemmer = nltk.stem.porter.PorterStemmer()
    stems = {}  # dictionary of stems {stem: { 'orig_words': (set), 'count': 123 }, ...}
    words = {}  # dictionary of words {word: count}

    for post in posts:
        post = re.sub(r'<code>.*</code>', '', post)  # remove inline code snippets

        for paragraph in post.split('\n'):
            paragraph = paragraph.lower()  # lowercase text
            tokens = nltk.word_tokenize(paragraph)

            for token in tokens:
                token = re.sub(r'[^a-z]', '', token)  # remove any non-alphabet characters
                if token == '' or token in stop_words:
                    continue
                    
                if token in words.keys():
                    words[token] += 1
                else:
                    words[token] = 1

                stem = porter_stemmer.stem(token)

                if stem in stems:
                    stems[stem]['count'] += 1
                    stems[stem]['orig_words'].add(token)
                else:
                    stems[stem] = {}
                    stems[stem]['count'] = 1
                    stems[stem]['orig_words'] = set([token])

    counter = 50
    for s in sorted(stems.items(), key=lambda k_v: k_v[1]['count'], reverse=True):
        print(s)
        counter -= 1
        if counter == 0:
            break
            
    with open('data_analysis/frequent_words.txt', 'w') as f:
	    frequent_word_list = sorted(words, key=words.__getitem__, reverse=True)[:20]
	    for word in frequent_word_list:
	    	f.write(str(word) + ': ' + str(words[word]) + '\n')

    #with open('pickles/stems.pkl', 'wb') as f:
    #    pickle.dump(stems, f)

if __name__ == '__main__':
    stem_posts()
