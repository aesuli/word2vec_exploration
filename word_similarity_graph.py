import argparse
import shutil
import os
from nltk.corpus import stopwords
from gensim.models import Word2Vec

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input model file', required=True)
    parser.add_argument('-o', '--output', help='Output directory', required=True)
    parser.add_argument('-s', '--sim', help='Similarity threshold (default: 0.8)', type=float, default=0.8)
    parser.add_argument('-v', '--vsize', help='Vocabulary size (default: 2000)', type=int, default=2000)
    parser.add_argument('-l', '--language', help='Stopwords language (default: english)', type=str, default='english')
    args = parser.parse_args()

    model = Word2Vec.load(args.input)

    words = list(model.wv.vocab)

    withfreq = list()
    for word in words:
        withfreq.append((model.wv.vocab[word].count, word))

    withfreq.sort(reverse=True)

    words = list()
    exclude = stopwords.words(args.language)
    for _, word in withfreq:
        if not word in exclude and len(word) > 1:
            words.append(word)
            if len(words) >= args.vsize:
                break

    wordset = set(words)

    links = dict()
    nodes = set()

    for word in words:
        for simword, dist in model.wv.most_similar(positive=[word]):
            if dist > args.sim and simword in wordset:
                if not word in links:
                    links[word] = list()
                links[word].append(simword)
                nodes.add(word)
                nodes.add(simword)

    nodes = list(nodes)
    nodetoidx = dict()
    for i, word in enumerate(nodes):
        nodetoidx[word] = i

    output = args.output

    i = 1
    while True:
        try:
            shutil.copytree('visualization_template', output)
            break
        except:
            output = args.output + '_' + str(i)
            i += 1
            if i > 100:
                break

    with open(os.path.join(output, 'js', 'data.js'), 'w', encoding='utf-8', errors='ignore') as file:
        file.write('var nodes= [')
        for word in nodes:
            file.write('  {"name":"%s"},\n' % word.replace('"', '\''))
        file.write(']\n')

        file.write('var links = [')
        for key in links:
            for target in links[key]:
                file.write('  { source: nodes[%i], target: nodes[%i]},\n' % (nodetoidx[key], nodetoidx[target]))

        file.write(']\n')
