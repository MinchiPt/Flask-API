from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

# from db import items, stores
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(
        200, ItemSchema
    )  # Sending and validating data back to client with schema
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(404, message="Admin privilage required.")
            
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}, 200

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)
    # Sending and validating data back to client with schema
    def put(self, item_data, item_id):
        # item_data: (json data) when received will be validated by schema hence there is no need to populate item_data = request.get_json()
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        ()
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(
        200, ItemSchema(many=True)
    )  # ItemSchema(many=True) is an instance to deal with multiple item schemas and send back to client
    @jwt_required()
    def get(self):
        return ItemModel.query.all()

    #this endpoint is protected by jwt decorator and will not be access 
    #if client does not have a authorized token
    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(
        201, ItemSchema
    )  # Sending and validating data back to client with schema
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
