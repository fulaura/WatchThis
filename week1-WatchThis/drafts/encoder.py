from time import sleep
from IPython.display import clear_output
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def generate_embedding_local(text:str) -> list[float]:
    if not text or not isinstance(text, str):  
        return []
    return model.encode(text).tolist()