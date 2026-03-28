from nltk.tokenize import sent_tokenize

def summarize_text(text, num_sentences=5):
    sentences = sent_tokenize(text)
    
    # filter small/noisy sentences
    sentences = [s for s in sentences if len(s) > 40]
    
    return " ".join(sentences[:num_sentences])
    