
import unittest
import numpy as np

from PygameVisualizer import PygameVisualizer

class TestPygameVisualizer(unittest.TestCase):

    def test_blit(self):
        visualizer = PygameVisualizer().open()
        array = np.random.rand(80, 80, 3)*500
        print(np.max(array))
        with self.assertRaises(ValueError):
            visualizer.blit(array)
        visualizer.close()
            
        
if __name__ == '__main__':
    unittest.main()