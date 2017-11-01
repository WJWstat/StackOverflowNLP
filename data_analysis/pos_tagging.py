import re
import pickle
import nltk

with open('pickles/posts.pkl', 'rb') as f:
    posts = pickle.load(f)

sentences = []
pos_tags = {}

for post in posts:
    post = re.sub(r'<code>.*</code>', '', post)  # remove inline code snippets

    for paragraph in post.split('\n'):
        if len(paragraph) == 0:
            continue
        sentences = sentences + nltk.tokenize.sent_tokenize(paragraph)

    if len(sentences) >= 10:
        break

for sentence in sentences:
    if len(pos_tags) == 10:
        break
    words = nltk.word_tokenize(sentence)
    pos_tags[sentence] = nltk.pos_tag(words)

with open('data_analysis/sentences_pos_tags.txt', 'w') as f:
    for key in list(pos_tags.keys()):
        f.write(str(key) + '\n')
        f.write(str(pos_tags[key]) + '\n')
        f.write('\n----\n' + '\n')

with open('pickles/pos_tags.pkl', 'wb') as f:
    pickle.dump(pos_tags, f)
