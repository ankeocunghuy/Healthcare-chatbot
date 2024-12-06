import numpy as np
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams


class RAGModel:
    def __init__(self, embedding_model_name, documents, qdrantClient):
        """# Initialize the TextEmbedding model from fastembed"""
        self.model = TextEmbedding(model_name=embedding_model_name)
        self.documents = documents
        # self.qdrant_client = QdrantClient(":memory:")  # Use in-memory for quick setup (or use a persistent URL)
        
        self.qdrant_client = qdrantClient
        self.collection_name = "document_embeddings"
        
        # Create a Qdrant collection for vector search
        if self.qdrant_client.collection_exists(collection_name=self.collection_name):
            self.qdrant_client.delete_collection(collection_name=self.collection_name)

        self.qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),  # Adjust size based on embedding dims
        )
        
        self.create_qdrant_index()
    
    def create_qdrant_index(self):
        """ Generate embeddings using fastembed """
        embeddings = list(self.model.embed(self.documents))  # Convert generator to list
        embeddings = np.array(embeddings)  # Convert list to NumPy array
        
        # Insert embeddings and documents into Qdrant
        vectors = [embedding.tolist() for embedding in embeddings]
        payloads = [{"document": doc} for doc in self.documents]
        
        self.qdrant_client.upload_collection(
            collection_name=self.collection_name,
            vectors=vectors,
            payload=payloads,
            ids=None  
        )
    
    def retrieve_similar_docs(self, query, k=5, score_threshold=0.8):
        """ Retrieve k most similar doc with similar score >= score_threshold """

        query_emb = list(self.model.embed([query]))[0]  # Get embedding for the query
        
        # Search for the most similar documents in Qdrant
        search_result = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_emb.tolist(),
            score_threshold=score_threshold,
            limit=k
        )
        
        docs = [hit.payload["document"] for hit in search_result]
        return docs 

    
    def generate_relevant_context(self, query):
        """# Retrieve relevant context with query from source """
        docs = self.retrieve_similar_docs(query, 10, 0.6)
        context = "\n".join(docs)
        return context