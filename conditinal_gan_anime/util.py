import pandas as pd
import os
from skimage import io, transform
import numpy as np
from torch.utils.data import DataLoader, Dataset
from data_process import gen_voc


class AnimeDataSet(Dataset):

    def __init__(self, csv_file, root_dir, transform=None):
        super(AnimeDataSet, self).__init__()
        self.tag_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform
        self.voc = gen_voc(csv_file)

    def __len__(self):
        return len(self.tag_frame)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, '{}.jpg'.format(self.tag_frame.iloc[idx, 0]))
        image = io.imread(img_name)
        desc = self.tag_frame.iloc[idx, 1]
        tags = desc.split(' ')
        hair = tags[0]
        eyes = tags[2]
        words_len = self.voc.num_words
        sample = {
            'image': image,
            'tag': np.array([float(self.voc.word2index[hair])/words_len, float(self.voc.word2index[eyes])/words_len])
        }
        return sample
