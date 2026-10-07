from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich import print

from config import settings

embedding_model = OpenAIEmbeddings(
    model=settings.OPEN_ROUTER_EMBEDDING_MODEL,
    api_key=settings.OPEN_ROUTER_API_KEY,
    base_url=settings.OPEN_ROUTER_BASE_URL,
)

loader = PyPDFLoader(file_path="chat_agent/test.pdf")

docs = loader.load()

# print(docs)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

chunks = splitter.split_documents(documents=docs)

# print(chunks)
vectore_store = FAISS.from_documents(documents=chunks, embedding=embedding_model)

print(vectore_store)

# vectore_store.save_local("chat_agent/faiss_index")

# retriever = vectore_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# result = retriever.invoke("What is Deep learning?")

# print(result)
