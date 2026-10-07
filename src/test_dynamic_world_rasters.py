"""Small synthetic fixtures exercise real nodata hazards; they are not source images."""
import unittest
import numpy as np
from validate_dynamic_world_rasters import check_bands, safe_transition


def bands():
    b=np.zeros((12,2,2),dtype=np.float32)
    b[6]=.7;b[7]=.3;b[9]=4;b[10]=.7;b[11]=6
    return b


class ValidityTests(unittest.TestCase):
    def test_nan_border_and_finite_outside_region_cannot_be_water(self):
        a=bands();b=bands();a[:,0,0]=np.nan
        region=np.array([[True,True],[True,False]])
        sa,_=check_bands(a,region);sb,_=check_bands(b,region)
        codes,mask=safe_transition(a,b,sa,sb)
        self.assertEqual(codes[0,0],255);self.assertEqual(codes[1,1],255)
        self.assertEqual(int(mask.sum()),2)

    def test_low_confidence_unknown_and_no_observation_are_not_bare(self):
        a=bands();b=bands();b[9,0,0]=2;b[6,1,0]=.59;b[7,1,0]=.41;b[10,1,0]=.59
        region=np.ones((2,2),dtype=bool)
        sa,_=check_bands(a,region);sb,_=check_bands(b,region)
        codes,mask=safe_transition(a,b,sa,sb)
        self.assertEqual(codes[0,0],255);self.assertEqual(codes[1,0],255)
        self.assertEqual(int(mask.sum()),2)

    def test_probability_precision_and_wrong_exported_labels(self):
        b=bands();b[7]+=.00006
        _,r=check_bands(b,np.ones((2,2),dtype=bool))
        self.assertGreater(r['probability_sum_max_absolute_deviation'],0)
        b[11]=7
        with self.assertRaises(ValueError):check_bands(b,np.ones((2,2),dtype=bool))

    def test_negative_probability_wrong_confidence_and_invalid_sum(self):
        for change in [('probability',-1),('confidence',.9),('sum',.5)]:
            b=bands()
            if change[0]=='probability':b[0]=change[1]
            elif change[0]=='confidence':b[10]=change[1]
            else:b[7]=change[1]
            with self.assertRaises(ValueError):check_bands(b,np.ones((2,2),dtype=bool))


if __name__=='__main__':unittest.main()
