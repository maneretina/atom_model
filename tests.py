#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#author Neretina Maria
import unittest
import numpy as np
import pandas as pd
import os
import atom_model.prog as prog

class AtomTestCase(unittest.TestCase):
    def test_1(self):
        levels_list = pd.DataFrame(columns = ['name','g','e'])  
        levels_list = prog.levels(levels_list,prog.dat[:,0],prog.dat[:,1:].astype(float))

        for i in range(len(levels_list['energy'])-1):
            self.assertLess(levels_list['energy'][i+1],levels_list['energy'][i])


if __name__ == '__main__':
    unittest.main()

