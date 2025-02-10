#from sentence_transformers import SentenceTransformer, util

# Load a lightweight Sentence-BERT model (MiniLM version)

def similarity(cover_letter, job_description):
	# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
	# # Get sentence embeddings for both texts
	# job_description_embedding = model.encode(job_description, convert_to_tensor=True)
	# cover_letter_embedding = model.encode(cover_letter, convert_to_tensor=True)
	# # Compute cosine similarity
	# similarity = util.pytorch_cos_sim(job_description_embedding, cover_letter_embedding)
	# return similarity.item()
	return None