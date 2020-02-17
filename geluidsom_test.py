# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 13:16:45 2020

@author: A642983
"""
import unittest
import geluidsom as gs
import pandas as pd
from pandas.util.testing import assert_frame_equal
from pandas.util.testing import assert_series_equal
import numpy as np

class dB_tests(unittest.TestCase):
    def setUp(self):
        self.in_dBs = [20., 30., 0.]
        self.double_dBs = [23.0103,33.0103, 3.0103]  #self.in_dBs keer 2
        self.summed_dB = 30.417873  # logaritsmische som van self,.in_dBs
        self.values = [100., 1000., 1.]
        
        self.in_dB_raw = self.in_dBs[0]
        self.value_raw = self.values[0]
        
        self.in_dB_df = pd.DataFrame(data={
                'col1': self.in_dBs,
                'col2': self.in_dBs
                })
        self.value_df= pd.DataFrame(data={
                'col1': self.values,
                'col2': self.values
                })

    def test_dB_to_value_raw(self):
        result = gs.dB_to_value(self.in_dB_raw)
        self.assertEqual(result, self.value_raw)

    def test_dB_to_value_df(self):
        result = gs.dB_to_value(self.in_dB_df) 
        assert_frame_equal(result, self.value_df)
    
    def test_value_to_dB_raw(self):  
        result = gs.value_to_dB(self.value_raw)
        self.assertEqual(result, self.in_dB_raw)
    
    def test_value_to_dB_df(self):  
        result = gs.value_to_dB(self.value_df) 
        assert_frame_equal(result, self.in_dB_df)
    
    def test_dB_sum_axis_0(self):
        
        result = gs.dB_sum(self.in_dB_df, axis = None)
        result_axis0 = gs.dB_sum(self.in_dB_df, axis = 0)
        
        
        expected = pd.Series(data={
                'col1': self.summed_dB,
                'col2': self.summed_dB
                })
        assert_series_equal(result, expected)
        assert_series_equal(result_axis0, expected)
        
    def test_dB_sum_axis_1(self):
        result = gs.dB_sum(self.in_dB_df, axis = 1)
        
        expected = pd.Series(data=self.double_dBs)
        assert_series_equal(result, expected)  
        
    def test_dB_add(self):
        result = gs.dB_add([self.in_dB_df, self.in_dB_df])
        
        expected = pd.DataFrame(data={
                'col1': self.double_dBs,
                'col2': self.double_dBs
                })
        assert_frame_equal(result, expected) 
        
    def test_dB_multiply(self):
        result = gs.dB_multiply(self.in_dB_df, 2.)
        
        expected = pd.DataFrame(data={
                'col1': self.double_dBs,
                'col2': self.double_dBs
                })
        assert_frame_equal(result, expected) 
    
    def test_Lp_direct_point(self):
        Lw = self.in_dB_df
        result = gs.Lp_direct_point(Lw, 1., 2.)
        Lps = [
                12.018201317,
                22.01820131792538,
                -7.981798682074618
                ]  #uit online calculator voor zekerheid
        expected = pd.DataFrame(data={
                'col1': Lps,
                'col2':Lps
                })
        assert_frame_equal(result, expected) 
        
        
class other_tests(unittest.TestCase):
    def setUp(self):
        self.dims = [1., 2., 3.6]
        self.area = 25.6
    def test_area_of_box(self):
        result = gs.area_of_box(self.dims[0], self.dims[1], self.dims[2])
        self.assertAlmostEqual(result, self.area)
    def test_area_of_box_list(self):
        result = gs.area_of_box(self.dims)
        self.assertAlmostEqual(result, self.area )
    def test_area_of_box_pd(self):
        series = pd.Series(self.dims)
        result = gs.area_of_box(series)
        self.assertAlmostEqual(result, self.area)
    def test_area_of_sphere(self):
        result = gs.area_of_sphere(2.5)
        expected =78.5398163
        self.assertAlmostEqual(result,expected)

        
if __name__ == '__main__':
    unittest.main()
