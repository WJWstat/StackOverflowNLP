import re
import pickle
import nltk

# Load pickle
with open('pickles/posts.pkl', 'rb') as f:
    posts = pickle.load(f)

sentences = []
# dictionary to store sentences and the pos tags of the words
pos_tags = {} # {sentence: dictionary of words and tags}

# perform sentence tokenization to get sentences
for post in posts:
    post = re.sub(r'<code>.*</code>', '', post)  # remove inline code snippets

    for paragraph in post.split('\n'):
        if len(paragraph) == 0:
            continue
        sentences = sentences + nltk.tokenize.sent_tokenize(paragraph) # returns tokenized sentence

    if len(sentences) >= 10:
        break

# perform word tokenization on the sentences 
for sentence in sentences:
    # break if there are 10 tagged sentences 
    if len(pos_tags) == 10:
        break
    words = nltk.word_tokenize(sentence) # returns word tokens
    pos_tags[sentence] = nltk.pos_tag(words) # returns dictionary of word and pos tag

# write pos tags to file
with open('data_analysis/sentences_pos_tags.txt', 'w') as f:
    for key in list(pos_tags.keys()):
        f.write(str(key) + '\n')
        f.write(str(pos_tags[key]) + '\n')
        f.write('\n----\n' + '\n')

# pickle data
with open('pickles/pos_tags.pkl', 'wb') as f:
    pickle.dump(pos_tags, f)
