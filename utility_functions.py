import pytube.extract
from youtube_transcript_api import YouTubeTranscriptApi
import pytube
# import gensim
# from gensim import corpora

# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt_tab')
def get_video_id(url):
    id = pytube.extract.video_id(url)
    return id

def extract_transcript_from_youtube(youtube_url):
    video_id = get_video_id(youtube_url)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = "\n".join([t['text'] for t in transcript])
    return transcript_text



def topic_modelling(structured_text):
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in word_tokenize(structured_text.lower()) if word.isalpha() and word not in stop_words]
    # Create a dictionary and corpus
    dictionary = corpora.Dictionary([tokens])
    corpus = [dictionary.doc2bow([token]) for token in tokens]
    # Train the LDA model
    lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15)
    # Output the topics
    topics = lda_model.print_topics()
    return topics

