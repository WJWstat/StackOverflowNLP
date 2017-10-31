import pickle
import enchant
import re

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


def main():
    get_irregular_token_stats()


if __name__ == '__main__':
    main()
