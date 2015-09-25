from sqlalchemy import (
    Column,
    LargeBinary,
    SmallInteger,
    String,
    DateTime
    )

from sqlalchemy.orm import (
    synonym,
    )

from angerona2 import (
    Base,
    DBSession,
)

from sqlalchemy.ext.hybrid import hybrid_property

class Secret(Base):
    __tablename__ = 'secret'
    uniqhash = Column(String(64), primary_key=True)
    nonce = Column(LargeBinary(32))
    salt = Column(LargeBinary(32))
    snippet_type = Column(String(8))
    expiry_time = Column(DateTime)
    lifetime_reads = Column(SmallInteger)
    flags = Column(SmallInteger)

    stored_data = Column(LargeBinary)

    def __init__(self, uniqid=None):
        if uniqid:
            self.uniqhash = uniqid
        self.flags = 0x01

    @hybrid_property
    def flag_delete_early(self):
        return bool(self.flags & 0x01)

    @flag_delete_early.setter
    def flag_delete_early(self, value):
        if bool(value):
            self.flags |= 0x01
        else:
            self.flags &= ~0x01

    @hybrid_property
    def flag_unlimited_reads(self):
        return bool(self.flags & 0x02)

    @flag_unlimited_reads.setter
    def flag_unlimited_reads(self, value):
        if bool(value):
            self.flags |= 0x02
        else:
            self.flags &= ~0x02
