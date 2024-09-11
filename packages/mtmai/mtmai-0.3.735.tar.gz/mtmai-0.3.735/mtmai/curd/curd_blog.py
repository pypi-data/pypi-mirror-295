"""博客系统的 curd 操作"""

from pydantic import BaseModel
from sqlmodel import Session, select

from mtmai.llm.embedding import embedding_hf
from mtmai.models.blog import Post, PostBase
from mtmai.models.models import Document, DocumentIndex


class PostCreate(PostBase):
    content: str


async def create_blog_post(*, session: Session, blog_post_create: PostCreate) -> Post:
    input_data = PostCreate.model_validate(blog_post_create)

    # Create Document
    doc = Document(content=input_data.content)
    session.add(doc)
    session.flush()  # Flush to get the id without committing

    # Create DocumentIndex
    embedding_result = await embedding_hf(inputs=[input_data.content])
    doc_index = DocumentIndex(document_id=doc.id, embedding=embedding_result[0])
    session.add(doc_index)

    # Create Post
    new_blog_post = Post(title=input_data.title, doc_id=doc.id)
    session.add(new_blog_post)

    session.commit()
    session.refresh(new_blog_post)
    return new_blog_post


class DocumentQueryReq(BaseModel):
    query: str
    limit: int = 10
    offset: int = 0


async def document_query(session: Session, req: DocumentQueryReq) -> list[Document]:
    embedding_result = await embedding_hf(inputs=[req.query])
    query = (
        select(Document)
        .join(DocumentIndex, Document.id == DocumentIndex.document_id)
        .order_by(DocumentIndex.embedding.l2_distance(embedding_result[0]))
        .offset(req.offset)
        .limit(req.limit)
    )
    result = session.exec(query).all()
    return result
