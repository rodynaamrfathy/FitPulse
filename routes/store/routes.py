from flask import Blueprint, request, flash, redirect, url_for, render_template, current_app, session
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import MySQLdb.cursors  # For using DictCursor
from helpers import allowed_file  # Import the allowed_file function from helpers.py

# Create a blueprint for store management
store_bp = Blueprint('store', __name__)

# -------------------------------Store-Product-Starts-Here------------------------------------------

# Render the store page and fetch all products
@store_bp.route('/store')
def store():
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    cursor.close()
    return render_template('store.html', products=products)

# Render product details
@store_bp.route('/product/<int:product_id>')
def product(product_id):
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM products WHERE productid = %s', (product_id,))
    product = cursor.fetchone()
    
    if product is None:
        flash('Product not found.', 'danger')
        return redirect(url_for('store.store'))
    
    cursor.execute('SELECT description FROM productdescription WHERE productid = %s', (product_id,))
    descriptions = cursor.fetchall()
    cursor.close()
    
    return render_template('product.html', product=product, descriptions=descriptions)

@store_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    # Convert product_id to string if necessary
    product_id_str = str(product_id)
    
    # Initialize cart if it's not in the session
    if 'cart' not in session:
        session['cart'] = {}
    
    # Fetch product details from the database
    mysql = current_app.config['mysql']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM products WHERE productid = %s', (product_id,))
    product = cursor.fetchone()
    cursor.close()

    if product is None:
        flash('Product not found.', 'danger')
        return redirect(url_for('store.store'))
    
    # Add or update product in the cart
    cart = session['cart']
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'id': product_id_str,  # Store product ID in the cart
            'name': product['productname'],
            'price': product['price'],
            'quantity': 1,
            'image': product['imageurl']
        }

    # Save updated cart back to session
    session['cart'] = cart
    flash('Product added to cart!', 'success')

    return redirect(url_for('store.store'))


# Route to display cart
@store_bp.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    total = sum(float(item['price']) * int(item['quantity']) for item in cart.values())
    return render_template('cart.html', cart=cart, total=total)

@store_bp.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'cart' in session and str(product_id) in session['cart']:  # Ensure product_id is converted to string
        session['cart'].pop(str(product_id))
        flash('Item removed from cart.', 'info')
    else:
        flash('Item not found in cart.', 'danger')
    
    return redirect(url_for('store.view_cart'))  # Change this line

# Route for increasing the quantity of a product in the cart
@store_bp.route('/increase_quantity/<int:product_id>', methods=['POST'])
def increase_quantity(product_id):
    print(f'Increasing quantity for product_id: {product_id}')
    product_id_str = str(product_id)  # Convert to string for consistency
    if 'cart' in session and product_id_str in session['cart']:
        session['cart'][product_id_str]['quantity'] += 1
        flash('Quantity increased!', 'success')
    else:
        flash('Item not found in cart.', 'danger')
    
    return redirect(url_for('store.view_cart'))

# Route for decreasing the quantity of a product in the cart
@store_bp.route('/decrease_quantity/<int:product_id>', methods=['POST'])
def decrease_quantity(product_id):
    product_id_str = str(product_id)  # Convert to string for consistency
    if 'cart' in session and product_id_str in session['cart']:
        if session['cart'][product_id_str]['quantity'] > 1:
            session['cart'][product_id_str]['quantity'] -= 1
            flash('Quantity decreased!', 'success')
        else:
            flash('Item quantity cannot be less than 1.', 'danger')
    else:
        flash('Item not found in cart.', 'danger')
    
    return redirect(url_for('store.view_cart'))
