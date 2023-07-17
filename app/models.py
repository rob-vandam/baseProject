from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import engine
from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    authtoken = Column(String(500))
    refreshtoken = Column(String(500))
    idtoken = Column(String(500))
    admin_id = Column(Integer)
    app_id = Column(Integer)
    action = Column(String(20))
    lang = Column(String(20))
    chain_id = Column(Integer)
    Base.metadata.create_all(bind=engine)




