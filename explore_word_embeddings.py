import argparse
from gensim.models import Word2Vec


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input word2vec model', required=True)
    args = parser.parse_args()

    model = Word2Vec.load(args.input)
    print(len(model.wv.vocab), 'words')
    print('type "?" for help')
    while True:
        line = input('> ')
        if line == 'x':
            break
        try:
            words = line.split(' ')
            if words[0] == '?':
                print(
                    'typing any word returns the list of the most similar words in the model (prefix a minus "-" to maximize dissimilarity)')
                print('* - lists all the words in the vocabulary')
                print('dnm followed by three or more words - return the most dissimilar word from the set')
            elif words[0] == '*':
                for word in model.wv.vocab:
                    print(word)
            elif words[0] == 'dnm':
                # find which word in the list is the least related to the other words
                print(model.wv.doesnt_match(words[1:]))
            else:
                # find which words in the model are most similar to the ones provided as query,
                # and most dissimilar to those entered with a preceeding '-'
                positive = [word for word in words if word[0] != '-']
                negative = [word[1:] for word in words if word[0] == '-']
                print(model.wv.most_similar(positive, negative))
        except KeyError as ke:
            print(ke)
        except:
            pass


if __name__ == "__main__":
    main()
