from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import datetime
import os

app = Flask(__name__)
app.secret_key = 'flipkart_ultra_max_v12'

# ==========================================
# 1. SETTINGS (UPI ID)
# ==========================================
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"

# ==========================================
# 2. INVENTORY LOGIC (MEESHO + FLIPKART STYLE)
# ==========================================
products = []
next_id = 1

def add_product(name, price, category, keyword, count=1):
    global next_id
    colors = ['Red', 'Blue', 'Black', 'Green', 'Yellow', 'White', 'Pink', 'Orange']
    
    for i in range(count):
        color = random.choice(colors)
        
        # MRP Logic:
        # Agar Loot price (kam) hai, to MRP 5-10 guna dikhao (90% Off)
        # Agar Real price hai, to MRP 1.5 guna dikhao (30% Off)
        if price < 100:
            original_price = price * random.randint(5, 10)
            discount = random.randint(80, 95)
        else:
            original_price = int(price * random.uniform(1.4, 2.0))
            discount = random.randint(20, 60)

        # AI Image Generator (Pollinations AI)
        # Seed use karte hain taaki har product ki photo alag ho
        img_seed = random.randint(1000, 9999)
        main_img = f"https://image.pollinations.ai/prompt/{keyword} {color} product view?width=300&height=300&nologo=true&seed={img_seed}"
        
        products.append({
            'id': next_id,
            'name': f"{name} ({color})",
            'price': price,
            'original_price': original_price,
            'discount': discount,
            'category': category,
            'main_image': main_img,
            'images': [main_img], # Slider ke liye
            'rating': round(random.uniform(3.5, 5.0), 1),
            'rating_count': f"{random.randint(100, 5000)}",
        })
        next_id += 1

# --- 1. SPECIAL REQUEST: BATS & BADMINTON ---
print("Generating Sports Gear...")
# Loot Items
add_product("Plastic Cricket Bat", 99, "Sports", "plastic cricket bat toy", 5)
add_product("Kids Badminton Set", 70, "Sports", "badminton racket pair cheap", 5)
# Real Items
add_product("Kashmir Willow Bat", 499, "Sports", "professional cricket bat wood", 10)
add_product("Pro Badminton Kit Bag", 399, "Sports", "yonex badminton bag", 5)
add_product("Cosco Tennis Ball", 50, "Sports", "green tennis ball", 10)

# --- 2. LOOT STORE (₹9, ₹19, ₹49, ₹99) ---
print("Generating Loot Items...")
loot_items = [
    ("USB OTG Adapter", 9, "Gadget", "usb otg adapter small"),
    ("Mobile Stand", 9, "Gadget", "plastic mobile holder"),
    ("Cable Protector", 9, "Gadget", "spiral cable protector"),
    ("Cleaning Cloth", 19, "Home", "microfiber cleaning cloth"),
    ("Face Mask (Pack of 5)", 19, "Fashion", "black face mask"),
    ("Ball Pen Set", 19, "Stationery", "blue ball pen set"),
    ("Wired Earphones", 49, "Gadget", "wired earphones black"),
    ("Men Handkerchief", 49, "Fashion", "cotton handkerchief men"),
    ("KeyChain LED", 49, "Gadget", "small led keychain flashlight"),
    ("Tempered Glass", 50, "Mobile", "mobile screen guard glass"),
    ("Phone Back Cover", 99, "Mobile", "printed mobile back cover"),
    ("Socks (Pack of 3)", 99, "Fashion", "ankle socks men"),
]

for name, price, cat, key in loot_items:
    add_product(name, price, cat, key, count=3) # Har item ke 3 piece

# --- 3. MEESHO/FLIPKART STYLE (Real Prices) ---
print("Generating Real Products...")

# Fashion (Saree, Kurti, Shirts)
add_product("Banarasi Silk Saree", 499, "Fashion", "indian silk saree traditional", 5)
add_product("Cotton Kurti", 299, "Fashion", "ladies cotton kurti design", 5)
add_product("Men Printed T-Shirt", 199, "Fashion", "men stylish printed t-shirt", 8)
add_product("Denim Jeans", 599, "Fashion", "blue denim jeans men", 5)
add_product("Formal Shirt", 449, "Fashion", "white formal shirt men", 5)

# Electronics
add_product("Bluetooth Neckband", 399, "Electronics", "bluetooth neckband earphones", 5)
add_product("Smart Watch T800", 899, "Electronics", "smart watch orange strap", 5)
add_product("Power Bank 10000mAh", 699, "Electronics", "power bank slim", 4)
add_product("Trimmer for Men", 349, "Electronics", "beard trimmer black", 4)

# Home
add_product("Double Bedsheet", 249, "Home", "floral bedsheet double bed", 4)
add_product("Water Bottle 1L", 149, "Home", "steel water bottle", 4)
add_product("Lunch Box", 199, "Home", "tiffin box insulated", 4)
add_product("LED Bulb (Pack of 4)", 299, "Home", "led light bulb white", 3)

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def get_product(pid):
    for p in products:
        if p['id'] == pid: return p
    return None

def get_similar(pid):
    # Same category ke items dhundo
    current = get_product(pid)
    sim = [p for p in products if p['category'] == current['category'] and p['id'] != pid]
    if not sim: sim = products # Agar same category na mile to random
    return random.sample(sim, min(len(sim), 6))

# ==========================================
# 4. HTML TEMPLATE (Mobile Friendly)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flipkart Big Sale</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --fk-blue: #2874f0; --fk-yellow: #ff9f00; --bg: #f1f2f4; }
        body { background: var(--bg); padding-bottom: 70px; font-family: sans-serif; }
        a { text-decoration: none; color: inherit; }
        
        /* HEADER */
        .navbar { background: var(--fk-blue); padding: 10px; position: sticky; top: 0; z-index: 100; }
        .logo { color: white; font-weight: bold; font-style: italic; font-size: 1.2rem; }
        .logo span { color: var(--fk-yellow); }
        .cart-icon { color: white; font-size: 1.2rem; position: relative; }
        .badge-count { position: absolute; top: -5px; right: -8px; font-size: 10px; }

        /* CATEGORIES */
        .cat-row { overflow-x: auto; white-space: nowrap; background: white; padding: 10px; gap: 10px; display: flex; }
        .cat-btn { border: 1px solid #ddd; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; color: #333; }
        
        /* PRODUCT CARD */
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; padding: 4px; }
        .card { background: white; border: 1px solid #eee; padding: 8px; position: relative; display: flex; flex-direction: column; }
        .card img { width: 100%; height: 140px; object-fit: contain; margin-bottom: 5px; }
        .offer-tag { position: absolute; top: 5px; left: 5px; background: #26a541; color: white; font-size: 10px; padding: 2px 5px; border-radius: 2px; }
        .p-name { font-size: 0.85rem; color: #333; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
        .p-price { font-weight: bold; font-size: 1rem; }
        .p-mrp { color: #878787; text-decoration: line-through; font-size: 0.8rem; margin-left: 5px; }
        .p-disc { color: #388e3c; font-size: 0.8rem; font-weight: bold; margin-left: 5px; }
        
        /* FOOTER */
        .bottom-nav { position: fixed; bottom: 0; width: 100%; background: white; display: flex; border-top: 1px solid #ddd; padding: 10px 0; z-index: 1000; }
        .nav-item { flex: 1; text-align: center; font-size: 0.8rem; color: #333; }
        .nav-item i { font-size: 1.2rem; display: block; margin-bottom: 2px; }
        
        /* BUTTONS */
        .btn-buy { background: var(--fk-yellow); border: none; width: 100%; padding: 12px; font-weight: bold; color: white; }
        .btn-cart { background: white; border: 1px solid #ddd; width: 100%; padding: 12px; font-weight: bold; }
        
        /* PAYMENT PAGE */
        .pay-box { background: white; margin: 15px; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    </style>
</head>
<body>

    <div class="navbar d-flex justify-content-between align-items-center">
        <div class="d-flex align-items-center">
             <i class="fas fa-bars text-white me-3" data-bs-toggle="offcanvas" data-bs-target="#sidebar"></i>
             <div class="logo">Flipkart<span>Plus</span></div>
        </div>
        <a href="/cart" class="cart-icon">
            <i class="fas fa-shopping-cart"></i>
            {% if session.get('cart') %}
            <span class="badge rounded-pill bg-danger badge-count">{{ session.get('cart')|length }}</span>
            {% endif %}
        </a>
    </div>

    <div class="offcanvas offcanvas-start" id="sidebar">
        <div class="offcanvas-header bg-primary text-white">
            <h5 class="offcanvas-title">Account</h5>
        </div>
        <div class="offcanvas-body p-0">
            <a href="/" class="d-block p-3 border-bottom">Home</a>
            <a href="/my_orders" class="d-block p-3 border-bottom">My Orders</a>
            <a href="/logout" class="d-block p-3 border-bottom text-danger">Logout</a>
        </div>
    </div>

    {% if page == 'home' %}
        
        <div style="background: var(--fk-blue); padding: 0 10px 10px;">
            <input type="text" class="form-control" placeholder="Search for products, brands and more">
        </div>

        <div class="cat-row">
            <a href="/?cat=all" class="cat-btn">All</a>
            <a href="/?cat=Sports" class="cat-btn">Sports</a>
            <a href="/?cat=Fashion" class="cat-btn">Fashion</a>
            <a href="/?cat=Gadget" class="cat-btn">Gadgets</a>
            <a href="/?cat=Home" class="cat-btn">Home</a>
        </div>

        <img src="https://image.pollinations.ai/prompt/flipkart big billion sale banner?width=800&height=200&nologo=true" style="width:100%; height:auto;">

        <div class="bg-white p-2 mt-2">
            <h6 class="fw-bold text-danger">🔥 Under ₹99 Store</h6>
            <div style="display:flex; overflow-x:auto; gap:10px;">
                {% for p in products if p.price < 100 %}
                <a href="/product/{{ p.id }}" style="min-width:120px;" class="card text-dark">
                    <img src="{{ p.main_image }}">
                    <div class="p-name">{{ p.name }}</div>
                    <div class="p-price">₹{{ p.price }}</div>
                </a>
                {% endfor %}
            </div>
        </div>

        <h6 class="fw-bold p-2 mt-2">Suggested for You</h6>
        <div class="grid">
            {% for p in products %}
            {% if cat == 'all' or p.category == cat %}
            <a href="/product/{{ p.id }}" class="card text-dark">
                <span class="offer-tag">{{ p.discount }}% OFF</span>
                <img src="{{ p.main_image }}">
                <div class="p-name">{{ p.name }}</div>
                <div>
                    <span class="p-price">₹{{ p.price }}</span>
                    <span class="p-mrp">₹{{ p.original_price }}</span>
                    <span class="p-disc">{{ p.discount }}% off</span>
                </div>
                <div style="font-size:10px; color:#26a541;">Free Delivery</div>
            </a>
            {% endif %}
            {% endfor %}
        </div>

    {% elif page == 'detail' %}
        <div class="bg-white">
            <img src="{{ product.main_image }}" style="width:100%; height:300px; object-fit:contain;">
            <div class="p-3">
                <h5>{{ product.name }}</h5>
                <div class="d-flex align-items-center mb-2">
                    <span class="badge bg-success">{{ product.rating }} <i class="fas fa-star" style="font-size:10px;"></i></span>
                    <span class="text-muted ms-2 small">{{ product.rating_count }} Ratings</span>
                </div>
                <h1>₹{{ product.price }} 
                    <span class="text-muted fs-6 text-decoration-line-through">₹{{ product.original_price }}</span>
                    <span class="text-success fs-6">{{ product.discount }}% off</span>
                </h1>
                
                <div class="mt-3">
                    <h6>Available offers</h6>
                    <small class="d-block"><i class="fas fa-tag text-success"></i> 5% Cashback on Flipkart Axis Bank Card</small>
                    <small class="d-block"><i class="fas fa-tag text-success"></i> Special Price Get extra ₹50 off</small>
                </div>
            </div>
        </div>
        
        <div style="height:60px;"></div>
        <div style="position:fixed; bottom:0; width:100%; display:flex; z-index:999;">
            <form action="/add_to_cart/{{ product.id }}" method="post" style="flex:1;">
                <button class="btn-cart">ADD TO CART</button>
            </form>
            <form action="/buy_now/{{ product.id }}" method="post" style="flex:1;">
                <button class="btn-buy">BUY NOW</button>
            </form>
        </div>

    {% elif page == 'cart' %}
        <div class="p-3">
            <h5>My Cart ({{ cart_items|length }})</h5>
            {% if cart_items %}
                {% for item in cart_items %}
                <div class="card mb-2 flex-row p-2 align-items-center">
                    <img src="{{ item.main_image }}" style="width:60px; height:60px; object-fit:contain;">
                    <div class="ms-3">
                        <div class="fw-bold">{{ item.name }}</div>
                        <div>₹{{ item.price }}</div>
                    </div>
                </div>
                {% endfor %}
                <div class="fixed-bottom p-3 bg-white border-top shadow">
                    <div class="d-flex justify-content-between mb-2">
                        <b>Total Amount</b>
                        <b>₹{{ total }}</b>
                    </div>
                    <a href="/checkout" class="btn btn-warning w-100 fw-bold">Place Order</a>
                </div>
            {% else %}
                <div class="text-center mt-5">
                    <img src="https://rukminim1.flixcart.com/www/800/800/promos/16/05/2019/d438a32e-765a-4d8b-b4a6-520b560971e8.png" width="200">
                    <h5 class="mt-3">Your cart is empty!</h5>
                    <a href="/" class="btn btn-primary mt-3">Shop Now</a>
                </div>
            {% endif %}
        </div>

    {% elif page == 'payment' %}
        <div class="pay-box">
            <h5><i class="fas fa-shield-alt text-success"></i> Secure Payment</h5>
            <hr>
            <div class="d-flex justify-content-between mb-3">
                <span>Total Amount:</span>
                <span class="fw-bold">₹{{ total }}</span>
            </div>
            
            <div class="alert alert-info small">
                Preferred Method: UPI (PhonePe, GPay, Paytm)
            </div>

            <a href="upi://pay?pa={{ upi_id }}&pn={{ upi_name }}&am={{ total }}&cu=INR" 
               class="btn btn-success w-100 py-3 fw-bold" onclick="autoSubmit()">
                Pay ₹{{ total }} using UPI App
            </a>

            <div id="loader" class="text-center mt-3" style="display:none;">
                <div class="spinner-border text-primary"></div>
                <p>Verifying Payment...</p>
            </div>
            
            <form id="successForm" action="/success" method="post"></form>
        </div>
        <script>
            function autoSubmit() {
                document.getElementById('loader').style.display = 'block';
                setTimeout(function(){
                    document.getElementById('successForm').submit();
                }, 6000); // 6 second wait
            }
        </script>

    {% elif page == 'success' %}
        <div class="text-center mt-5 p-4">
            <img src="https://img.freepik.com/premium-vector/green-check-mark-icon-symbol-logo-circle-tick-symbol-green-color-vector-illustration_685751-503.jpg" width="100">
            <h2 class="mt-3 text-success">Order Placed!</h2>
            <p class="text-muted">Thank you for shopping.</p>
            <div class="card p-3 mt-4">
                <div class="d-flex justify-content-between">
                    <span>Delivery By:</span>
                    <b>{{ date }}</b>
                </div>
            </div>
            <a href="/" class="btn btn-primary w-100 mt-4">Continue Shopping</a>
        </div>

    {% elif page == 'login' %}
        <div class="p-4 bg-white m-3 shadow-sm rounded">
            <h4>Login</h4>
            <form method="post">
                <div class="mb-3">
                    <label>Phone Number</label>
                    <input type="number" name="phone" class="form-control" placeholder="+91" required>
                </div>
                <button class="btn btn-warning w-100">Request OTP</button>
            </form>
        </div>

    {% endif %}

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

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
    session['cart'] = []
    date = (datetime.datetime.now() + datetime.timedelta(days=4)).strftime("%d %b, %Y")
    return render_template_string(HTML_TEMPLATE, page='success', date=date)

@app.route('/my_orders')
def my_orders():
    return "<h1>My Orders Page (Coming Soon)</h1><a href='/'>Go Home</a>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
