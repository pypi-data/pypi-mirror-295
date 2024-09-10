# Global variables will be assign in variables.py
from enum import Enum

# Set number of workers to use for concurrent async processing
import os

# TODO: Load env file if availabale
NUM_WORKERS = 4

# Set directory for logs
LOG_DIR = "nexusai_logs"

# Set log file size in MB
LOG_FILE_SIZE = 100

# Set log file backup count 
LOG_BACKUP_COUNT = 5

# Set maximum number of files size
MAX_FILE_SIZE_ALLOW = 5242880

# Module Constants
SUCCESS = "SUCESS"
FAILED = "FAILED"
INFO = "INFORMATION"
PROCESSING = "PROCESSING"
ERROR = "ERROR"
WARNING = "WARNING"

# Set OPENAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME","gpt-4-32k")
OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
OPENAI_DEPLOYMENT_VERSION = os.getenv("OPENAI_DEPLOYMENT_VERSION")
OPENAI_DEPLOYMENT_ENDPOINT = os.getenv("OPENAI_DEPLOYMENT_ENDPOINT")

# temportary need to be removed
os.environ["ALLOWED_FILE_TYPES"] = ".txt, .doc, .yaml, .docx, .pdf, .rtf, .html, .htm, .xml, .csv, .json, .md, .odt, .tex, .log, .ini, .asc"

# Set PostgreSQL configuration
POSTGRES_AUTOCOMMIT = True
POSTGRES_HOST = os.getenv("PGVECTOR_HOST")
POSTGRES_PORT = os.getenv("PGVECTOR_PORT")
POSTGRES_DB = os.getenv("PGVECTOR_DB")
POSTGRES_USER = os.getenv("PGVECTOR_USER")
POSTGRES_PASSWORD = os.getenv("PGVECTOR_PWD")

# Set AWS configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


# Set ENV
ENV = os.getenv("ENV")

ROOT_PATH = os.getenv("ROOT_PATH", "")

MAX_FILE_COUNT = os.getenv("MAX_FILE_COUNT", 10)

OLD_K_VALUE = 20

# Chunking Configuration
CHUNK_SIZE = 2000 
CHUNK_OVERLAP = int(CHUNK_SIZE * 0.10) # 10% of chunk size


# Retreiver Arguments
FETCH_K = 5
LAMBDA_MULT = 0.8

# Embedding Configuration
EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
AZURE_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")
BATCH_SIZE = 100




CONNECTION_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USER = os.getenv("REDIS_USER")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
# REDIS_INDEX =  os.getenv("REDIS_INDEX")
SCHEMA_NAME = os.getenv("REDIS_SCHEMA_NAME")

#adding vectordb here (Can modify accordingly between redis and pgvector )
vectordb='pgvector'

#adding parser here (Can modify accordingly between tika and UnstructuredFileLoader )
PARSER = 'unstructure'

#AWS SQS URL
QUEUE_URL = os.getenv("QUEUE_URL")


#Summary Constants
WORKERS_PER_CORE = 1
MAP_REDUCE_ALGORITHM = 'map_reduce'

REDUCE_TEMPLATE = """The following is set of summaries:
                                {doc_summaries}
                                As a professional summarizer, create a concise and comprehensive summary and title of the provided text, be it an article, post, conversation, or passage, while adhering to these guidelines:
                
                                1. Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness. Format the summary in paragraph form for easy understanding. Strictly on the provided text, without including external information. Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
                                2. Also generate a title that is descriptive, accurate, and reflective of the content.
                                3. Also generate the list key highlights that are being discussed in summary, maximum upto top 5 highlights.
                                4. Then generate the sentiment(positive, negative and neutral) on the given summary. 
                                5. Output format should be a json with first key as title, second key as summary, third key as highlights and value as in list, fourth key as sentiment. 
                                """

MAP_TEMPLATE = """The following is a set of documents
                            {docs}
                            As a professional summarizer, create a concise and comprehensive summary of the provided text, be it an article, post, conversation, or passage, while adhering to these guidelines:
                            1. Craft a summary that is detailed, thorough, in-depth, and complex, while maintaining clarity and conciseness.
                            2. Incorporate main ideas and essential information, eliminating extraneous language and focusing on critical aspects.
                            3. Strictly on the provided text, without including external information.
                            4. Format the summary in paragraph form for easy understanding." 
                            """

SUMMARY_CHUNK_SIZE = 2000
SUMMARY_CHUNK_OVERLAP = 100
