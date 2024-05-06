#  PURPOSE: sends json request to backend of method:
# - GET -> get data
# - POST -> create something new
# - PUT/PATCH -> update data
# - DELETE -> delete data

from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])        # creates a webpage /  route with a name and permitted methods
def get_contacts():
    # gets all contacts in database
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x : x.to_json(), contacts))        # maps lambda function to_json() to each contact in contacts
    return jsonify({"contacts" : json_contacts})

@app.route("/create_contact", methods=["POST"])
def create_contact():
    # creates, stages, and commits a new contact
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return jsonify({"message" : "You must include a first name, last name, and email."}), 400       # if did not give one of the 3, return error message in json with code 400

    new_contact = Contact(first_name = first_name, last_name = last_name, email = email)
    try:
        db.session.add(new_contact)         # prepare to write to database
        db.session.commit()                 # write to database
    except Exception as e:
        return jsonify({"message" : str(e)}), 400       # catch any exceptions
    
    return jsonify({"message" : "User created!"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])      # @ in python means 
def update_contact(user_id):
    # updates a contact and commit
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message" : "User not found"}), 404
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)      # gets data from request to change first name
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message" : "user updated"}), 200

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    # delete a contact and commit
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message" : "User not found"}), 404
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message" : "user deleted"}), 200



if __name__ == "__main__":      # only excecute main if we are running main directly
    with app.app_context():
        db.create_all()         # create all models in database
    
    app.run(debug = True)