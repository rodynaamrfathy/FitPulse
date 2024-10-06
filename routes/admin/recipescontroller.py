import MySQLdb
from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app

# Define Blueprint for recipes management
recipes_bp = Blueprint('recipescontroller', __name__)

'''
    The Following Route is for the Recipe Management

    1- manage_recipes & rendering manage_recipes.html
'''

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

'''
    This route fetches all the recipes from the database and renders them in the manage_recipes.html
'''

@recipes_bp.route('/manage_recipes')
def manage_recipes():
    mysql = current_app.config['mysql']  # Fetch the MySQL connection from Flask's current_app config
    cursor = mysql.connection.cursor()

    # Query to fetch all recipes data
    cursor.execute("SELECT * FROM recipes")  # Adjust this query as needed
    recipes = cursor.fetchall()  # Fetch all recipes

    cursor.close()

    # Render the fetched recipes in the manage_recipes.html template
    return render_template('manage_recipes.html', recipes=recipes)





'''
    The Following Route is for adding a new recipe
    it takes the recipe details from the form and inserts them into the database
    then redirects to manage_recipes
'''
from flask import session, redirect, url_for, flash, current_app, request, render_template

@recipes_bp.route('/add_recipe', methods=['POST'])
def add_recipe():
    # Get the MySQL connection
    mysql = current_app.config['mysql']  

    # Fetch the authorid from the session
    authorid = session.get('authorid')  # Get authorid from session

    # Check if authorid is not None (user is logged in)
    if authorid is None:
        flash('You must be logged in to add a recipe!', 'danger')

    # Get the recipe details from the form
    recipename = request.form['recipename']
    category = request.form['category']
    description = request.form['description']
    preptime = request.form['preptime']
    cooktime = request.form['cooktime']
    ingredients = request.form['ingredients']
    nutritionfacts = request.form['nutritionsfacts']
    instructions = request.form['instructions']  # Added instructions

    # Upload image (if any)
    image = request.files.get('image')  # Use .get() for safe access
    image_filename = image.filename if image else None

    # Save the uploaded image to the correct directory if it exists
    if image:
        image.save(f"static/uploads/recipe_images/{image_filename}")

    cursor = mysql.connection.cursor()

    # Inserting recipe details into the database, including description
    cursor.execute("""
        INSERT INTO recipes (authorid, recipename, category, image, description, preptime, cooktime, ingredients, nutritionfacts,instructions, publisheddate) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, NOW())
    """, (authorid, recipename, category, image_filename, description, preptime, cooktime, ingredients, nutritionfacts,instructions))

    mysql.connection.commit()
    cursor.close()

    flash('Recipe added successfully!', 'success')
    return redirect(url_for('recipescontroller.manage_recipes'))





@recipes_bp.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor()

    # Fetch the recipe details
    cursor.execute("SELECT * FROM recipes WHERE recipeid = %s", (recipe_id,))
    recipe = cursor.fetchone()

    if request.method == 'POST':
        # Get the updated recipe details from the form
        recipename = request.form.get('recipename')
        category = request.form.get('category')
        description = request.form.get('description')
        preptime = request.form.get('preptime')
        cooktime = request.form.get('cooktime')
        ingredients = request.form.get('ingredients')
        nutritionfacts = request.form.get('nutritionsfacts')
        instructions = request.form.get('instructions')  # Added instructions

        if not recipename or not description:
            flash('Recipe name and description cannot be empty!', 'error')
            return render_template('edit_recipe.html', recipe=recipe)

        # Handle image upload
        image = request.files.get('image')

        # Use existing image if no new image is uploaded
        if image and image.filename:
            image_filename = image.filename
            # Save new image
            image.save(f"static/uploads/recipe_images/{image_filename}")
        else:
            image_filename = recipe[4]  # Assuming the image filename is in the 5th column

        try:
            # Update the recipe in the database
            cursor.execute("""
                UPDATE recipes
                SET recipename = %s, category = %s, image = %s, description = %s, 
                    preptime = %s, cooktime = %s, ingredients = %s, nutritionfacts = %s, instructions = %s
                WHERE recipeid = %s
            """, (recipename, category, image_filename, description, preptime, cooktime, ingredients, nutritionfacts, instructions, recipe_id))
            mysql.connection.commit()
            flash('Recipe updated successfully!', 'success')
        except MySQLdb.IntegrityError as e:
            mysql.connection.rollback()
            flash('Error updating recipe: ' + str(e), 'error')

        cursor.close()
        return redirect(url_for('recipescontroller.manage_recipes'))

    cursor.close()
    return render_template('edit_recipe.html', recipe=recipe)







@recipes_bp.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    mysql = current_app.config['mysql'] 
    cursor = mysql.connection.cursor()

    try:
        cursor.execute("DELETE FROM recipes WHERE recipeid = %s", (recipe_id,))
        mysql.connection.commit()
        flash('Recipe deleted successfully!', 'success')
    except Exception as e:
        mysql.connection.rollback()  
        flash('An error occurred while deleting the recipe: ' + str(e), 'error')
    finally:
        cursor.close()

    return redirect(url_for('recipescontroller.manage_recipes'))
