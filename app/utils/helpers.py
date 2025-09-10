from bson import ObjectId

def obj_id(obj):
    return str(obj) if isinstance(obj, ObjectId) else obj

def doc_to_user_response(doc):
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "email": doc["email"],
        "role": doc.get("role", "user")
    }

def doc_to_product_response(doc):
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "price": doc["price"],
        "description": doc.get("description", ""),
        "stock": doc.get("stock", 0)
    }

def doc_to_order_response(doc):
    doc["user"]["id"] = str(doc["user"]["_id"])
    del doc["user"]["_id"]
    for p in doc["products"]:
        p["product_id"] = str(p["product_id"])
        p["product_details"]["id"] = str(p["product_details"]["_id"])
        del p["product_details"]["_id"]
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc
