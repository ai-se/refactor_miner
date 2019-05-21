# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 15:39:01 2018

@author: suvod
"""

from pygit2 import clone_repository
from pygit2 import GIT_SORT_TOPOLOGICAL, GIT_SORT_REVERSE,GIT_MERGE_ANALYSIS_UP_TO_DATE,GIT_MERGE_ANALYSIS_FASTFORWARD,GIT_MERGE_ANALYSIS_NORMAL,GIT_RESET_HARD
from pygit2 import Repository
import shutil,os
import pygit2
import re
from os import listdir
from os.path import isfile, join
from datetime import datetime
import platform
import threading
from multiprocessing import Queue
from threading import Thread
import numpy as np
import itertools
import pandas as pd
from multiprocessing import Pool, cpu_count
from os.path import dirname as up


class git2repo(object):
    
    def __init__(self,repo_url,repo_name):
        self.repo_url = repo_url
        self.repo_name = repo_name
        self.repos = []
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.repo_path = os.getcwd() + '/temp_repo/' + repo_name
        else:
            self.repo_path = os.getcwd() + '\\temp_repo\\' + repo_name
        self.cores = cpu_count()
        
    def clone_repo(self):
        git_path = pygit2.discover_repository(self.repo_path)
        if git_path is not None:
            self.repo = pygit2.Repository(git_path)
            return self.repo
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
        self.repo = clone_repository(self.repo_url, self.repo_path)
        return self.repo

    
    def repo_remove(self):
        self.repo.free()
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            deldir = self.repo_path + '/.git/objects/pack'
        else:
            deldir = self.repo_path + '\\.git\\objects\\pack'
        print(os.path.isfile(deldir))
        delFiles = [f for f in listdir(deldir) if isfile(join(deldir, f))]
        for i in delFiles:
            if platform.system() == 'Darwin' or platform.system() == 'Linux':
                file_name = deldir + '/' + i
            else:
                file_name = deldir + '\\' + i
            os.chmod(file_name, 0o777)
        if os.path.exists(self.repo_path):
            shutil.rmtree(self.repo_path,ignore_errors=True)
            
        
    def get_current_commit_objects(self):
        commits = []
        for commit in self.repo.walk(self.repo.head.target, GIT_SORT_TOPOLOGICAL | GIT_SORT_REVERSE):
            commits.append(commit)
        return commits
        
        