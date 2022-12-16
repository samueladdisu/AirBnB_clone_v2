#!/usr/bin/python3
""" City Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if getenv("HBNB_TYPE_STORAGE", None) == "db":
        __tablename__ = "cities"
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place",
                              backref="cities",
                              cascade="all, delete, delete-orphan")
    else:
        state_id = ""
        name = ""
