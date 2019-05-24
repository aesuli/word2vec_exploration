import argparse
import bz2
import csv
import logging
import multiprocessing
import os
import re
import sys
from codecs import iterdecode

from gensim.models import Phrases
from gensim.models.word2vec import FAST_VERSION, Word2Vec


def generateEmbeddings(sentences, outputFile, size=100, window=5, min_count=10, ngrams=0):
    for n in range(ngrams - 1):
        bigram_transformer = Phrases(sentences, min_count=min_count)
        sentences = bigram_transformer[sentences]
    model = Word2Vec(sentences, size=size, window=window, min_count=min_count,
                     workers=multiprocessing.cpu_count())
    model.init_sims(replace=True)
    model.save(outputFile)


class DatasetReader:
    def __init__(self, inputFile, content_cols, compressed=False, encoding='utf8', splitter=r'\W+', count=None):
        self._inputFile = inputFile
        self._splitter = re.compile(splitter)
        self._max = count
        self._content_cols = content_cols
        self._compressed = compressed
        self._encoding = encoding

    def __iter__(self):
        return self.readDataset()

    def readDataset(self):
        if self._max:
            max = self._max
        if self._compressed:
            with bz2.BZ2File(self._inputFile, 'r') as fin:
                textfile = iterdecode(fin, encoding=self._encoding, errors='ignore')
                for line in self._read(textfile):
                    yield line
        else:
            with open(self._inputFile, 'r', encoding=self._encoding, errors='ignore') as fin:
                for line in self._read(fin):
                    yield line

    def _read(self, fin):
        if self._max:
            max = self._max

        reader = csv.reader(fin)
        for row in reader:
            words = list()
            for col in self._content_cols:
                words.extend(self._splitter.split(row[col].lower()))
            yield words
            if self._max:
                max -= 1
                if max == 0:
                    break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input CSV file', required=True)
    parser.add_argument('-o', '--output', help='Output file', required=True)
    parser.add_argument('-e', '--encoding',
                        help='Input file enconding (default: utf8, for windows files try windows-1252 or ascii)',
                        default='utf-8')
    parser.add_argument('-z', '--bz2', help='Input file is compressed', action='store_true')
    parser.add_argument('-t', '--text', help='Columns with text', nargs='+', type=int, required=True)
    parser.add_argument('-m', '--mindf', help='Minimum DF (default: 100)', type=int, default=100)
    parser.add_argument('-v', '--vsize', help='Vector size (default: 200)', type=int, default=200)
    parser.add_argument('-n', '--ngrams', help='Use ngrams (default: no)', type=int, default=0)
    parser.add_argument('-c', '--count', help='Read only a limited number of documents (default: no limit)', type=int,
                        default=None)
    args = parser.parse_args()

    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))
    logging.info("using optimization %s", FAST_VERSION)

    sentences = DatasetReader(args.input, args.text, compressed=args.bz2, count=args.count, encoding=args.encoding)

    generateEmbeddings(sentences, args.output, size=args.vsize, min_count=args.mindf, ngrams=args.ngrams)
