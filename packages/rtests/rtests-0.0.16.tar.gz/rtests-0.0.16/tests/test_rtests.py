import os
os.environ['R_HOME'] = r'C:\Program Files\R\R-4.3.1'

import unittest
import rtests



class TestRTests(unittest.TestCase):
    def test_r_wilcoxsign_test(self):
        a = [6.0, 4.0, 5.0, 5.0, 7.0, 6.0, 6.0, 6.0, 7.0, 6.0, 6.0, 5.0, 6.0, 6.0, 5.0, 5.0, 3.0, 6.0, 6.0, 5.0, 6.0,
             5.0, 4.0, 6.0, 6.0, 6.0, 7.0, 4.0, 3.0, 4.0, 6.0, 6.0, 5.0, 6.0, 4.0, 6.0, 6.0, 5.0, 7.0, 6.0, 6.0, 5.0,
             6.0, 7.0, 6.0, 6.0, 6.0, 5.0, 7.0, 7.0]
        b = [5.0, 3.0, 5.0, 3.0, 5.0, 3.0, 6.0, 2.0, 3.0, 6.0, 2.0, 5.0, 5.0, 6.0, 4.0, 6.0, 4.0, 5.0, 5.0, 3.0, 7.0,
             5.0, 6.0, 6.0, 4.0, 3.0, 4.0, 3.0, 2.0, 4.0, 5.0, 4.0, 4.0, 6.0, 2.0, 6.0, 7.0, 4.0, 4.0, 5.0, 5.0, 5.0,
             5.0, 7.0, 4.0, 5.0, 3.0, 2.0, 6.0, 7.0]

        r = rtests.r_wilcoxsign_test(a, b, print_result=True)

        """Test1 Result:

                Wilcoxon signed rank test with continuity correction
            
            data:  c(6, 4, 5, 5, 7, 6, 6, 6, 7, 6, 6, 5, 6, 6, 5, 5, 3, 6, 6, 5, 6, 5, 4, 6, 6, 6, 7, 4, 3, 4, 6, 6, 5, 
            6, 4, 6, 6, 5, 7, 6, 6, 5, 6, 7, 6, 6, 6, 5, 7, 7) and c(5, 3, 5, 3, 5, 3, 6, 2, 3, 6, 2, 5, 5, 6, 4, 6, 4, 
            5, 5, 3, 7, 5, 6, 6, 4, 3, 4, 3, 2, 4, 5, 4, 4, 6, 2, 6, 7, 4, 4, 5, 5, 5, 5, 7, 4, 5, 3, 2, 6, 7)
            V = 636.5, p-value = 1.167e-05
            alternative hypothesis: true location shift is not equal to 0
            
            
            Test2 Result:
            
                Exact Wilcoxon-Pratt Signed-Rank Test
            
            data:  y by x (pos, neg) 
                 stratified by block
            Z = 4.5276, p-value = 1.474e-06
            alternative hypothesis: true mu is not equal to 0"""

        assert r["p_value"] == 1.167e-05

    def test_mannwhitney_u(self):
        a = [5, 2, 1, 3, 6, 2, 2, 4, 1, 2, 7, 3, 7, 2, 7, 5, 1, 4, 5, 1, 1, 4, 5, 2, 1, 1, 7, 2, 3, 2, 2, 1, 4, 5,
                  2, 5, 4, 1, 5, 2, 2, 2, 6, 4, 3, 2, 6, 5, 5, 6]
        b = [5, 2, 1, 3, 7, 2, 2, 4, 1, 2, 6, 3, 7, 2, 7, 5, 1, 5, 5, 2, 2, 4, 4, 4, 3, 2, 7, 3, 3, 3, 2, 4, 3, 5,
                  2, 6, 4, 1, 3, 2, 2, 2, 6, 5, 3, 3, 5, 6, 6, 7]
        rtests.r_mannwhitneyu_test(a, b, print_result=True)