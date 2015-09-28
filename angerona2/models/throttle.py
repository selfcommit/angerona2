# from sqlalchemy import (
#     Column,
#     LargeBinary,
#     Integer,
#     String,
#     DateTime
#     )
# 
# from sqlalchemy.orm import (
#     synonym,
#     )
# 
# from angerona2 import (
#     Base,
# )
# 
# # this will need to be stored in a memory table or !SQLite for decent load
# class Throttle(Base):
#     __tablename__ = 'throttle'
#     ip = Column(String(64), primary_key=True)
#     result = Column(Integer)
#     ts = Column(DateTime)
#     urihash = Column(String(64))
