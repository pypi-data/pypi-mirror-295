import unittest
from TorturePhrases_Estimator import identify_tortured_phrases

class TestTorturePhrasesEstimator(unittest.TestCase):
    def test_identify_tortured_phrases(self):
        text = "We need to commence the project subsequent to our meeting."
        expected = ['commence instead of start', 'subsequent to instead of after']
        result = identify_tortured_phrases(text)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
