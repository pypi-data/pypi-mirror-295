from sqlalchemy.orm import DeclarativeBase


# Base class used to define SQL database ORM models
class Base(DeclarativeBase):
    pass


# TODO setup file with custom types for easier type hinting.
# https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#whatsnew-20-orm-declarative-typing
#
# E.g.
# intpk = Annotated[int, mapped_column(primary_key=True)]
# user_fk = Annotated[int, mapped_column(ForeignKey("user_account.id"))]
#
# Which can be imported/used when setting up tabled e.g.:

# class User(Base):
#     __tablename__ = "user_account"

#     id: Mapped[intpk]
#     name: Mapped[str50]
#     fullname: Mapped[Optional[str]]
#     addresses: Mapped[List["Address"]] = relationship(back_populates="user")
