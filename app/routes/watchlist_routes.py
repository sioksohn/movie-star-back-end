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

# @watchlist_bp.route("/<viewer_id>/watchlist/add", methods=["POST"])  #{params: {"viewer_id":id , "content":content}}
# def add_one_content_to_viewer_watchlist(viewer_id, content):
#     request_body = request.get_json()
#     request_content = validate_request_body(Content, request_body["content"])

#     viewer = validate_model(Viewer, request_body["viewer_id"])
#     # content = validate_model(Content, request_content["content_id"])
#     content = Content.query.get(request_content["content_id"])

#     if not content:
#         new_content = content
#         db.session.add(new_content)
#         db.session.commit()

#     new_watchlist = {}
#     new_watchlist["viewer_id"] = viewer.id,
#     new_watchlist["content_id"] = content.id
        

#     db.session.add(new_watchlist)
#     db.session.commit()

#     return make_response(jsonify(f"Watchlist {new_watchlist.id} successfully created"), 201)

# @watchlist_bp.route("/test", methods=["POST"])  #{params: {"viewer_id":id , "content":content}}
# def add_one_content_to_viewer_watchlist():
#     request_body = request.get_json()
        
#     new_content = Content(
#             poster = request_body["poster"],
#             title = request_body["title"],
#             date = request_body["date"],
#             media_type = request_body["media_type"],
#             vote_average = request_body["vote_average"]
#         )
#     console.log(new_content)

#     db.session.add(new_content)
#     db.session.commit()
#     console.log(Content.query.all())
#     # new_watchlist = {}
#     # new_watchlist["viewer_id"] = viewer.id,
#     # new_watchlist["content_id"] = request_content.id
        

#     # db.session.add(new_watchlist)
#     # db.session.commit()

#     return make_response(jsonify(f"successfully created"), 201)

@watchlist_bp.route("/add", methods=["POST"])
def create_watchlist():
    request_body = validate_request_body(Content, request.get_json())
    
    new_content = Content(
            poster = request_body["poster"],
            title = request_body["title"],
            date = request_body["date"],
            media_type = request_body["media_type"],
            vote_average = request_body["vote_average"]
        )
    console.log(new_content)

    db.session.add(new_content)
    db.session.commit()

    return make_response(jsonify(f"Watchlist {new_watchlist.id} successfully created"), 201)