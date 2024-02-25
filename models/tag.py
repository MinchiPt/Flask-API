from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(db.Integer(), db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")

    # Alchemy knows that the stores table is used by the storemodel class, so when we have a store_id using the stores tables, we can then define a relationship with the storemodel class, and it will automatically populate the store variable with a storemodel object, whose id matches that of the foreign key; back_populates will also have an items relationship at the store.py that allows each storemodel object to easilly see items that are associated with.
