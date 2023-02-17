from app import db
from app.models.viewer import Viewer
from app.models.content import Content
from app.models.watchlist import Watchlist
from app.models.model_helpers import *
from flask import Blueprint, jsonify, abort, make_response, request

watchlist_bp = Blueprint("watchlist_bp", __name__, url_prefix="/watchlist")

@watchlist_bp.route("", methods=["POST"])
def create_watchlist():
    request_body = validate_request_body(Watchlist, request.get_json())
    viewer = validate_model(Viewer, request_body["viewer_id"])
    content = validate_model(Content, request_body["content_id"])
    new_watchlist = Watchlist.from_dict(request_body)

    db.session.add(new_watchlist)
    db.session.commit()

    return make_response(jsonify(f"Watchlist {new_watchlist.id} successfully created"), 201)

@watchlist_bp.route("", methods=["GET"])
def read_all_watchlists():
    watchlist_query = Watchlist.query
    watchlist_response = []
    for watchlist in watchlist_query:
        watchlist_response.append(watchlist.to_dict())
    return jsonify(watchlist_response)

@watchlist_bp.route("/<watchlist_id>", methods=["DELETE"])
def delete_one_watchlist(viewer_id):
    watchlist = validate_model(Watchlist, watchlist_id)
    
    db.session.delete(watchlist)
    db.session.commit()
    
    return make_response(jsonify(watchlist.to_dict()), 200)

@watchlist_bp.route("<viewer_id>/add", methods=["POST"]) # request = {viewer_id, content}
def add_one_content_to_watchlist_of_loggined_viewer(viewer_id):
    request_body = request.get_json()
    request_content = validate_request_body(Content, request_body["content"])
    viewer = validate_model(Viewer, request_body["viewer_id"])
    content = Content.query.get(request_content["id"])

    if not content:
        new_content = Content.from_dict(request_content)
        db.session.add(new_content)
        db.session.commit()
    
        content = new_content

    duplicate_watchlist = Watchlist.query.filter_by(content_id=content.id).filter_by(viewer_id=viewer.id).all()
    print(duplicate_watchlist)

    if not duplicate_watchlist:
        request_watchlist = {
            "viewer_id":viewer.id,
            "content_id":content.id
        }
        
        new_watchlist = Watchlist.from_dict(request_watchlist)

        db.session.add(new_watchlist)
        db.session.commit()

        return make_response(jsonify(f"Watchlist {new_watchlist.id} successfully created"), 201)
    
    return make_response(jsonify(f"This movie already exists in the watchlist."), 400)