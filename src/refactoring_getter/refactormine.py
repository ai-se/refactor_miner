#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 18:54:29 2019

@author: suvodeepmajumder
"""
from git_log import git2repo
from utils import  regex_matcher
import os
import re
import shlex
import numpy as np
import pandas as pd
from glob2 import glob, iglob
import subprocess as sp
import understand as und
from pathlib import Path
from pdb import set_trace
import sys
from collections import defaultdict
import os
import platform
from os.path import dirname as up


class RefactorMine(object):
    """
    Generate class, file, function, object oriented metrics for a project.

    Parameters
    ----------
    sources_path: str or pathlib.PosixPath

    Notes
    -----
    The class is designed to run in conjunction with a context manager.
    """

    def __init__(self,repo_url,repo_name):
        self.matcher = regex_matcher.regex_matcher()
        self.repo_url = repo_url
        self.repo_name = repo_name
        self.repo_obj = git2repo.git2repo(self.repo_url,self.repo_name)
        self.repo = self.repo_obj.clone_repo()
        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            self.repo_path = os.getcwd() + '/temp_repo/' + self.repo_name
            self.file_path = self.repo_path + '/all_refactorings_master.csv'
        else:
            self.repo_path = os.getcwd() + '\\temp_repo\\' + self.repo_name
            self.file_path = self.repo_path + '\\all_refactorings_master.csv'
        #self.repo_path = self.repo_obj.repo_path
        # Reference current directory, so we can go back after we are done.
        self.cwd = Path(os.getcwd())
        print(self.cwd)


    @staticmethod
    def _os_cmd(cmd, verbose=True):
        """
        Run a command on the shell

        Parameters
        ----------
        cmd: str
            A command to run.
        """
        cmd = shlex.split(cmd)
        #print(cmd)
        with sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.DEVNULL) as p:
            out, err = p.communicate()

        if verbose:
            print(out)
            print(err)
        return out, err
    
    

    def get_refactored_commits(self):
        """
        Use the refactpr miner tool's API to identify refactored commits

        Notes
        -----
        
        """

        self.commit_dataframe = pd.DataFrame()
        cmd = "RefactoringMiner -a {} {}".format(str(self.repo_path), 'master')
        print(cmd)
        out, err = self._os_cmd(cmd)
        self.commit_dataframe = pd.read_csv(self.file_path,sep = ';')
        self.commit_dataframe['before_class'] = [0]*self.commit_dataframe.shape[0]
        self.commit_dataframe['after_class'] = [0]*self.commit_dataframe.shape[0]
        for i in range(self.commit_dataframe.shape[0]):
            refactoring_type = self.commit_dataframe.iloc[i,1]
            refactoring_details = self.commit_dataframe.iloc[i,2]
            before_class, after_class = self.matcher.case_statements(refactoring_type,refactoring_details)
            self.commit_dataframe.iloc[i,3] = before_class
            self.commit_dataframe.iloc[i,4] = after_class
        self.save_to_csv()
        return self.commit_dataframe

    def save_to_csv(self):
        """
        Save the metrics dataframe to CSV
        """
        # Determine the path to save file
        save_path = up(self.cwd) + '/results/refactored/' +self.repo_name + '.csv'
        # Save the dataframe (no index column)
        self.commit_dataframe.to_csv(save_path, index=False)
        #self.repo_obj.repo_remove()

