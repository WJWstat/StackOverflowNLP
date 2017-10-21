import re
import pickle
import nltk


def pos_tag_sentences():
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

        if len(sentences) >= 15:
            break

    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        pos_tags[sentence] = nltk.pos_tag(words)

    # for key in list(pos_tags.keys()):
    #     print(key)
    #     print(pos_tags[key])
    #     print('\n----\n')

    with open('pickles/pos_tags.pkl', 'wb') as f:
        pickle.dump(pos_tags, f)

if __name__ == '__main__':
    pos_tag_sentences()
