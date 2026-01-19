from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import datetime
import os

app = Flask(__name__)
app.secret_key = 'flipkart_pro_max_v16'

# ==========================================
# 1. SETTINGS
# ==========================================
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"

# ==========================================
# 2. INVENTORY LOGIC
# ==========================================
products = []
next_id = 1

# Helper to add products
def add_product(name, price, category, keyword, count=1, specific_image=None):
    global next_id
    for i in range(count):
        # Discount Logic
        if price < 1000: # Loot items
            original_price = price * random.randint(5, 12)
            discount = random.randint(85, 99)
        else: # Real items
            original_price = int(price * random.uniform(1.3, 1.6))
            discount = random.randint(20, 40)

        # Image Logic
        if specific_image:
            main_img = specific_image
        else:
            # LoremFlickr (Fast & Real Photos)
            rand = random.randint(1, 1000)
            main_img = f"https://loremflickr.com/300/300/{keyword}?lock={next_id}{rand}"

        products.append({
            'id': next_id,
            'name': name,
            'price': price,
            'original_price': original_price,
            'discount': discount,
            'category': category,
            'main_image': main_img,
            'rating': round(random.uniform(3.8, 4.8), 1),
            'rating_count': f"{random.randint(100, 15000)}",
        })
        next_id += 1

# --- 1. MOBILE PHONES (2 Saste, Baki Mehnge) ---
print("Generating Mobiles...")
mobile_names = [
    ("Samsung Galaxy F14", "samsung,phone"),
    ("Vivo T2x 5G", "vivo,smartphone"),
    ("Realme Narzo N55", "realme,phone"),
    ("POCO C55", "smartphone"),
    ("Lava Blaze 5G", "mobile,phone"),
    ("Samsung S23 Ultra", "samsung,galaxy"),
    ("iPhone 13", "iphone"),
    ("Realme 11 Pro", "android,phone"),
    ("Vivo V29", "vivo,mobile"),
    ("Poco M6 Pro", "poco,phone")
]

# Shuffle kar dete hain taaki saste phone random jagah aayein
random.shuffle(mobile_names)

for index, (name, key) in enumerate(mobile_names):
    if index < 2: # Sirf pehle 2 phone saste honge (Loot)
        add_product(name, 999, "Mobile", key, 1)
    else: # Baki sab mehnge (Real Price)
        real_price = random.randint(9000, 25000)
        add_product(name, real_price, "Mobile", key, 1)

# --- 2. BACK COVERS (New Request) ---
print("Generating Back Covers...")
add_product("Transparent Bumper Case", 49, "Accessories", "phone,case", 5)
add_product("Printed Hard Cover", 99, "Accessories", "mobile,cover,art", 5)
add_product("Silicon Soft Case", 79, "Accessories", "iphone,case", 5)
add_product("Leather Flip Cover", 199, "Accessories", "leather,wallet", 3)

# --- 3. SPORTS (Specific Images - As requested) ---
print("Generating Sports...")
# Plastic Bat (Loot)
bat_img = "https://rukminim2.flixcart.com/image/416/416/xif0q/bat/q/t/y/1-plastic-cricket-bat-for-kids-plastic-cricket-bat-full-size-original-imagpyz5a5z5z5ze.jpeg"
add_product("Plastic Cricket Bat (Kids)", 99, "Sports", "cricket", 5, specific_image=bat_img)

# Heavy Bat (Real)
wood_bat_img = "https://rukminim2.flixcart.com/image/416/416/xif0q/bat/4/r/2/-original-imagrgd6b3zzzzzu.jpeg"
add_product("Heavy Duty Plastic Bat", 249, "Sports", "cricket", 10, specific_image=wood_bat_img)

# Badminton
badminton_img = "https://rukminim2.flixcart.com/image/416/416/l51d30w0/racquet/z/j/w/g-force-3600-super-lite-strung-1-g-force-3600-super-lite-original-imagft56z7sz5hze.jpeg"
add_product("Badminton Set (2 Rackets)", 70, "Sports", "badminton", 5, specific_image=badminton_img)

# --- 4. OTHER LOOT ITEMS ---
add_product("USB LED Light", 19, "Gadget", "usb,gadget", 5)
add_product("Mobile Stand", 9, "Accessories", "phone,stand", 5)
add_product("Men Running Shoes", 199, "Fashion", "shoes,sneaker", 5)
add_product("Smart Watch", 499, "Gadget", "smartwatch", 4)

# ==========================================
# 3. HELPERS
# ==========================================
def get_product(pid):
    for p in products:
        if p['id'] == pid: return p
    return None

# ==========================================
# 4. HTML TEMPLATE (With Tracking System)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flipkart Sale</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --fk-blue: #2874f0; --fk-yellow: #ff9f00; --bg: #f1f2f4; }
        body { background: var(--bg); padding-bottom: 80px; font-family: sans-serif; }
        a { text-decoration: none; color: inherit; }
        
        /* NAVBAR */
        .navbar { background: var(--fk-blue); padding: 10px; position: sticky; top: 0; z-index: 100; }
        .logo { color: white; font-weight: bold; font-style: italic; font-size: 1.2rem; }
        .logo span { color: var(--fk-yellow); }
        
        /* GRID */
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; padding: 5px; }
        .card { background: white; padding: 8px; border-radius: 4px; border: 1px solid #ddd; position: relative; }
        .card img { width: 100%; height: 140px; object-fit: contain; }
        .offer-tag { position: absolute; top: 5px; left: 5px; background: #26a541; color: white; font-size: 10px; padding: 2px 6px; border-radius: 2px; }
        
        /* TRACKING STYLES */
        .tracking-card { border-left: 4px solid #26a541; margin-bottom: 10px; }
        .track-step { position: relative; padding-left: 20px; margin-bottom: 10px; font-size: 0.9rem; }
        .track-step::before { content: ''; position: absolute; left: 0; top: 5px; width: 10px; height: 10px; background: #ddd; border-radius: 50%; }
        .track-step.active::before { background: #26a541; }
        .track-step.active { color: #26a541; font-weight: bold; }
        
        /* BOTTOM NAV */
        .bottom-nav { position: fixed; bottom: 0; width: 100%; background: white; display: flex; border-top: 1px solid #ddd; z-index: 1000; padding: 5px 0;}
        .nav-item { flex: 1; text-align: center; font-size: 0.7rem; color: #333; }
        .nav-item i { font-size: 1.2rem; display: block; margin-bottom: 2px; }
        .nav-item.active { color: var(--fk-blue); }
    </style>
</head>
<body>

    <div class="navbar d-flex justify-content-between align-items-center">
        <div class="logo">Flipkart<span>Plus</span></div>
        <a href="/cart" class="text-white position-relative">
            <i class="fas fa-shopping-cart fa-lg"></i>
            {% if session.get('cart') %}
            <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size:10px;">{{ session.get('cart')|length }}</span>
            {% endif %}
        </a>
    </div>

    {% if page == 'home' %}
        
        <div class="d-flex gap-2 p-2 overflow-auto bg-white mb-2 shadow-sm">
            <a href="/?cat=all" class="btn btn-sm btn-outline-dark rounded-pill">All</a>
            <a href="/?cat=Mobile" class="btn btn-sm btn-outline-primary rounded-pill">Mobiles</a>
            <a href="/?cat=Accessories" class="btn btn-sm btn-outline-primary rounded-pill">Covers</a>
            <a href="/?cat=Sports" class="btn btn-sm btn-outline-primary rounded-pill">Sports</a>
        </div>

        <div class="bg-white p-2 mb-2">
            <h6 class="fw-bold text-danger">⚡ Crazy Deals (Under ₹999)</h6>
            <div class="d-flex gap-2 overflow-auto">
                {% for p in products if p.price <= 999 %}
                <a href="/product/{{ p.id }}" class="card text-dark text-decoration-none" style="min-width: 140px;">
                    <span class="offer-tag">Loot</span>
                    <img src="{{ p.main_image }}">
                    <div style="font-size:0.8rem; height:20px; overflow:hidden;">{{ p.name }}</div>
                    <div class="fw-bold">₹{{ p.price }}</div>
                </a>
                {% endfor %}
            </div>
        </div>

        <h6 class="p-2 fw-bold">More Products</h6>
        <div class="grid">
            {% for p in products %}
            {% if cat == 'all' or p.category == cat %}
            <a href="/product/{{ p.id }}" class="card text-decoration-none text-dark">
                {% if p.discount > 50 %}<span class="offer-tag">{{ p.discount }}% Off</span>{% endif %}
                <img src="{{ p.main_image }}">
                <div style="font-size:0.9rem; margin-top:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{{ p.name }}</div>
                <div>
                    <span class="fw-bold">₹{{ p.price }}</span>
                    <span class="text-muted text-decoration-line-through small">₹{{ p.original_price }}</span>
                </div>
                <div class="small text-success">Free Delivery</div>
            </a>
            {% endif %}
            {% endfor %}
        </div>

    {% elif page == 'detail' %}
        <div class="bg-white">
            <img src="{{ product.main_image }}" style="width:100%; height:350px; object-fit:contain;">
            <div class="p-3">
                <h5>{{ product.name }}</h5>
                <div class="mb-2"><span class="badge bg-success">{{ product.rating }} ★</span> <small>{{ product.rating_count }} Ratings</small></div>
                <h1>₹{{ product.price }} <span class="text-muted fs-5 text-decoration-line-through">₹{{ product.original_price }}</span> <span class="text-success fs-5">{{ product.discount }}% off</span></h1>
            </div>
        </div>
        <div style="position:fixed; bottom:0; width:100%; display:flex; z-index:1000;">
            <form action="/add_to_cart/{{ product.id }}" method="post" style="flex:1;"><button style="background:white; border:none; width:100%; padding:15px; font-weight:bold;">ADD TO CART</button></form>
            <form action="/buy_now/{{ product.id }}" method="post" style="flex:1;"><button style="background:var(--fk-yellow); border:none; width:100%; padding:15px; font-weight:bold; color:white;">BUY NOW</button></form>
        </div>

    {% elif page == 'cart' %}
        <div class="p-3">
            <h5>My Cart</h5>
            {% for item in cart_items %}
            <div class="card mb-2 flex-row p-2 align-items-center">
                <img src="{{ item.main_image }}" style="width:60px; height:60px;">
                <div class="ms-3">
                    <div class="fw-bold">{{ item.name }}</div>
                    <div>₹{{ item.price }}</div>
                </div>
            </div>
            {% endfor %}
            {% if cart_items %}
            <div class="fixed-bottom p-3 bg-white border-top">
                <div class="d-flex justify-content-between mb-2"><b>Total</b><b>₹{{ total }}</b></div>
                <a href="/checkout" class="btn btn-warning w-100 fw-bold">Place Order</a>
            </div>
            {% else %}
            <div class="text-center mt-5">Cart Empty</div>
            {% endif %}
        </div>

    {% elif page == 'my_orders' %}
        <div class="p-3" style="background: #f1f3f6; min-height: 100vh;">
            <h5 class="mb-3">My Orders & Tracking</h5>
            
            {% if orders %}
                {% for o in orders %}
                <div class="card mb-3 p-3 tracking-card">
                    <div class="d-flex gap-3">
                        <img src="{{ o.image }}" style="width:70px; height:70px; object-fit:contain; border:1px solid #eee;">
                        <div>
                            <div class="fw-bold">{{ o.item }}</div>
                            <div class="small text-muted">₹{{ o.amount }} • {{ o.status }}</div>
                            <div class="text-success small fw-bold mt-1">Arriving by {{ o.date }}</div>
                        </div>
                    </div>
                    <hr>
                    <div class="mt-2">
                        <div class="fw-bold small mb-2">Delivery Status</div>
                        <div class="track-step active">Order Placed <span class="text-muted small float-end">Done</span></div>
                        <div class="track-step active">Shipped ({{ o.location }}) <span class="text-muted small float-end">Done</span></div>
                        <div class="track-step">Out for Delivery <span class="text-muted small float-end">Pending</span></div>
                    </div>
                </div>
                {% endfor %}
            {% else %}
                <div class="text-center mt-5">
                    <img src="https://cdn-icons-png.flaticon.com/512/2748/2748558.png" width="100">
                    <h5 class="mt-3">No orders yet!</h5>
                    <a href="/" class="btn btn-primary mt-3">Shop Now</a>
                </div>
            {% endif %}
        </div>

    {% elif page == 'payment' %}
        <div class="p-4 bg-white m-3 rounded shadow-sm">
            <h5>Confirm Payment</h5>
            <div class="alert alert-info">Pay <b>₹{{ total }}</b> via UPI</div>
            <a href="upi://pay?pa={{ upi_id }}&pn={{ upi_name }}&am={{ total }}&cu=INR" 
               class="btn btn-success w-100 py-3 fw-bold" onclick="startTimer()">
                Pay Now
            </a>
            <form id="payForm" action="/success" method="post"></form>
        </div>
        <script>
            function startTimer() { setTimeout(() => document.getElementById('payForm').submit(), 5000); }
        </script>

    {% elif page == 'success' %}
        <div class="text-center mt-5 p-4">
            <h1 style="font-size:80px;">🚚</h1>
            <h2 class="text-success">Order Placed!</h2>
            <p>You can track delivery in 'My Orders'.</p>
            <a href="/my_orders" class="btn btn-primary w-100 mt-3">Track Order</a>
        </div>

    {% elif page == 'login' %}
        <div class="p-4 bg-white m-3 shadow-sm rounded">
            <h4>Login</h4>
            <form method="post">
                <input type="number" name="phone" class="form-control mb-3" placeholder="Mobile Number" required>
                <button class="btn btn-warning w-100">Continue</button>
            </form>
        </div>
    {% endif %}

    <div class="bottom-nav">
        <a href="/" class="nav-item {% if page == 'home' %}active{% endif %}">
            <i class="fas fa-home"></i> Home
        </a>
        <a href="/my_orders" class="nav-item {% if page == 'my_orders' %}active{% endif %}">
            <i class="fas fa-box"></i> Orders
        </a>
        <a href="/cart" class="nav-item {% if page == 'cart' %}active{% endif %}">
            <i class="fas fa-shopping-cart"></i> Cart
        </a>
        <a href="/login" class="nav-item">
            <i class="fas fa-user"></i> Account
        </a>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# ==========================================
# 5. ROUTES
# ==========================================
@app.route('/')
def home():
    cat = request.args.get('cat', 'all')
    return render_template_string(HTML_TEMPLATE, page='home', products=products, cat=cat)

@app.route('/product/<int:pid>')
def product_detail(pid):
    product = get_product(pid)
    if not product: return redirect('/')
    return render_template_string(HTML_TEMPLATE, page='detail', product=product)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['phone']
        return redirect('/')
    return render_template_string(HTML_TEMPLATE, page='login')

@app.route('/add_to_cart/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    cart = session.get('cart', [])
    cart.append(pid)
    session['cart'] = cart
    return redirect('/cart')

@app.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    cart_items = [get_product(pid) for pid in cart_ids]
    total = sum(item['price'] for item in cart_items if item)
    return render_template_string(HTML_TEMPLATE, page='cart', cart_items=cart_items, total=total)

@app.route('/buy_now/<int:pid>', methods=['POST'])
def buy_now(pid):
    session['cart'] = [pid]
    return redirect('/checkout')

@app.route('/checkout')
def checkout():
    if not session.get('user'): return redirect('/login')
    return redirect('/payment')

@app.route('/payment')
def payment():
    cart_ids = session.get('cart', [])
    if not cart_ids: return redirect('/')
    total = sum(get_product(pid)['price'] for pid in cart_ids)
    return render_template_string(HTML_TEMPLATE, page='payment', total=total, upi_id=MY_UPI_ID, upi_name=MY_NAME)

@app.route('/success', methods=['POST'])
def success():
    # Order Confirm hone par Data Save karo
    cart_ids = session.get('cart', [])
    orders = session.get('orders', [])
    
    # Random Delivery date (7-10 days)
    days = random.randint(7, 10)
    del_date = (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%d %b")
    
    # Fake Tracking Data
    locations = ['Mumbai Hub', 'New Delhi Facility', 'Bangalore Center', 'In Transit - Lucknow']
    
    for pid in cart_ids:
        p = get_product(pid)
        orders.insert(0, { # Insert at top (Newest first)
            'item': p['name'], 
            'amount': p['price'], 
            'date': del_date,
            'image': p['main_image'],
            'status': 'Shipped',
            'location': random.choice(locations)
        })
    
    session['orders'] = orders
    session['cart'] = [] 
    return render_template_string(HTML_TEMPLATE, page='success')

@app.route('/my_orders')
def my_orders():
    orders = session.get('orders', [])
    return render_template_string(HTML_TEMPLATE, page='my_orders', orders=orders)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
