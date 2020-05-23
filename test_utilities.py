import utilities


class TestClass:
    test_input = "The quick brown fox jumps over the lazy dog."
    clf = utilities.classify_model()

    def test_setup_nltk(self):
        result = utilities.setup_nltk()
        assert result

    def test_parse_sentence_spacy(self):
        parsed, entities = utilities.parse_sentence_spacy(self.test_input)
        eles = {
            ("quick", "JJ", "amod", 1),
            ("brown", "JJ", "amod", 2),
            ("fox", "NN", "compound", 3),
            ("jumps", "NNS", "ROOT", 4),
            ("lazy", "JJ", "amod", 7),
            ("dog", "NN", "pobj", 8),
        }
        assert eles.issubset(set(parsed))
        assert entities == []

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
