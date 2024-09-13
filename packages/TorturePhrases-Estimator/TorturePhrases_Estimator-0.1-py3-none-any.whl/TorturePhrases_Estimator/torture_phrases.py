import os

class TorturePhrasesEstimator:
    def __init__(self):
        self.tortured_phrases = self.load_tortured_phrases()

    def load_tortured_phrases(self):
        """Load the list of tortured phrases from the text file."""
        file_path = os.path.join(os.path.dirname(__file__), "tortured_phrases_list.txt")
        with open(file_path, "r") as f:
            return [line.strip().lower() for line in f if line.strip()]

    def identify_tortured_phrases(self, text):
        """Identify and count tortured phrases in the provided text."""
        found_phrases = []
        lower_text = text.lower()

        for phrase in self.tortured_phrases:
            if phrase in lower_text:
                found_phrases.append(phrase)

        return found_phrases, len(found_phrases)

def identify_tortured_phrases(text):
    """Wrapper function to directly check tortured phrases."""
    estimator = TorturePhrasesEstimator()
    return estimator.identify_tortured_phrases(text)
