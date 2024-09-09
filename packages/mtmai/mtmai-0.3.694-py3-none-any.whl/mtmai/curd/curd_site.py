"""站点 curd 操作"""

import yaml
from sqlmodel import Session

from mtmai.models.site import Site


async def get_site(session: Session, site_id_or_host: str) -> Site:
    """获取站点"""

    # 开发期间，数据暂时写死
    yaml_data = yaml.load(
        open("ai_tasks/site_config_1.yml", encoding="utf-8"), Loader=yaml.SafeLoader
    )
    site_data = yaml_data.get("site")
    if not site_data:
        raise ValueError("站点数据不存在")
    return site_data
    # with get_session() as session:
    #     return session.query(Site).filter(Site.id == site_id_or_host).first()
