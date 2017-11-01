import pickle
import re
import matplotlib.pyplot as plt
import nltk

with open('pickles/posts.pkl', 'rb') as f:
    posts = pickle.load(f)

post_length = {}
for post in posts:
    post = re.sub(r'<code>.*</code>', '', post)  # remove inline code snippets
    words = nltk.word_tokenize(post)

    if len(words) in post_length:
        post_length[len(words)] += 1
    else:
        post_length[len(words)] = 1

plt.figure()
plt.bar(list(post_length.keys()), list(post_length.values()), width=1.0)
plt.xlabel('Word Count')
plt.ylabel('No. of Posts')
plt.tight_layout()
plt.savefig('plots/post_length.png', dpi=800)
plt.close('all')
