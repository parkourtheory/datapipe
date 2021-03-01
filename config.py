'''
If properties are added to or removed from configuration files, change this object to make
them available to all tasks.
'''
import os
import configparser

from utils import *

class Configuration(object):
    def __init__(self, config):
        cfg = configparser.ConfigParser(allow_no_value=True)
        cfg.read(config)

        # default configuration
        default = cfg['DEFAULT']
        self.whitelist = self.get_whitelist() if default.getboolean('whitelist') else []
        self.parallel = default.getboolean('parallel')
        self.pipe = default['pipe']

        # move configuration
        move = cfg['moves']
        self.move_csv = move['csv']
        self.node_map = move['map']

        # video configuration
        video = cfg['videos']
        self.video_src = video['src']
        self.video_dst = video['dst']
        self.video_csv = video['csv']
        self.video_csv_out = video['csv_out']
        self.video_height = int(video['height']) if video['height'] else 0
        self.video_width = int(video['width']) if video['width'] else 0
            
        # thumbnail configuration
        thumb = cfg['thumbnails']
        self.thumb_height = int(thumb['height']) if thumb['height'] else 0
        self.thumb_width = int(thumb['width']) if thumb['width'] else 0
        self.thumb_dst = thumb['dst']

        # dataset configuration
        ds = cfg['dataset']
        self.dataset = ds['dataset']
        self.train_split = float(ds['train_split'] or 0)
        self.val_split = float(ds['val_split'] or 0)
        self.test_split = float(ds['test_split'] or 0)
        self.is_split = self.train_split + self.val_split + self.test_split == 1

        assert self.is_split
        
        if video['csv_out']: make_dir(video['csv_out'])
        if video['src']: make_dir(video['src'])
        if video['dst']: make_dir(video['dst'])
        if thumb['dst']: make_dir(thumb['dst'])


    '''
    Open and return white list

    outputs:
    ids (list) List of ids to whitelist
    '''
    def get_whitelist(self):
        cfg = configparser.ConfigParser()
        cfg.read(is_config('whitelist'))
        return [int(i) for i in cfg['DEFAULT']['ids'].split(',')]