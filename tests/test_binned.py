#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_binned
----------------------------------

Tests for TOPAS binned reading.
"""

# system imports
import unittest
import os.path

# third-party imports
from numpy.testing import assert_array_almost_equal

# project imports
from topas2numpy import BinnedResult


data_dir = 'tests/data'
dose_path = os.path.join(data_dir, 'Dose.csv')
ntracks_path = os.path.join(data_dir, 'SurfaceTracks.csv')


class Test1D(unittest.TestCase):
    def setUp(self):
        self.result = BinnedResult(dose_path)

    def test_quantity(self):
        assert self.result.quantity == 'DoseToWaterBinned'
        assert self.result.unit == 'Gy'

    def test_dimensions(self):
        assert len(self.result.dimensions) == 3
        assert self.result.dimensions[0].name == 'X'
        assert self.result.dimensions[1].name == 'Y'
        assert self.result.dimensions[2].name == 'Z'
        assert self.result.dimensions[0].unit == 'cm'
        assert self.result.dimensions[1].unit == 'cm'
        assert self.result.dimensions[2].unit == 'cm'
        assert self.result.dimensions[0].n_bins == 1
        assert self.result.dimensions[1].n_bins == 1
        assert self.result.dimensions[2].n_bins == 300
        assert self.result.dimensions[0].bin_width == 10.2
        assert self.result.dimensions[1].bin_width == 10.2
        assert self.result.dimensions[2].bin_width == 0.1

    def test_data(self):
        assert len(self.result.statistics) == 1
        assert self.result.statistics[0] == 'Sum'
        assert len(self.result.data) == 1
        data = self.result.data['Sum']
        assert data.shape[0] == self.result.dimensions[0].n_bins
        assert data.shape[1] == self.result.dimensions[1].n_bins
        assert data.shape[2] == self.result.dimensions[2].n_bins


class Test2D(unittest.TestCase):
    def setUp(self):
        self.result = BinnedResult(ntracks_path)

    def test_quantity(self):
        assert self.result.quantity == 'SurfaceTrackCount'
        assert self.result.unit is None

    def test_dimensions(self):
        assert len(self.result.dimensions) == 3
        assert self.result.dimensions[0].name == 'X'
        assert self.result.dimensions[1].name == 'Y'
        assert self.result.dimensions[2].name == 'Z'
        assert self.result.dimensions[0].unit == 'cm'
        assert self.result.dimensions[1].unit == 'cm'
        assert self.result.dimensions[2].unit == 'cm'
        assert self.result.dimensions[0].n_bins == 10
        assert self.result.dimensions[1].n_bins == 10
        assert self.result.dimensions[2].n_bins == 1
        assert self.result.dimensions[0].bin_width == 6
        assert self.result.dimensions[1].bin_width == 6
        assert self.result.dimensions[2].bin_width == 60

    def test_data(self):
        assert len(self.result.statistics) == 1
        assert self.result.statistics[0] == 'Sum'
        assert len(self.result.data) == 1
        data = self.result.data['Sum']
        assert data.shape[0] == self.result.dimensions[0].n_bins
        assert data.shape[1] == self.result.dimensions[1].n_bins
        assert data.shape[2] == self.result.dimensions[2].n_bins


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
