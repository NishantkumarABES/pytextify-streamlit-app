from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
# import gensim
# from gensim import corpora

# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt_tab')
def get_video_id(url):
    return extract.video_id(url)

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



def is_valid_email(email):
    if '@' not in email or email.startswith('@') or email.endswith('@'):
        return False
    local_part, domain_part = email.split('@')
    if not local_part or not domain_part:
        return False
    if '.' not in domain_part or domain_part.startswith('.') or domain_part.endswith('.'):
        return False
    if len(local_part) > 64 or len(domain_part) > 255:
        return False
    return True