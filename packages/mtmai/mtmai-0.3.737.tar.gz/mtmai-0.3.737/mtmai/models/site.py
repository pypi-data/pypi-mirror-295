from datetime import datetime

from sqlmodel import Field, SQLModel

from mtmai.mtlibs import mtutils


class SiteHost(SQLModel):
    domain: str = Field(default=None, max_length=255)
    is_default: bool = Field(default=False)
    is_https: bool = Field(default=False)
    pass


class SiteBase(SQLModel):
    """
    站点基础配置
        1: 站点标题
        2: 站点域名
        3: 站点描述: 决定了 agent 如何自动采集文章和生成文章
        4: 站点关键词: 决定了 agent 如何自动采集文章和生成文章
        5: 站点作者
        6: 站点版权
        7: 站点创建时间
        8: 站点更新时间
    """

    title: str | None = Field(default=None, max_length=255)
    # hosts: list[SiteHost] = Field(default=[])
    description: str | None = Field(default=None, max_length=255)
    keywords: str | None = Field(default=None, max_length=255)
    author: str | None = Field(default=None, max_length=255)
    copyright: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())


# Database model, database table inferred from class name
class Site(SiteBase, table=True):
    id: str = Field(default_factory=mtutils.gen_orm_id_key, primary_key=True)
