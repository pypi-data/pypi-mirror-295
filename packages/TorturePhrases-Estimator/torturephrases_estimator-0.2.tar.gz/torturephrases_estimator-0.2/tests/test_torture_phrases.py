import unittest
from TorturePhrases_Estimator import identify_tortured_phrases

class TestTorturePhrasesEstimator(unittest.TestCase):
    def test_identify_tortured_phrases(self):
        text = "Subjects were dichotomized into experimental contingents, with one contingent being administered the active pharmaceutical ingredient and the other contingent receiving a pharmacologically inert substance."
        result = identify_tortured_phrases(text)
        print(result)

if __name__ == '__main__':
    unittest.main()
