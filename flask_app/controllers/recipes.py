from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/new') #form for creating new recipe.
def new():
    if "user_id" not in session:
        redirect('/')
    return render_template('new_recipe.html')

@app.route('/create',methods=['POST']) #process creating recipe form.
def create():
    if not Recipe.is_valid(request.form):
        return redirect('/new')
    Recipe.save(request.form)
    return redirect('/dashboard')

@app.route('/update/<int:id>') #show the update form.
def update(id):
    if "user_id" not in session:
        redirect('/')

    return render_template('edit_recipe.html', recipe=Recipe.get_by_id({"id":id}))

@app.route('/change',methods=['POST']) #process update recipe form.
def change():
    if not Recipe.is_valid(request.form):
        return redirect(f'/update/{request.form["id"]}')
    Recipe.update_recipe(request.form)

    return redirect('/dashboard')

@app.route('/recipes/<int:id>') #show one recipe.
def show(id):
    if "user_id" not in session:
        redirect('/')

    return render_template('show_one.html', user=User.get_by_id({"id": session['user_id']}),recipe=Recipe.get_by_id({"id":id}))

@app.route('/recipes/delete/<int:id>') #delete one recipe.
def destroy(id):
    Recipe.delete_recipe_by_id(id)
    return redirect ('/dashboard')



