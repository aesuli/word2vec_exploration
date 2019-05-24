import argparse
import shutil
import os
import re
import csv
from gensim.models import Word2Vec

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input model file', required=True)
    parser.add_argument('-o', '--output', help='Output directory', required=True)
    parser.add_argument('-a', '--tags', help='Columns with tags to process', nargs='+', type=int, required=True)
    parser.add_argument('-s', '--sim', help='Similarity threshold (default: 0.6)', type=float, default=0.6)
    parser.add_argument('-v', '--vsize', help='Vocabulary size (default: 2000)', type=int, default=2000)
    parser.add_argument('-n', '--names', help='File with mapping of tags to human readable names')

    args = parser.parse_args()

    model = Word2Vec.load(args.input)

    tags = list(model.docvecs.doctags)

    tagre = re.compile('^COL([0-9]+)_(.*)$')

    withfreq = list()
    for tag in tags:
        m = tagre.findall(tag)
        if m and int(m[0][0]) in args.tags:
            withfreq.append((model.docvecs.doctags[tag].doc_count, tag))

    withfreq.sort(reverse=True)

    tags = list()

    for _, tag in withfreq:
        tags.append(tag)
        if len(tags) >= args.vsize:
            break

    tagset = set(tags)

    links = dict()
    nodes = set()

    for tag in tags:
        for simtag, dist in model.docvecs.most_similar(positive=[tag]):
            if dist > args.sim and simtag in tagset:
                if not tag in links:
                    links[tag] = list()
                links[tag].append(simtag)
                nodes.add(tag)
                nodes.add(simtag)

    nodes = list(nodes)
    nodetoidx = dict()
    for i, tag in enumerate(nodes):
        nodetoidx[tag] = i

    names = dict()
    if args.names:
        with open(args.names, 'r', encoding='utf-8', errors='ignore') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    names[row[-2]] = row[-1]

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
        for tag in nodes:
            m = tagre.findall(tag)
            if m:
                if m[0][1] in names:
                    tag = names[m[0][1]]
            file.write('{"name":"%s"},\n' % tag.replace('"', '\''))
        file.write(']\n')

        file.write('var links = [')
        for key in links:
            for target in links[key]:
                file.write('{ source: nodes[%i], target: nodes[%i]},\n' % (nodetoidx[key], nodetoidx[target]))

        file.write(']\n')
