import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from langchain_community.document_loaders import DirectoryLoader, S3DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings, BedrockEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
import os
import json
import uuid
from typing import List, Tuple
from loguru import logger

class RAGSemanticSearch:
    def __init__(self, path: str, mode: str = "local", region_name: str = None, huggingface_api_token: str = None):
        self.path = path
        self.mode = mode
        self.region_name = region_name
        self.huggingface_api_token = huggingface_api_token
        
        if self.mode == "local" and not self.huggingface_api_token:
            raise ValueError("HuggingFace API token is required when using local mode")
        
        self.session = self._create_session() if self.mode == "aws" else None
        self.bedrock_client = self.session.client(service_name="bedrock-runtime") if self.mode == "aws" else None
        
        self.docs = self._load_and_process_documents()
        self.collection_name = self._get_collection_name()
        self.persistent_client = self._create_and_populate_collection()
        self.db = self._create_chroma_db()

    def _create_session(self):
        try:
            if self.region_name:
                return boto3.Session(region_name=self.region_name)
            else:
                return boto3.Session()
        except (NoCredentialsError, PartialCredentialsError) as e:
            logger.error(f"AWS credential error: {str(e)}")
            raise ValueError("AWS credentials not found or incomplete. Please ensure your credentials are properly configured.")

    def _get_collection_name(self):
        if self.mode == "aws":
            bucket_name = self.path.split('/')[0]
            return f"collection_{bucket_name.replace('-', '_')}"
        return "local_collection"

    def _load_and_process_documents(self) -> List:
        try:
            if self.mode == "aws":
                loader = S3DirectoryLoader(self.path)
            else:
                loader = DirectoryLoader(self.path, glob="**/*.txt")
            
            chunk_size = 2000
            chunk_overlap = 60
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            documents = loader.load()
            return text_splitter.split_documents(documents)
        except Exception as e:
            logger.error(f"Error loading documents: {str(e)}")
            raise

    def _create_and_populate_collection(self) -> chromadb.PersistentClient:
        try:
            persistent_client = chromadb.PersistentClient(path="./chromadb", settings=Settings(allow_reset=True))
            
            if self.mode == "aws":
                embedding_function = BedrockEmbeddings(
                    model_id="cohere.embed-english-v3",
                    client=self.bedrock_client
                )
            else:
                embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            
            collection = persistent_client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
                embedding_function=embedding_function
            )

            for doc in self.docs:
                collection.add(
                    ids=[str(uuid.uuid1())], metadatas=[doc.metadata], documents=[doc.page_content]
                )
            
            return persistent_client
        except Exception as e:
            logger.error(f"Error creating and populating collection: {str(e)}")
            raise

    def _create_chroma_db(self) -> Chroma:
        try:
            if self.mode == "aws":
                embedding_function = BedrockEmbeddings(
                    model_id="cohere.embed-english-v3",
                    client=self.bedrock_client
                )
            else:
                embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            
            return Chroma(
                client=self.persistent_client,
                collection_name=self.collection_name,
                embedding_function=embedding_function,
            )
        except Exception as e:
            logger.error(f"Error creating Chroma DB: {str(e)}")
            raise

    def get_similar_docs(self, query: str, k: int = 5) -> List[Tuple]:
        try:
            return self.db.similarity_search_with_relevance_scores(query, k=k)
        except Exception as e:
            logger.error(f"Error getting similar docs: {str(e)}")
            raise

    def model_invoke(self, prompt: str) -> str:
        try:
            if self.mode == "aws":
                body = json.dumps({
                    "messages": [
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": prompt}],
                        }
                    ],
                    "max_tokens": 2000,
                    "top_p": 0.2,
                    "temperature": 0,
                    "anthropic_version": "bedrock-2023-05-31"
                })

                modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
                accept = "application/json"
                contentType = "application/json"

                response = self.bedrock_client.invoke_model(
                    body=body,
                    modelId=modelId,
                    accept=accept,
                    contentType=contentType
                )
                return json.loads(response.get('body').read())['content'][0]['text']
            else:
                llm = HuggingFaceHub(
                    repo_id="google/flan-t5-xxl",
                    model_kwargs={"temperature": 0.5, "max_length": 512},
                    huggingfacehub_api_token=self.huggingface_api_token
                )
                return llm(prompt)
        except Exception as e:
            logger.error(f"Error invoking model: {str(e)}")
            raise

    def get_answer(self, question: str, context: str) -> str:
        prompt_template = f"""Answer the question based on the context below. If the question cannot be answered based on the context, say "I don't know."

        Context: {context}

        Question: {question}

        Answer:"""

        return self.model_invoke(prompt_template)

    def semantic_search(self, question: str) -> List[Tuple]:
        return self.get_similar_docs(question, k=5)

    def rag_with_sources(self, question: str) -> Tuple[str, List[str]]:
        try:
            similar_docs = self.semantic_search(question)
            context = "\n\n".join([doc[0].page_content for doc in similar_docs])
            
            answer = self.get_answer(question, context)
            sources = [doc[0].metadata['source'] for doc in similar_docs]

            return answer, sources
        except Exception as e:
            logger.error(f"Error in RAG with sources: {str(e)}")
            raise

    def _get_user_friendly_error(self, error):
        if isinstance(error, ValueError):
            return str(error)
        elif isinstance(error, boto3.exceptions.Boto3Error):
            return "An error occurred with the AWS service. Please check your AWS resources and permissions."
        else:
            return f"An unexpected error occurred: {str(error)}."