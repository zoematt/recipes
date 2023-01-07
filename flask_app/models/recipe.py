from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Recipe:
    db = "recipes"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.under_30 = data['under_30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.other_date = data['other_date']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name,under_30,description,instructions, user_id, other_date) VALUES(%(name)s,%(under_30)s,%(description)s,%(instructions)s,%(user_id)s, %(other_date)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        list = []
        for i in results:
            r = Recipe(i)
            u = {
                'id': i['users.id'], 
                'first_name': i['first_name'], 
                'last_name': i['last_name'], 
                'email': i['email'], 
                'password': i['password'], 
                'created_at' : i['users.created_at'],
                'updated_at' : i['users.updated_at']
                }
            User(u)
            r.user = u
            list.append(r)
        print("list")
        print(list)
        return list

    @classmethod
    def get_by_id(cls,data):
        query= "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id where recipes.id= %(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(results)
        print("creating recipe")
        r = cls(results[0])
        u = {
            'id': results[0]['users.id'], 
            'first_name': results[0]['first_name'], 
            'last_name': results[0]['last_name'], 
            'email': results[0]['email'], 
            'password': results[0]['password'], 
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at']
            }
        User(u)
        r.user = u
        print(r)
        return r


    @staticmethod
    def is_valid(recipe_dict):
        valid = True
        flash_string = " field is required and must be at least 3 characters."
        if len(recipe_dict["name"]) < 3:
            flash("Name " + flash_string)
            valid = False
        if len(recipe_dict["description"]) < 3:
            flash("Description " + flash_string)
            valid = False
        if len(recipe_dict["instructions"]) < 3:
            flash("Instructions " + flash_string)
            valid = False
        if "under_30" not in recipe_dict:
            flash("Does your recipe take less than 30 min?")
            valid = False

        return valid

    @classmethod
    def update_recipe(cls, recipe_dict):

        # Update the data in the database.
        query = """UPDATE recipes
                    SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30 = %(under_30)s, other_date=%(other_date)s
                    WHERE id = %(id)s;"""
        result = connectToMySQL(cls.db).query_db(query,recipe_dict)
        return result

    @classmethod
    def delete_recipe_by_id(cls, recipe_id):

        data = {"id": recipe_id}
        query = "DELETE from recipes WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query,data)
        return recipe_id




    