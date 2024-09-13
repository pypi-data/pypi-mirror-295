import glob
import os
import re

import stanza

from stanza.utils.default_paths import get_default_paths

begin_re = re.compile(r"B-([0-9]+)")
in_re =  re.compile(r"I-([0-9]+)")

def read_doc(filename):
    with open(filename, encoding="utf-8") as fin:
        lines = fin.readlines()

    all_words = []
    all_coref = []
    current_words = []
    current_coref = []
    for line in lines:
        line = line.strip()
        if not line:
            all_words.append(current_words)
            all_coref.append(current_coref)
            current_words = []
            current_coref = []
            continue
        pieces = line.split("\t")
        current_words.append(pieces[3])
        current_coref.append(pieces[-1])

    if current_words:
        all_words.append(current_words)
        all_coref.append(current_coref)

    return all_words, all_coref

def process_coref(filename, sentences, corefs):
    processed = []

    start_idx = cluster = None
    for sent_idx, sentence_coref in enumerate(corefs):
        for word_idx, word_coref in enumerate(sentence_coref):
            if word_coref == '-':
                if start_idx is not None:
                    processed.append((cluster, start_idx, word_idx-1))
                    start_idx = cluster = None
                continue
            if word_coref.startswith('I-'):
                try:
                    word_cluster = int(word_coref[2:])
                except ValueError as e:
                    raise ValueError("Unexpected coref format %s in document %s" % (word_coref, filename))
                if word_cluster != cluster:
                    raise ValueError("Unexpected coref %s followed B-%d" % (word_coref, cluster))
                continue
            if not word_coref.startswith('B-'):
                raise ValueError("Unexpected coref %s" % word_coref)
            if start_idx is not None:
                processed.append((cluster, start_idx, word_idx-1))
                start_idx = cluster = None
            cluster = int(word_coref[2:])
            start_idx = word_idx
        if start_idx is not None:
            processed.append((cluster, start_idx, len(sentence_coref)-1))
    return sentences

def main():
    paths = get_default_paths()
    coref_input_path = paths["COREF_BASE"]
    tamil_base_path = os.path.join(coref_input_path, "tamil", "ta_Coref_data")
    tamil_glob = os.path.join(tamil_base_path, "*txt")

    filenames = sorted(glob.glob(tamil_glob))
    docs = [read_doc(x) for x in filenames]
    docs = [process_coref(filename, doc[0], doc[1]) for filename, doc in zip(filenames, docs)]

if __name__ == '__main__':
    main()
