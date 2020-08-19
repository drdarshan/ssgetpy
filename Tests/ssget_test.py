import unittest
import ssget as p

class TestPyUFGet(unittest.TestCase):
    def test_search_by_id(self):
        m = p.search(42)
        self.assertEqual(len(m), 1)
        self.assertEqual(m[0].id, 42)

    def test_search_by_group(self):
        matrices = p.search("HB/*")
        for matrix in matrices:
            self.assertEqual(matrix.group, "HB")
    
    def test_search_by_name(self):
        matrices = p.search("c-")
        self.assertTrue(len(matrices) > 0)
        for matrix in matrices:
            self.assertTrue(matrix.name.startswith("c-"))
    
    def test_filter_by_rows(self):
        matrices = p.search(rowbounds = (None, 1000))
        self.assertTrue(len(matrices) > 0)
        for matrix in matrices:
            self.assertTrue(matrix.rows <= 1000)

    def test_filter_by_shape(self):
        rmin = 50
        rmax = 1000
        cmin = 200
        cmax = 5000
        matrices = p.search(rowbounds = (rmin, rmax), colbounds=(cmin, cmax))
        self.assertTrue(len(matrices) > 0)
        for matrix in matrices:
            self.assertTrue(matrix.rows >= rmin and matrix.rows <= rmax and matrix.cols >= cmin and matrix.cols <= cmax)

    def test_filter_by_spd_true(self):
        matrices = p.search(isspd = True)
        self.assertTrue(len(matrices) > 0)
        for matrix in matrices:
            self.assertTrue(matrix.isspd)

    def test_filter_by_spd_false(self):
        matrices = p.search(isspd = False)
        self.assertTrue(len(matrices) > 0)
        for matrix in matrices:
            self.assertFalse(matrix.isspd)

if __name__ == "__main__":
    unittest.main()


