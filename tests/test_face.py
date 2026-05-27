import sys
import os
import unittest
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.face_utils import validate_image, compare_embeddings

class TestFaceUtils(unittest.TestCase):

    def test_validate_image_missing_file(self):
        """Test that missing image returns invalid."""
        result = validate_image("nonexistent_path.jpg")
        self.assertFalse(result["valid"])

    def test_compare_embeddings_identical(self):
        """Test that identical vectors give similarity of 1.0."""
        vec1 = np.ones((1, 512), dtype='float32')
        vec2 = np.ones((1, 512), dtype='float32')
        # Normalize
        vec1 = vec1 / np.linalg.norm(vec1)
        vec2 = vec2 / np.linalg.norm(vec2)
        score = compare_embeddings(vec1, vec2)
        self.assertAlmostEqual(score, 1.0, places=3)

    def test_compare_embeddings_opposite(self):
        """Test that opposite vectors give similarity near -1.0."""
        vec1 =  np.ones((1, 512), dtype='float32')
        vec2 = -np.ones((1, 512), dtype='float32')
        vec1 = vec1 / np.linalg.norm(vec1)
        vec2 = vec2 / np.linalg.norm(vec2)
        score = compare_embeddings(vec1, vec2)
        self.assertAlmostEqual(score, -1.0, places=3)

if __name__ == "__main__":
    unittest.main()
