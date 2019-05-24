import argparse
import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from gensim.models import Word2Vec
from sklearn.decomposition import PCA

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input model file', required=True)
    parser.add_argument('-a', '--tags', help='Columns with tags to process', nargs='+', type=int, required=True)
    parser.add_argument('-v', '--vsize', help='Vocabulary size (default: 100)', type=int, default=100)
    parser.add_argument('-p', '--pca', help='Use PCA for analysis (default: t-sne)', action='store_true')
    parser.add_argument('-n', '--names', help='File with mapping of tags to human readable names')
    parser.add_argument('-d', '--dimensions', help='Visualization dimension 2/3 (default: 2)', type=int, default=2)
    parser.add_argument('-c', '--clusters', help='Number of clusters (default: 8)', type=int, default=8)

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

    names = dict()
    if args.names:
        with open(args.names, 'r', encoding='utf-8', errors='ignore') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    names[row[-2]] = row[-1]

    if args.pca:
        reducer = PCA(n_components=args.dimensions)
    else:
        reducer = TSNE(n_components=args.dimensions, random_state=0)

    clusterer = KMeans(n_clusters=args.clusters)

    X = np.array([np.array(model.docvecs[tag]) for tag in tags])

    labels = clusterer.fit_predict(X)
    colors = [cm.gist_rainbow(label / (clusterer.n_clusters - 1.)) for label in labels]
    y = reducer.fit_transform(X)
    plotx = y[:, 0]
    ploty = y[:, 1]
    if args.dimensions == 3:
        plotz = y[:, 2]
    fig = plt.figure()
    if args.dimensions == 3:
        subplot = Axes3D(fig)
        subplot.scatter(plotx, ploty, plotz, color=colors)
        for tag, x, y, z in zip(tags, plotx, ploty, plotz):
            m = tagre.findall(tag)
            if m and m[0][1] in names:
                subplot.text(x, y, z, names[m[0][1]])
            else:
                subplot.text(x, y, 0, tag)
    else:
        subplot = fig.add_subplot(111)
        subplot.scatter(plotx, ploty, color=colors)
        for tag, x, y in zip(tags, plotx, ploty):
            m = tagre.findall(tag)
            if m and m[0][1] in names:
                subplot.annotate(names[m[0][1]], (x, y))
            else:
                subplot.annotate(tag, (x, y))
    plt.show()
