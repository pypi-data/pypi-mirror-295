import logging

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import Session, select

from mtmai.api.deps import CurrentUser, SessionDep
from mtmai.llm.embedding import embedding_hf
from mtmai.models.models import Document, DocumentBase

router = APIRouter()

logger = logging.getLogger()


# Properties to return via API, id is always required
class DocumentPublic(DocumentBase):
    id: str
    collection: str
    document: str


class DocumentResonse(BaseModel):
    data: list[DocumentPublic]
    count: int


async def doc_retrieval(db: Session, query: str):
    result = await embedding_hf(inputs=[query])
    docs = db.exec(
        select(Document).order_by(Document.embedding.l2_distance(result[0])).limit(5)
    ).all()
    return docs


class RagAddContentRes(DocumentBase):
    # success: bool = True
    pass


class RagAddContentReq(DocumentBase):
    pass


@router.post("", response_model=RagAddContentRes)
async def add_content(
    db: SessionDep, current_user: CurrentUser, item_in: RagAddContentReq
):
    item = DocumentBase.model_validate(item_in, update={"owner_id": current_user.id})
    result = await embedding_hf(inputs=[item.document])
    item = Document(
        document=item_in.document, embedding=result[0], owner_id=current_user.id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# class RagRetrievalReq(BaseModel):
#     collection: str | None
#     query: str
#     limit: int = Field(10, le=100)  # 设置最大值为 100


# @router.post("/query", response_model=DocumentResonse)
# async def query_doc(db: SessionDep, req: RagRetrievalReq):
#     result = await embedding_hf(inputs=[req.query])
#     docs = db.exec(
#         select(Document)
#         .order_by(Document.embedding.l2_distance(result[0]))
#         .limit(req.limit)
#     ).all()
#     return DocumentResonse(data=docs, count=len(docs))


# def hello_pg_vetor():
#     # loader = TextLoader("state_of_the_union.txt")
#     loader = WebBaseLoader("https://www.espn.com/")
#     documents = loader.load()
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     docs = text_splitter.split_documents(documents)

#     embeddings = get_embeding_llm()
#     connection_string = settings.DATABASE_URL
#     collection_name = "state_of_the_union"

#     db = PGEmbedding.from_documents(
#         embedding=embeddings,
#         documents=docs,
#         collection_name=collection_name,
#         connection_string=connection_string,
#     )

#     query = "What did the president say about Ketanji Brown Jackson"
#     docs_with_score: list[tuple[Document, float]] = db.similarity_search_with_score(
#         query
#     )

#     for doc, score in docs_with_score:
#         print("-" * 80)
#         print("Score: ", score)
#         print(doc.page_content)
#         print("-" * 80)

#     return json.dumps(jsonable_encoder(docs_with_score))
