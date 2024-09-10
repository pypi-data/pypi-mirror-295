from collections import defaultdict
import re

def tfidf(id_terms, cat_product_count_filtered):	
	term_max_freq = defaultdict(int)
	for terms_count in id_terms.values():
		for term, frequency in terms_count.items():
				term_max_freq[term] = max(term_max_freq[term],frequency)
	tf = {}
	idf = {}
	for cat_id, terms_count in id_terms.items():
		tf[cat_id] = {term:frequency/cat_product_count_filtered[cat_id] for term,frequency in terms_count.items()}
		idf[cat_id] = {term:frequency/term_max_freq[term] for term,frequency in terms_count.items()}
	del term_max_freq
	tf = {cat_id : tf_within_cat for cat_id,tf_within_cat in tf.items() if tf_within_cat}
	idf = {cat_id : idf_cat for cat_id,idf_cat in idf.items() if idf_cat}	
	tf_idf = {cat_id: {term:(tf[cat_id][term] + idf[cat_id][term]) for term in terms_count} for cat_id,terms_count in id_terms.items()}
	del tf
	del idf
	tf_idf = {cat_id : term_freq for cat_id,term_freq in tf_idf.items() if term_freq}	
	del id_terms
	term_max_tfidf = defaultdict(int)
	for terms_count in tf_idf.values():
		for term, frequency in terms_count.items():
				term_max_tfidf[term] = max(term_max_tfidf[term],frequency)
	tf_idf = {cat_id : {term:round(100*term_freq/term_max_tfidf[term],2) for term , term_freq in term_freq.items()} for cat_id,term_freq in tf_idf.items()}	
	tf_idf = {cat_id : {term:score for term , score in term_freq.items() if score>1} for cat_id,term_freq in tf_idf.items()}	
	return(tf_idf)

def create_cbow(docs):
	indexes = defaultdict(set)
	dlist = list(docs.items())
	for _id, doc in dlist:
		for word in doc:
			indexes[word].add(_id)	
	return indexes
	
def clean_input(input_text):
	text = " ".join(input_text)
	text = text.replace('..','.').replace('. ', ' ').replace("- "," ").replace(" -"," ")
	text = re.sub(r"\s+"," ", text, flags = re.I)
	text = re.sub(r'([a-z])\1+', r'\1\1', text)
	text = re.sub(r'[,:;{}?!/_\$@<>()\\#%+=\[\]\']', ' ',text)
	text = " ".join([t.replace('"',' inch') if t.replace(".","").replace('"','').isnumeric() else t for t in text.split()])		
	text = re.sub(r'[^a-z0-9.*\- ]', '', text)	
	text = text.rstrip('.')	
	text = " ".join([t.replace("."," ") if t.replace(".","").isalpha() else t for t in text.split()])
	text = " ".join([t.replace("-"," ") if t.replace("-","").isalnum() else t for t in text.split()])
	text = " ".join([t.replace("*","x") if t.replace(".","").replace("*","").isnumeric() else t.replace("*","") for t in text.split()])
	text = text.split()
	return text	