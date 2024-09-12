"""
博客系统api
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

from mtmai.api.deps import SessionDep
from mtmai.core.db import get_session
from mtmai.curd.curd_blog import create_blog_post
from mtmai.models.blog import Post, PostBase
from mtmai.models.models import Document

router = APIRouter()


class BlogPostItem(PostBase):
    id: str

    pass


class BlogPostListResponse(BaseModel):
    data: list[BlogPostItem]
    count: int


@router.get("/items", response_model=BlogPostListResponse)
async def post_list(
    *,
    db: Session = Depends(get_session),
    query: str = Query(default=""),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    if query:
        # 如果有查询字符串，执行向量搜索
        vector_search_query = (
            select(Document.id)
            .order_by(Document.embedding.l2_distance(query))
            .limit(limit * 2)
        )
        relevant_doc_ids = db.exec(vector_search_query).all()

        # 然后使用这些ID来获取完整的博客文章信息
        joined_query = (
            select(Document, Post)
            .join(Post, Document.id == Post.doc_id)
            .where(Document.id.in_(relevant_doc_ids))
            .offset(offset)
            .limit(limit)
        )
    else:
        # 如果没有查询字符串，返回最新的博客文章
        joined_query = (
            select(Document, Post)
            .join(Post, Document.id == Post.doc_id)
            .order_by(Post.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

    results = db.exec(joined_query).all()

    posts = [
        BlogPostItem(id=post.id, title=post.title or "", content=doc.content or "")
        for doc, post in results
    ]

    return BlogPostListResponse(data=posts, count=len(posts))


class BlogPostCreateReq(BaseModel):
    title: str
    content: str
    tags: list[str] = []


class BlogPostCreateRes(BaseModel):
    id: str


@router.post("/", response_model=BlogPostCreateRes)
async def post_create(
    *,
    db: SessionDep,
    req: BlogPostCreateReq,
):
    return create_blog_post(session=db, blog_post_create=req)


class BlogPostUpdateReq(BaseModel):
    title: str
    content: str


class BlogPostUpdateRes(BaseModel):
    id: str


@router.put("/{post_id}", response_model=BlogPostUpdateRes)
async def blog_post_update(
    *,
    post_id: str,
    db: Session = Depends(get_session),
    req: BlogPostUpdateReq,
):
    blog_post = db.exec(select(Post).where(Post.id == post_id)).one()
    if not blog_post:
        raise HTTPException(status_code=404)

    blog_post.title = req.title

    # 更新内容
    if blog_post.content_id:
        blog_post_content = db.exec(
            select(Document).where(Document.id == blog_post.content_id)
        ).one_or_none()
    else:
        blog_post_content = None

    if not blog_post_content:
        blog_post_content = Document(content=req.content)
        db.add(blog_post_content)
        db.commit()
        db.refresh(blog_post_content)
        blog_post.content_id = blog_post_content.id
    else:
        blog_post_content.content = req.content

    db.add(blog_post)
    db.add(blog_post_content)
    db.commit()
    return BlogPostUpdateRes(id=blog_post.id)


class BlogPostDetailResponse(BaseModel):
    id: str
    title: str
    content: str
    tags: list[str]
    author_id: str | None
    author_avatar: str | None
    author_email: str | None
    author_website: str | None
    author_bio: str | None
    author_location: str | None
    author_company: str | None
    author_job_title: str | None
    author_skills: list[str] | None
    author_interests: list[str] | None
    author_hobbies: list[str] | None
    author_languages: list[str] | None
    author_languages_level: list[str] | None


@router.get("/{post_id}", response_model=BlogPostDetailResponse)
async def get_post_detail(
    *,
    post_id: str,
    db: Session = Depends(get_session),
):
    """获取 Post 详细完整信息"""
    blog_post = db.exec(select(Post).where(Post.id == post_id)).one_or_none()
    if not blog_post:
        raise HTTPException(status_code=404, detail="Post not found")

    blog_post_content = db.exec(
        select(Document).where(Document.id == blog_post.doc_id)
    ).one_or_none()
    if not blog_post_content:
        raise HTTPException(status_code=404, detail="Post content not found")

    return BlogPostDetailResponse(
        id=blog_post.id,
        title=blog_post.title,
        content=blog_post_content.content,
        tags=[],  # Assuming tags are not implemented yet
        author_id=None,  # Assuming author details are not implemented yet
        author_avatar=None,
        author_email=None,
        author_website=None,
        author_bio=None,
        author_location=None,
        author_company=None,
        author_job_title=None,
        author_skills=None,
        author_interests=None,
        author_hobbies=None,
        author_languages=None,
        author_languages_level=None,
    )
