# models.py
# Rohan Weeden
# Created: July 3, 2017

# Declare the database models needed for the ctf module

Base = declarative_base()

class CTF(Base):
    __tablename__ = "ctfs"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
