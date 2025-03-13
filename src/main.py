
#	
# uvicorn , nginx 相关的东西部署后端服务；
# Batch , 异步等

import os
from loguru import logger
from dotenv import dotenv_values

# 如果你使用的是官方 langchain 包的老版本，下面的 import 不一定都能用
# 根据 DeprecationWarning，建议改成 langchain_community 下的对应类
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from langchain_community.document_loaders import TextLoader

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 如果要做 Web API
from langserve import add_routes
from fastapi import FastAPI

# 1) 先定义 BASE_DIR 指向当前文件所在的目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2) 正确加载 env 文件 (假设 .env 就放在项目根目录)
ENV_FILE = os.path.join(BASE_DIR, "..", ".env")
ENV_CONFIG = dotenv_values(ENV_FILE)

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple api server using Langchain's Runnable interfaces",
)

logger.info("init app succ")


def get_retriver() -> EnsembleRetriever:
    # 3) 构建 text.txt 的绝对路径
    text_path = os.path.join(BASE_DIR, "..", "data", "text.txt")
    text_loader = TextLoader(text_path, encoding="utf-8")
    text_docs = text_loader.load()

    # 4) embeddings 用 openai_api_key / openai_api_base
    embeddings = OpenAIEmbeddings(
        openai_api_key=ENV_CONFIG.get("OPENAI_API_KEY"),
        openai_api_base=ENV_CONFIG.get("OPENAI_API_BASE"),
    )

    vectorstore = FAISS.from_documents(text_docs, embeddings)
    bm25_retriever = BM25Retriever.from_documents(documents=text_docs, k=1)
    emb_retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, emb_retriever], weights=[0.5, 0.5]
    )
    return ensemble_retriever


def build_chain():
    template = """Answer the question based on the following context.

    {context}

    Question: {question}

    If context is not useful, answer the question directly and do not refer to context.
    """

    prompt = ChatPromptTemplate.from_template(template)

    # 这里也用 openai_api_key 和 openai_api_base
    model = ChatOpenAI(
        openai_api_key=ENV_CONFIG.get("OPENAI_API_KEY"),
        openai_api_base=ENV_CONFIG.get("OPENAI_API_BASE"),
    )

    retriver = get_retriver()
    chain = (
        {"context": retriver, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    return chain


def build_joke_chain():
    template = """帮我写一个关于{topic}的笑话"""
    prompt = ChatPromptTemplate.from_template(template)

    model = ChatOpenAI(
        openai_api_key=ENV_CONFIG.get("OPENAI_API_KEY"),
        openai_api_base=ENV_CONFIG.get("OPENAI_API_BASE"),
    )
    joke_chain = prompt | model | StrOutputParser()
    return joke_chain


def api():
    import uvicorn

    qa_chain = build_chain()
    add_routes(app, qa_chain, path="/qa")

    joke_chain = build_joke_chain()
    add_routes(app, joke_chain, path="/joke")

    uvicorn.run(app, host="localhost", port=8005)


def test():
    qa_chain = build_chain()
    logger.info(qa_chain.invoke("RAG的本质是什么？"))

    joke_chain = build_joke_chain()
    logger.info(joke_chain.invoke({"topic": "cat"}))


def main():
    # test()
    api()


if __name__ == "__main__":
    main()

