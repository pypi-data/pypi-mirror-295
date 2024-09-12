from typing import TYPE_CHECKING

from sqlmodel import SQLModel

if TYPE_CHECKING:
    pass


class CommonFormField(SQLModel):
    name: str
    label: str | None = None
    type: str | None = None
    required: bool | None = None
    default: str | None = None
    description: str | None = None
    options: list[str] | None = None
    placeholder: str | None = None


class CommonFormData(SQLModel):
    title: str | None = None
    fields: list[CommonFormField] | None = None
