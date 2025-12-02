"""
Knowledge base system for storing and retrieving email classification context
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions


class KnowledgeBase:
    """
    Vector-based knowledge base for storing product information,
    common queries, and historical classification data
    """

    def __init__(self, persist_directory: str = "./data/knowledge_base"):
        """
        Initialize the knowledge base with ChromaDB

        Args:
            persist_directory: Directory to persist the vector database
        """
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )

        # Use default embedding function (all-MiniLM-L6-v2)
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()

        # Initialize collections
        self._init_collections()

    def _init_collections(self):
        """Initialize the different collections for knowledge storage"""
        # Product information collection
        self.products_collection = self.client.get_or_create_collection(
            name="products",
            embedding_function=self.embedding_function,
            metadata={"description": "Penta Fine Ingredients product catalog"}
        )

        # Common queries and responses collection
        self.queries_collection = self.client.get_or_create_collection(
            name="common_queries",
            embedding_function=self.embedding_function,
            metadata={"description": "Common customer queries and classifications"}
        )

        # Historical classifications collection
        self.history_collection = self.client.get_or_create_collection(
            name="classification_history",
            embedding_function=self.embedding_function,
            metadata={"description": "Historical email classifications for learning"}
        )

    def add_product(self, product_id: str, name: str, description: str,
                   category: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Add product information to the knowledge base

        Args:
            product_id: Unique product identifier
            name: Product name
            description: Product description
            category: Product category
            metadata: Additional product metadata
        """
        doc_metadata = {
            "product_id": product_id,
            "name": name,
            "category": category,
            **(metadata or {})
        }

        self.products_collection.add(
            documents=[f"{name}: {description}"],
            metadatas=[doc_metadata],
            ids=[product_id]
        )

    def add_common_query(self, query_id: str, query_text: str,
                        classification: str, confidence: float,
                        metadata: Optional[Dict[str, Any]] = None):
        """
        Add a common query pattern to the knowledge base

        Args:
            query_id: Unique query identifier
            query_text: The query text
            classification: The classification category
            confidence: Confidence score
            metadata: Additional metadata
        """
        doc_metadata = {
            "query_id": query_id,
            "classification": classification,
            "confidence": confidence,
            "added_at": datetime.now().isoformat(),
            **(metadata or {})
        }

        self.queries_collection.add(
            documents=[query_text],
            metadatas=[doc_metadata],
            ids=[query_id]
        )

    def add_classification_history(self, email_id: str, email_content: str,
                                   classification: str, confidence: float,
                                   was_correct: Optional[bool] = None,
                                   metadata: Optional[Dict[str, Any]] = None):
        """
        Add a historical classification to the knowledge base

        Args:
            email_id: Unique email identifier
            email_content: Email content (subject + body)
            classification: Classification category
            confidence: Confidence score
            was_correct: Whether the classification was correct (from feedback)
            metadata: Additional metadata
        """
        doc_metadata = {
            "email_id": email_id,
            "classification": classification,
            "confidence": confidence,
            "was_correct": was_correct,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {})
        }

        self.history_collection.add(
            documents=[email_content],
            metadatas=[doc_metadata],
            ids=[email_id]
        )

    def search_products(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant products based on query

        Args:
            query: Search query
            n_results: Number of results to return

        Returns:
            List of relevant products with metadata
        """
        try:
            results = self.products_collection.query(
                query_texts=[query],
                n_results=n_results
            )

            if not results["documents"][0]:
                return []

            return [
                {
                    "document": doc,
                    "metadata": meta,
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ]
        except Exception as e:
            print(f"Error searching products: {e}")
            return []

    def search_similar_queries(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar historical queries

        Args:
            query: Query text
            n_results: Number of results to return

        Returns:
            List of similar queries with their classifications
        """
        try:
            results = self.queries_collection.query(
                query_texts=[query],
                n_results=n_results
            )

            if not results["documents"][0]:
                return []

            return [
                {
                    "document": doc,
                    "metadata": meta,
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ]
        except Exception as e:
            print(f"Error searching queries: {e}")
            return []

    def search_classification_history(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search classification history for similar emails

        Args:
            query: Query text
            n_results: Number of results to return

        Returns:
            List of similar historical classifications
        """
        try:
            results = self.history_collection.query(
                query_texts=[query],
                n_results=n_results
            )

            if not results["documents"][0]:
                return []

            return [
                {
                    "document": doc,
                    "metadata": meta,
                    "distance": dist
                }
                for doc, meta, dist in zip(
                    results["documents"][0],
                    results["metadatas"][0],
                    results["distances"][0]
                )
            ]
        except Exception as e:
            print(f"Error searching history: {e}")
            return []

    def get_context_for_classification(self, email_content: str) -> Dict[str, Any]:
        """
        Get relevant context from knowledge base for email classification

        Args:
            email_content: Email content to classify

        Returns:
            Dictionary with relevant context from all collections
        """
        return {
            "similar_queries": self.search_similar_queries(email_content, n_results=3),
            "relevant_products": self.search_products(email_content, n_results=3),
            "similar_history": self.search_classification_history(email_content, n_results=3)
        }

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about the knowledge base"""
        return {
            "total_products": self.products_collection.count(),
            "total_queries": self.queries_collection.count(),
            "total_history": self.history_collection.count()
        }
