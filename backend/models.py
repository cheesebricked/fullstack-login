# PURPOSE: creates database models

from config import db       # imports our database instance

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key = True)      # creates a column with index variable called id, primary key means it must be unique
    first_name = db.Column(db.String(120), unique = False, nullable = False)
    last_name = db.Column(db.String(120), unique = False, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)

    def to_json(self):
        # returns a python dicitonary of the contact
        return {
            "id" : self.id,
            "firstName" : self.first_name,
            "lastName" : self.last_name,
            "email" : self.email,
        }
