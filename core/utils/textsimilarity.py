from sentence_transformers import SentenceTransformer, util

ref_sentences = ['turn off the lights',
                 'turn off the kitchens lights', 'turn the kitchen lights off']


class TextSimilarity:
    # given a wav file and a hotword, return True if the hotword is detected using snowboy hotword detector
    def __init__(self, threshold=0.5):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self.model.encode(ref_sentences)
        self.threshold = threshold

    def detect(self, sentence):
        sentence_embedding = self.model.encode(sentence)
        print(util.cos_sim(sentence_embedding, self.embeddings))


if __name__ == "__main__":
    similarity = TextSimilarity()
    import time
    start = time.time()
    similarity.detect('turn off the kitchen lights')
    print(time.time() - start)
