from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
    # items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete, delete-orphan")

    # Alchemy knows that the stores table is used by the storemodel class, so when we have a store_id using the stores tables, we can then define a relationship with the storemodel class, and it will automatically populate the store variable with a storemodel object, whose id matches that of the foreign key;
    # back_populates to items, and items that back_populates to store, alchemy knows that these are two ends of a relationship.
    # lazy = dynamic is a config that will only fetch the storemodel when we tell it to
