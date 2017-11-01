import pickle
import enchant
import re
import nltk
from tokenizer_implemented import simple_tokenizer


def get_irregular_token_stats():
    with open('pickles/tokens.pkl', 'rb') as f:
        tokens = pickle.load(f)

    f = open('tokenization/irregular_token_stats.txt', 'w+')

    d = enchant.Dict("en_US")

    irregular_tokens = {}
    for token in tokens:
        if not d.check(token):
            irregular_tokens[token] = irregular_tokens.get(token, 0) + 1

    count = 0

    f.write("{:10} : {:7}\n".format("Token", "Count"))
    for key, value in sorted(irregular_tokens.items(), key=lambda x: x[1], reverse=True):
        if re.match(r'[a-zA-Z]', key):
            f.write("{:10} : {:7}\n".format(key, value))
            count += 1
            if count == 20:
                break


def pos_tag_sentences():
    with open('pickles/posts.pkl', 'rb') as f:
        posts = pickle.load(f)

    sentences = []
    pos_tags = {}
    d = enchant.Dict("en_US")

    for post in posts:
        post = re.sub(r'<code>.*</code>', '', post)  # remove inline code snippets

        for paragraph in post.split('\n'):
            if len(paragraph) == 0:
                continue

            sub_sentences = nltk.tokenize.sent_tokenize(paragraph)
            for sub_sentence in sub_sentences:
                if len(sentences) >= 15:
                    break
                words = sub_sentence.split()
                for word in words:
                    if not d.check(word):
                        sentences.append(sub_sentence)
                        break

    for sentence in sentences:
        words = []
        for token in simple_tokenizer(sentence):
            if token:
                words.append(token)
        # words = nltk.word_tokenize(sentence)
        pos_tags[sentence] = nltk.pos_tag(words)

    with open('tokenization/pos_tags_using_tokenizer.txt', 'w') as f:
        for key in list(pos_tags.keys()):
            f.write(key)
            f.write('\n\n[{}]\n\n'.format(', '.join(("('" + token + "', '" + tag + "')")
                                                    for token, tag in pos_tags[key])))
            f.write('\n----\n')

    with open('pickles/pos_tags_using_tokenizer.pkl', 'wb') as f:
        pickle.dump(pos_tags, f)


def main():
    get_irregular_token_stats()
    pos_tag_sentences()


if __name__ == '__main__':
    main()
