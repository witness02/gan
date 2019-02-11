"""
Using to generate negative data-set.
"""
import argparse


# Voc class keeps a mapping from words to indexes, a reverse mapping of indexes to words.
class Voc:
    def __init__(self, name):
        self.name = name
        self.word2index = {}
        self.index2word = {}
        self.word2count = {}
        self.num_words = 0

    def add_word(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.index2word[self.num_words] = word
            self.word2count[word] = 1
            self.num_words += 1
        else:
            self.word2count[word] += 1

    def add_sentence(self, sentence, separator):
        for word in sentence.split(separator):
            self.add_word(word)


def gen_voc(filename):
    voc = Voc('color')
    with open(filename) as datafile:
        lines = datafile.readlines()
        for line in lines:
            sp = line.split(',')
            if len(sp) != 2:
                continue
            desc = sp[1]
            tags = desc.split(' ')
            if len(tags) != 4:
                continue
            voc.add_word(tags[0])
            voc.add_word(tags[2])
    return voc


def get_tag_set(filename):
    tag_set = set()
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            sp = line.split(',')
            if 2 != len(sp):
                continue
            tag_set.add(sp[1])
    return tag_set


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='process data')
    parser.add_argument('--cmd', type=str, help='command')
    parser.add_argument('--filename', type=str, help='name of source file')
    parser.add_argument('--gen-filename', type=str, help='name of dist file')
    args = parser.parse_args()

    print('Begin to generate word mapping')

    voc = gen_voc(args.filename)

    print('Finish generating... \nthe number of words is {} \nmapping from index to word is \n\t{}'.format(
        voc.num_words, voc.index2word
    ))

    print('Begin to generate negative data-set')
    tag_set = get_tag_set(args.filename)
    negative_txt = ''
    for source_tag in tag_set:
        with open(args.filename) as positive_file:
            lines = positive_file.readlines()
            for line in lines:
                sp = line.split(',')
                if 2 != len(sp):
                    continue
                image_idx = sp[0]
                desc = sp[1]
                if source_tag == desc:
                    continue
                negative_txt += image_idx + ',' + source_tag + '\n'
    with open(args.gen_filename, 'w') as negative_file:
        negative_file.writelines(negative_txt)
    print('Success to write to negative file')

