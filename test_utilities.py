import utilities
import pytest


class TestClass:
    test_input = "The quick brown fox jumps over the lazy dog."
    clf = utilities.classify_model()

    def test_setup_nltk(self):
        result = utilities.setup_nltk()
        assert result

    @pytest.mark.skip(reason="No way of currently testing this")
    def test_parse_sentence(self):
        triples, root = utilities.parse_sentence(self.test_input)
        triples = list(triples)
        assert (("jumps", "VBZ"), "nsubj", ("fox", "NN")) in triples
        assert (("jumps", "VBZ"), "nmod", ("dog", "NN")) in triples
        assert root == "jumps"

    def test_classify_model(self):
        from features import features_dict
        import hashlib
        import numpy as np

        keys = [
            "id",
            "wordCount",
            "stemmedCount",
            "stemmedEndNN",
            "CD",
            "NN",
            "NNP",
            "NNPS",
            "NNS",
            "PRP",
            "VBG",
            "VBZ",
            "startTuple0",
            "endTuple0",
            "endTuple1",
            "endTuple2",
            "verbBeforeNoun",
            "qMark",
            "qVerbCombo",
            "qTripleScore",
            "sTripleScore",
            "class",
        ]
        sentence_id = hashlib.md5(str(self.test_input).encode("utf-8")).hexdigest()[:16]
        f = features_dict(sentence_id, self.test_input)
        features = [f[k] for k in keys][1:-1]
        features = np.array(features).reshape(1, -1)

        assert self.clf.predict(features)[0] == "S"

    def test_classify_sentence(self):
        result = utilities.classify_sentence(self.clf, self.test_input)
        assert result == "S"
