from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from db import engine
import enum

Base = declarative_base()

class Method(enum.Enum):
    GET             = 0
    HEAD            = 1
    POST            = 2
    PUT             = 3
    DELETE          = 4
    CONNECT         = 5
    OPTIONS         = 6
    TRACE           = 7
    PATCH           = 8

    def from_str(method: str):
        methods = {
            Method.GET: [
                "get", "g"
            ],
            Method.HEAD: [
                "head", "hea", "h"
            ],
            Method.POST: [
                "post", "pst", "p"
            ],
            Method.PUT: [
                "put", "s"
            ],
            Method.DELETE: [
                "delete", "del", "d"
            ],
            Method.CONNECT: [
                "connect", "con", "c"
            ],
            Method.OPTIONS: [
                "options", "opt", "o"
            ],
            Method.TRACE: [
                "trace", "trc", "t"
            ],
            Method.PATCH: [
                "patch", "pac", "f"
            ]
        }

        for k, v in methods.items():
            if method.lower() in v:
                return k
        return None

    def to_str(self):
        return (
            "GET",
            "HEAD",
            "POST",
            "PUT",
            "DELETE",
            "CONNECT",
            "OPTIONS",
            "TRACE",
            "PATCH"
        )[self.value]

class User(Base):
    __tablename__   = "users"

    id              = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token           = Column(String(256), unique=True)
    email           = Column(String(320), unique=True)
    ntfy_url        = Column(String(32), unique=True)
    discord_id      = Column(BigInteger, unique=True)
    hooks           = relationship("Hook", back_populates="user", lazy="joined")

    def __repr__(self):
        return f"<User(id={self.id}, token={self.token[:6]+'...' if type(self.token) == str else self.token}, ntfy={self.ntfy_url}, discord_id={self.discord_id}, nb_hooks={len(self.hooks)})>"

class Hook(Base):
    __tablename__   = "hooks"

    id              = Column(Integer, primary_key=True, index=True, autoincrement=True)
    short_url       = Column(String(32), unique=True, nullable=False)
    method          = Column(Enum(Method))
    url             = Column(String(256), nullable=False)
    body            = Column(String(1024), nullable=False)
    is_redirect     = Column(Boolean, default=False)

    user_id         = Column(Integer, ForeignKey("users.id"), nullable=False)
    user            = relationship("User", back_populates="hooks", lazy="joined")

    expires_at      = Column(DateTime, default=lambda: datetime.now() + timedelta(days=1))

    def __repr__(self):
        return f"<Hook(id={self.id}, path={self.short_url}, url={self.url}, expire_at={self.expires_at})>"

class Event(Base):
    __tablename__   = "events"

    id              = Column(Integer, primary_key=True, index=True)

Base.metadata.create_all(engine)