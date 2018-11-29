import pandas as pd
import os
from skimage import io, transform
from torch.utils.data import DataLoader, Dataset


class AnimeDataSet(Dataset):

    def __init__(self, csv_file, root_dir, transform=None):
        super(AnimeDataSet, self).__init__()
        self.tag_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.tag_frame)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, '{}.jpg'.format(self.tag_frame.iloc[idx, 0]))
        image = io.imread(img_name)
        sample = {'image': image}
        return sample
