from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session, send_from_directory
import os
import random
import requests
import shutil
from io import BytesIO
from PIL import Image, ImageDraw
from .dummy_data import get_products, get_orders, get_users
from .helper import check_is_float_and_convert, upload_image_to_imgbb
from base64 import b64encode

views = Blueprint('views', __name__)
MAX_IMAGE_SIZE = 512 * 1024

# Path to the images directory
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
images_dir = os.path.join(static_dir, 'img', 'banner')
mfp_img = os.path.join(static_dir, 'img', 'mfp')
product_img_dir = os.path.join(static_dir, 'img', 'products')

# Ensure the image directories exist
os.makedirs(images_dir, exist_ok=True)
os.makedirs(mfp_img, exist_ok=True)
os.makedirs(product_img_dir, exist_ok=True)

# Sample banner images from the internet (pet-themed)
SAMPLE_BANNER_IMAGES = [
    "https://images.unsplash.com/photo-1548199973-03cce0bbc87b?w=800&h=400&fit=crop",
    "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?w=800&h=400&fit=crop",
    "https://images.unsplash.com/photo-1450778869180-41d0601e046e?w=800&h=400&fit=crop",
    "https://images.unsplash.com/photo-1560807707-8cc77767d783?w=800&h=400&fit=crop",
    "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=800&h=400&fit=crop"
]

# Sample MFP promotional image
SAMPLE_MFP_IMAGE = "https://images.unsplash.com/photo-1568640347023-a616a30bc3bd?w=600&h=400&fit=crop"

def download_image(url, save_path):
    """Download an image from a URL and save it to the specified path"""
    try:
        response = requests.get(url, stream=True, timeout=5)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # For small images, use BytesIO and PIL to process
        if int(response.headers.get('Content-Length', 0)) < 1024 * 1024:  # Less than 1MB
            img = Image.open(BytesIO(response.content))
            img.save(save_path)
        else:
            # For larger images, stream to disk
            with open(save_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        
        return True
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")
        return False

# Create some sample banner images if none exist
def ensure_sample_images():
    """Ensure sample images exist by downloading from URLs or creating placeholders"""
    # Banner images
    any_downloaded = False
    for i, url in enumerate(SAMPLE_BANNER_IMAGES):
        banner_path = os.path.join(images_dir, f'banner{i+1}.jpg')
        if not os.path.exists(banner_path):
            if download_image(url, banner_path):
                any_downloaded = True
            else:
                # Create a fallback colored rectangle if download fails
                img = Image.new('RGB', (800, 400), color=(73, 109, 137))
                draw = ImageDraw.Draw(img)
                draw.text((400, 200), f"Banner {i+1}", fill="white")
                img.save(banner_path)

    # MFP promotional image
    mfp_path = os.path.join(mfp_img, 'MFP.jpg')
    if not os.path.exists(mfp_path):
        if not download_image(SAMPLE_MFP_IMAGE, mfp_path):
            # Create a fallback colored rectangle if download fails
            img = Image.new('RGB', (600, 400), color=(200, 100, 50))
            draw = ImageDraw.Draw(img)
            draw.text((300, 200), "Special Offer!", fill="white")
            img.save(mfp_path)

    # If no images were downloaded successfully, create some dummy products
    if not any_downloaded:
        create_fallback_product_images()

def create_fallback_product_images():
    """Create fallback product images if downloads fail"""
    categories = ["dog-food", "cat-food", "dog-toy", "cat-toy", "dog-medicine", "cat-medicine"]
    colors = [(240, 98, 146), (50, 168, 82), (25, 118, 210), (255, 152, 0), (156, 39, 176), (121, 85, 72)]
    
    for i, category in enumerate(categories):
        img_path = os.path.join(product_img_dir, f"{category}.jpg")
        if not os.path.exists(img_path):
            color = colors[i % len(colors)]
            img = Image.new('RGB', (300, 300), color=color)
            draw = ImageDraw.Draw(img)
            draw.text((150, 150), category.replace('-', ' ').title(), fill="white")
            img.save(img_path)

# Call this function to ensure we have images
ensure_sample_images()

@views.route('/')
def home():
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
    
    # Check if directory exists and has files
    if os.path.exists(images_dir) and os.listdir(images_dir):
        images = [f for f in os.listdir(images_dir) if f.split('.')[-1].lower() in valid_extensions]
        random_image = random.choice(images) if images else None
    else:
        random_image = None
    
    # Get dummy product data
    all_products = get_products()
    medicine = [p for p in all_products if 'medicine' in p['category'].lower()]
    toys = [p for p in all_products if 'toy' in p['category'].lower()]
    foods = [p for p in all_products if 'food' in p['category'].lower()]
    
    # Try to render index.html, fall back to home.html if not found
    try:
        return render_template("index.html", random_image=random_image, 
                             products=all_products, toys=toys, medicine=medicine, foods=foods)
    except:
        return render_template("home.html", random_image=random_image, 
                             products=all_products, toys=toys, medicine=medicine, foods=foods)

@views.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    if "user_id" not in session:
        flash('User login required to add product', category='error')
        return jsonify({"error": "Unauthorized"}), 401

    # Retrieve product data from request
    data = request.get_json()
    product_id = data.get("id")
    product_name = data.get("name")
    product_price = data.get("price")
    image_url = data.get("image_url")

    # Initialize cart in session if it doesn't exist
    if "cart" not in session:
        session["cart"] = []

    # Add product to cart
    cart = session["cart"]
    cart.append({
        "id": product_id, 
        "name": product_name, 
        "price": float(product_price), 
        "product_img": image_url,
        "quantity": 1
    })
    session["cart"] = cart  # Update session

    return jsonify({"cart_count": len(cart)})

@views.route('/get_cart_count', methods=['GET'])
def get_cart_count():
    cart = session.get("cart", [])
    return jsonify({'cart_count': len(cart)})

@views.route('/userinfo')
def userinfo():
    users = get_users()
    return render_template('userinfo.html', data=users)

category_list = [
    "cat-food",
    "dog-food",
    "bird-food",
    "cat-medicine",
    "dog-medicine",
    "rabbit-medicine",
    "bird-medicine",
    "hamster-medicine"
]

@views.route('/cart')
def view_cart():
    if "user_id" not in session:
        # For testing, automatically set a user_id
        session["user_id"] = 1
        session["user_name"] = "Test User"

    cart = session.get("cart", [])
    total_price = sum(float(item["price"]) * item.get("quantity", 1) for item in cart)

    return render_template("cart.html", cart=cart, total_price=total_price)

@views.route("/increment-cart", methods=["POST"])
def increment_cart():
    product_id = request.form.get("product_id")
    cart = session.get("cart", [])
    for item in cart:
        if str(item["id"]) == str(product_id):
            item["quantity"] += 1
            break
    session["cart"] = cart
    return redirect("/cart")

@views.route("/decrement-cart", methods=["POST"])
def decrement_cart():
    product_id = request.form.get("product_id")
    cart = session.get("cart", [])
    # Iterate through the cart to find and update the item
    cart = [
        item for item in cart if not (
            str(item["id"]) == str(product_id) and 
            item["quantity"] == 1
        )
    ]
    for item in cart:
        if str(item["id"]) == str(product_id):
            item["quantity"] -= 1
            break
    session["cart"] = cart
    return redirect("/cart")

@views.route("/remove-cart-item", methods=["POST"])
def remove_cart_item():
    product_id = request.form.get("product_id")
    cart = session.get("cart", [])
    cart = [item for item in cart if str(item["id"]) != str(product_id)]
    session["cart"] = cart
    return redirect("/cart")

@views.route('/appiontment')
def appointment():
    return render_template('vetAppintment.html')

@views.route('/blog')
def blog():
    return render_template('pet_blog.html')

@views.route('/adminDashboard', methods=['GET','POST'])
def adminDashboard():
    if request.method == 'GET':
        orders = get_orders()
        return render_template("adminDashboard.html", orders=orders)
    
    if request.method == 'POST':
        name = request.form.get("productName", None)
        category = request.form.get('productCategory', None)
        description = request.form.get('description', None)
        stock = request.form.get('quantity', None)
        price = request.form.get('price', None)
        
        # Just provide feedback that the product would be added (no DB)
        flash(f"Product '{name}' added successfully!", "success")
        return redirect(url_for('views.adminDashboard'))

@views.route("/place-order", methods=["POST"])
def place_order():
    # Auto-set user if not logged in (for testing)
    if "user_id" not in session:
        session["user_id"] = 1
        session["user_name"] = "Test User"
    
    user_id = session.get("user_id")
    
    name = request.form.get("name")
    address = request.form.get("address")
    payment_method = request.form.get('payment_method', 'COD')
    transaction_id = request.form.get('transaction_id', None)
    cart = session.get("cart", [])
    
    # Calculate totals
    total_price = sum(item["quantity"] * float(item["price"]) for item in cart)
    delivery_fee = 35
    tax = round(total_price * 0.04, 2)
    total = round(total_price + delivery_fee + tax, 2)
    
    # Validate transaction_id if payment method is Bkash
    if payment_method == "Bkash" and not transaction_id:
        flash("Transaction ID is required for Bkash payments.", "error")
        return redirect(url_for("views.view_cart"))
    
    # Store in session for confirmation page
    session["order_name"] = name
    session["order_address"] = address
    session["order_total"] = total
    session["order_payment_method"] = payment_method
    session["order_transaction_id"] = transaction_id
    
    # Clear the cart after placing the order
    session["cart"] = []

    return redirect(url_for("views.order_confirmation"))

@views.route("/order-confirmation")
def order_confirmation():
    name = session.get("order_name", "Customer")
    address = session.get("order_address", "No address provided")
    total = session.get("order_total", 0)
    payment_method = session.get("order_payment_method", "COD")
    transaction_id = session.get("order_transaction_id", "N/A")
    
    return render_template("order_confirmation.html", 
                          name=name, 
                          address=address, 
                          total=total,
                          payment_method=payment_method,
                          transaction_id=transaction_id)

@views.route('/toys')
def toys():
    toy_products = [p for p in get_products() if 'toy' in p['category'].lower()]
    return render_template('toys.html', toys=toy_products)

@views.route('/medicine')
def medicine():
    medicine_products = [p for p in get_products() if 'medicine' in p['category'].lower()]
    return render_template('medicine.html', medicine=medicine_products)

@views.route('/food')
def food():
    food_products = [p for p in get_products() if 'food' in p['category'].lower()]
    return render_template('food.html', foods=food_products)

# Serve static files directly (fallback)
@views.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)
