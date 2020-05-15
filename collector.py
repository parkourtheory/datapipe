import os
import sys
import pandas as pd
from tqdm import tqdm
from pytube import YouTube

sys.path.insert(1, '/media/ch3njus/Seagate4TB/projects/pystagram')

from pystagram import Instagram

class Collector(object):
    def __init__(self):
        pass


    def collect(self):
        failed = pd.DataFrame(columns=['id', 'moveName', 'vid', 'channel', 'link', 'time', 'embed'])
        failed.reset_index()
        table = pd.read_csv('database/missing_with_link.csv')
        prj_dir = '/media/ch3njus/Seagate4TB/research/parkourtheory/data/videos'
        dst = os.path.join(prj_dir, 'scraped')

        if not os.path.exists(dst):
            os.makedirs(dst)

        for i, row in tqdm(table.iterrows(), total=len(table)):
            name = row['moveName'].lower().replace(' ', '_')
            link = row['link']

            try:
                if 'youtube' in link:
                    vid = YouTube(link)
                    vid.streams.get_highest_resolution().download(dst, filename=name)
                elif 'instagram' in link:
                    gram = Instagram(link)
                    gram.download(dest=dst, filename=name)
                table.at[i, 'embed'] = name+'.mp4'
            except Exception:
                failed = failed.append(row, ignore_index=True)

        table = table[~table.id.isin(failed.id)]
        table = table.drop(table.columns[0], axis=1)
        failed.to_csv('unavailable.csv')
        table.to_csv('found.csv')