import argparse
import logging
import multiprocessing
import os
import re
import sys

from gensim.models import Phrases
from gensim.models.word2vec import FAST_VERSION, Word2Vec


def generateEmbeddings(docs, outputFile, size=100, window=5, min_count=10, ngrams=0):
    for n in range(ngrams - 1):
        bigram_transformer = Phrases(docs, min_count=min_count)
        docs = bigram_transformer[docs]
    model = Word2Vec(docs, size=size, window=window, min_count=min_count,
                     workers=multiprocessing.cpu_count())
    model.init_sims(replace=True)
    model.save(outputFile)


class WikiDocReader:
    def __init__(self, input, encoding='utf8', splitter=r'\W+'):
        self._input = input
        self._splitter = re.compile(splitter)
        self._encoding = encoding

    def __iter__(self):
        return self.readDataset()

    def readDataset(self):
        if os.path.isfile(self._input):
            for match in self.processFile(self._input):
                yield match
        elif os.path.isdir(self._input):
            for root, dirnames, filenames in os.walk(self._input):
                for filename in filenames:
                    for match in self.processFile(os.path.join(root, filename)):
                        yield match

    def processFile(self, filename):
        with open(filename, 'r', encoding=self._encoding, errors='ignore') as fin:
            for line in fin:
                if not line.startswith('<'):
                    yield self._splitter.split(line.lower())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input',
                        help='Input directory with Wikipedia text (in the format produced by the wikipedia extractor (https://github.com/aesuli/wikipedia-extractor)',
                        type=str, required=True)
    parser.add_argument('-o', '--output', help='Output file', required=True)
    parser.add_argument('-e', '--encoding',
                        help='Input file enconding (default: utf8, for windows files try windows-1252 or ascii)',
                        default='utf-8')
    parser.add_argument('-m', '--mindf', help='Minimum DF (default: 100)', type=int, default=100)
    parser.add_argument('-v', '--vsize', help='Vector size (default: 200)', type=int, default=200)
    parser.add_argument('-n', '--ngrams', help='Use ngrams (default: no)', type=int, default=0)
    args = parser.parse_args()

    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))
    logging.info("using optimization %s", FAST_VERSION)

    docs = WikiDocReader(args.input, encoding=args.encoding)

    generateEmbeddings(docs, args.output, size=args.vsize, min_count=args.mindf, ngrams=args.ngrams)
