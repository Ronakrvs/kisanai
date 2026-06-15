import logging
from typing import Optional
import numpy as np

logger = logging.getLogger(__name__)

SYSTEM_PROMPT_HI = """आप KisanAI हैं — एक विशेषज्ञ कृषि सहायक जो भारतीय किसानों की मदद करता है।
आप हिंदी में उत्तर दें। संक्षिप्त और व्यावहारिक जानकारी दें।
केवल कृषि से संबंधित प्रश्नों का उत्तर दें।
"""

SYSTEM_PROMPT_EN = """You are KisanAI — an expert agriculture assistant helping Indian farmers.
Answer in English. Be concise and practical.
Only answer agriculture-related questions.
"""

FALLBACK_HI = "माफ करें, अभी इस प्रश्न का उत्तर देना संभव नहीं है। कृपया अपने स्थानीय कृषि अधिकारी से संपर्क करें।"
FALLBACK_EN = "Sorry, I couldn't answer this question right now. Please contact your local agriculture officer."


class RAGPipeline:
    def __init__(self, db_url: Optional[str], llm_model: str, embed_model: str):
        self.db_url = db_url
        self.llm_model = llm_model
        self.embed_model = embed_model
        self._embedder = None
        self._conn = None
        self._ollama = None

    def init(self):
        try:
            from sentence_transformers import SentenceTransformer
            self._embedder = SentenceTransformer(self.embed_model)
            logger.info(f"Loaded embedding model: {self.embed_model}")
        except Exception as e:
            logger.warning(f"Embedding model not loaded: {e}")

        if self.db_url:
            try:
                import psycopg2
                from pgvector.psycopg2 import register_vector
                self._conn = psycopg2.connect(self.db_url)
                register_vector(self._conn)
                logger.info("Connected to PostgreSQL with pgvector")
            except Exception as e:
                logger.warning(f"DB not connected: {e}")

        try:
            import ollama
            self._ollama = ollama
            logger.info(f"Ollama ready with model: {self.llm_model}")
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")

    def _embed(self, text: str) -> Optional[np.ndarray]:
        if self._embedder:
            return self._embedder.encode(text, normalize_embeddings=True)
        return None

    def _retrieve(self, query_embedding: np.ndarray, top_k: int = 3) -> list[str]:
        if not self._conn or query_embedding is None:
            return []
        try:
            with self._conn.cursor() as cur:
                cur.execute(
                    "SELECT content FROM knowledge_base ORDER BY embedding <=> %s::vector LIMIT %s",
                    (query_embedding.tolist(), top_k),
                )
                return [row[0] for row in cur.fetchall()]
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []

    def _generate(self, prompt: str, language: str) -> str:
        if not self._ollama:
            return FALLBACK_HI if language == "hi" else FALLBACK_EN

        system = SYSTEM_PROMPT_HI if language == "hi" else SYSTEM_PROMPT_EN
        try:
            response = self._ollama.chat(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
            )
            return response["message"]["content"]
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return FALLBACK_HI if language == "hi" else FALLBACK_EN

    def answer(self, question: str, language: str = "hi") -> str:
        embedding = self._embed(question)
        context_docs = self._retrieve(embedding) if embedding is not None else []

        if context_docs:
            context = "\n\n".join(context_docs)
            if language == "hi":
                prompt = f"संदर्भ:\n{context}\n\nप्रश्न: {question}"
            else:
                prompt = f"Context:\n{context}\n\nQuestion: {question}"
        else:
            prompt = question

        return self._generate(prompt, language)
