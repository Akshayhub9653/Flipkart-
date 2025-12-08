
from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import datetime
import os

app = Flask(__name__)
app.secret_key = 'flipkart_final_public_release_v9'

# ==========================================
# 1. SETTINGS
# ==========================================
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"

# ==========================================
# 2. INVENTORY LOGIC (MASSIVE STOCK)
# ==========================================
products = []
next_id = 1

COLORS = ['Red', 'Blue', 'Black', 'Gold', 'Silver', 'Green', 'White', 'Pink', 'Yellow']

def add_product(name, price, category, keyword, count=1):
    global next_id
    for i in range(count):
        color = COLORS[i % len(COLORS)]
        
        # 99% Discount Logic (MRP Fake Badhana)
        # Agar price 1 hai, to MRP 100 dikhana padega tabhi 99% off banega
        original_price = price * 100 
        
        # 3 Images for Slider
        images = [
            f"https://image.pollinations.ai/prompt/{keyword} {color} product view?width=400&height=400&nologo=true&seed={next_id}1",
            f"https://image.pollinations.ai/prompt/{keyword} {color} lifestyle view?width=400&height=400&nologo=true&seed={next_id}2",
            f"https://image.pollinations.ai/prompt/{keyword} {color} close up?width=400&height=400&nologo=true&seed={next_id}3"
        ]

        products.append({
            'id': next_id,
            'name': f"{name} {color} Ed.",
            'price': price,
            'original_price': original_price,
            'discount': 99,  # Fixed 99% OFF
            'category': category,
            'images': images,
            'main_image': images[0],
            'rating': round(random.uniform(3.5, 5.0), 1),
            'rating_count': f"{random.randint(1, 50)}k",
            'specs': {"Color": color, "Warranty": "1 Year", "Condition": "New"},
        })
        next_id += 1

# --- 1. PREMIUM PHONES (Fixed ₹1500) ---
add_product("iPhone 15 Pro Max", 1500, "Mobile", "iphone 15 pro max titanium", 5)
add_product("Samsung S24 Ultra", 1500, "Mobile", "samsung s24 ultra", 5)

# --- 2. BUDGET PHONES (Mix ₹49, ₹99, ₹999) ---
add_product("Vivo T2x 5G", 999, "Mobile", "vivo smartphone", 4)
add_product("Oppo Reno 10", 499, "Mobile", "oppo phone", 4)
add_product("Realme Narzo", 99, "Mobile", "realme phone", 4)
add_product("Jio Keypad Phone", 49, "Mobile", "feature phone keypad", 3)

# --- 3. ₹1 LOOT STORE (Toys & Gadgets) ---
add_product("RC Toy Car", 1, "Toys", "remote control toy car", 5)
add_product("LED Keychains", 1, "Toys", "fancy keychain", 5)
add_product("USB Light", 1, "Gadget", "usb led light flexible", 5)
add_product("Mobile Stand", 1, "Gadget", "mobile phone holder stand", 5)

# --- 4. FASHION (Shoes ₹50, Watch ₹30-49) ---
add_product("Running Shoes", 50, "Fashion", "nike running shoes", 6)
add_product("Digital Watch", 30, "Fashion", "digital led watch band", 5)
add_product("Analog Watch", 49, "Fashion", "luxury wrist watch men", 5)
add_product("Cotton Socks (Pack of 3)", 10, "Fashion", "socks men", 5)
add_product("Men T-Shirt", 49, "Fashion", "men t-shirt folded", 5)

# --- 5. HOME & BEAUTY (Sab Wapas Aa Gaya) ---
add_product("Matte Lipstick", 25, "Beauty", "red lipstick tube", 5)
add_product("Eyeliner Kit", 15, "Beauty", "makeup eyeliner", 4)
add_product("Kitchen Knife Set", 20, "Home", "kitchen knife steel", 5)
add_product("Water Bottle", 19, "Home", "steel water bottle", 5)
add_product("Lunch Box", 29, "Home", "tiffin box", 4)


def get_product(pid):
    for p in products:
        if p['id'] == pid: return p
    return None

def get_similar_products(current_id):
    sim = [p for p in products if p['id'] != current_id]
    return random.sample(sim, min(len(sim), 6))

# ==========================================
# 3. HTML TEMPLATE
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flipkart Big Billion Days</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --fk-blue: #2874f0; --bg-grey: #f1f3f6; }
        body { background-color: var(--bg-grey); padding-top: 60px; padding-bottom: 70px; font-family: sans-serif; }
        a { text-decoration: none; color: inherit; }
        
        .navbar { background-color: var(--fk-blue); height: 60px; }
        
        /* 2-Column Grid for everything */
        .product-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; padding: 5px; }
        
        .card { background: white; padding: 10px; position: relative; border: 1px solid #eee; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
        .tag-badge { position: absolute; top: 5px; left: 5px; background: #388e3c; color: white; padding: 2px 6px; font-size: 10px; border-radius: 2px; }
        
        /* IMAGE SLIDER */
        .slider-container { overflow-x: auto; display: flex; scroll-snap-type: x mandatory; height: 300px; }
        .slider-img { min-width: 100%; height: 100%; object-fit: contain; scroll-snap-align: center; }
        
        /* TIMER */
        .timer-box { background: white; color: #333; padding: 2px 5px; border-radius: 3px; font-weight: bold; font-size: 12px; }
        
        /* FOOTER */
        .sticky-footer { position: fixed; bottom: 0; left: 0; width: 100%; display: flex; z-index: 1000; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); }
        .btn-cart { flex: 1; background: white; border: none; padding: 15px; font-weight: bold; }
        .btn-buy { flex: 1; background: #ff9f00; border: none; padding: 15px; font-weight: bold; color: white; }
        
        .user-dp { width: 30px; height: 30px; background: white; color: var(--fk-blue); border-radius: 50%; font-weight: bold; display: flex; align-items: center; justify-content: center; }
        
        /* SCROLLABLE ROW */
        .scroll-row { display: flex; overflow-x: auto; gap: 8px; padding: 5px; background: white; }
        .scroll-item { min-width: 130px; border: 1px solid #eee; padding: 5px; text-align: center; }
    </style>
</head>
<body>

    <nav class="navbar fixed-top">
        <div class="container-fluid d-flex align-items-center text-white">
            <i class="fas fa-bars me-3" data-bs-toggle="offcanvas" data-bs-target="#sidebar"></i>
            <span class="fw-bold fst-italic">Flipkart<span style="color:#ff9f00;">Plus</span></span>
            <a href="/cart" class="ms-auto text-white position-relative">
                <i class="fas fa-shopping-cart"></i>
                {% if session.get('cart') %}
                <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style="font-size:10px;">{{ session.get('cart')|length }}</span>
                {% endif %}
            </a>
        </div>
    </nav>

    <div class="offcanvas offcanvas-start" tabindex="-1" id="sidebar">
        <div class="offcanvas-header bg-primary text-white">
            <h5 class="offcanvas-title">
                {% if session.get('user') %}
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div class="user-dp">{{ session.get('user')['name'][0] }}</div>
                        {{ session.user.name }}
                    </div>
                {% else %} Login & Signup {% endif %}
            </h5>
        </div>
        <div class="offcanvas-body p-0">
            <a href="/" class="d-block p-3 border-bottom"><i class="fas fa-home me-2"></i> Home</a>
            <a href="/my_orders" class="d-block p-3 border-bottom"><i class="fas fa-box me-2"></i> My Orders</a>
            <a href="/cart" class="d-block p-3 border-bottom"><i class="fas fa-shopping-cart me-2"></i> My Cart</a>
            <a href="/" class="d-block p-3 border-bottom"><i class="fas fa-mobile me-2"></i> Mobiles</a>
            <a href="/" class="d-block p-3 border-bottom"><i class="fas fa-tshirt me-2"></i> Fashion</a>
            <a href="/" class="d-block p-3 border-bottom"><i class="fas fa-plug me-2"></i> Electronics</a>
            <a href="/" class="d-block p-3 border-bottom"><i class="fas fa-couch me-2"></i> Home</a>
            {% if session.get('user') %}
                <a href="/logout" class="d-block p-3 border-bottom text-danger">Logout</a>
            {% else %}
                <a href="/login" class="d-block p-3 border-bottom text-primary">Login</a>
            {% endif %}
        </div>
    </div>

    <div class="container-fluid px-0">
        {% if page == 'home' %}
            <div style="background: var(--fk-blue); padding: 0 10px 10px;">
                <input type="text" class="form-control rounded-1 border-0" placeholder="Search for products...">
            </div>

            <div style="background: linear-gradient(90deg, #ff0000, #ff5500); color: white; padding: 10px; display: flex; justify-content: space-between; align-items: center;">
                <div><i class="fas fa-bolt"></i> FLASH SALE 99% OFF</div>
                <div class="d-flex gap-1">
                    <span class="timer-box" id="h">11</span> : <span class="timer-box" id="m">59</span> : <span class="timer-box" id="s">30</span>
                </div>
            </div>

            <div class="bg-white p-2 mb-2">
                <div class="d-flex justify-content-between mb-2">
                    <span class="fw-bold text-danger">₹1 Loot Store</span>
                    <span class="badge bg-danger">Live Now</span>
                </div>
                <div class="scroll-row">
                    {% for p in products if p.price == 1 %}
                    <a href="/product/{{ p.id }}" class="scroll-item text-decoration-none text-dark">
                        <img src="{{ p.main_image }}" style="height:100px; width:100%; object-fit:contain;">
                        <div style="font-size:12px; margin-top:5px;" class="text-truncate">{{ p.name }}</div>
                        <div class="fw-bold">₹{{ p.price }} <span class="text-success small">99% off</span></div>
                    </a>
                    {% endfor %}
                </div>
            </div>

            <div class="bg-white p-2 mb-2">
                <h6 class="fw-bold">Crazy Mobile Deals</h6>
                <div class="product-grid">
                    {% for p in products if p.category == 'Mobile' %}
                    <a href="/product/{{ p.id }}" class="card text-dark text-decoration-none">
                        <span class="tag-badge">99% Off</span>
                        <img src="{{ p.main_image }}" style="height:120px; object-fit:contain;">
                        <div class="mt-2" style="font-size:13px;">{{ p.name }}</div>
                        <div class="fw-bold">₹{{ p.price }} <span class="text-muted text-decoration-line-through small">₹{{ p.original_price }}</span></div>
                    </a>
                    {% endfor %}
                </div>
            </div>

            <div class="bg-white p-2">
                <h6 class="fw-bold">Fashion, Home & More</h6>
                <div class="product-grid">
                    {% for p in products if p.category != 'Mobile' and p.price > 1 %}
                    <a href="/product/{{ p.id }}" class="card text-dark text-decoration-none">
                        <span class="tag-badge">99% Off</span>
                        <img src="{{ p.main_image }}" style="height:120px; object-fit:contain;">
                        <div class="mt-2" style="font-size:13px;">{{ p.name }}</div>
                        <div class="fw-bold">₹{{ p.price }} <span class="text-muted text-decoration-line-through small">₹{{ p.original_price }}</span></div>
                    </a>
                    {% endfor %}
                </div>
            </div>

        {% elif page == 'detail' %}
            <div class="bg-white border-bottom pb-3">
                <div class="slider-container">
                    {% for img in product.images %}
                    <img src="{{ img }}" class="slider-img">
                    {% endfor %}
                </div>
                <div class="text-center text-muted small mt-1">Swipe for more photos</div>
            </div>

            <div class="bg-white p-3">
                <h5>{{ product.name }}</h5>
                <div class="mb-2">
                    <span class="badge bg-success">{{ product.rating }} ★</span> 
                    <span class="text-muted small ms-2">{{ product.rating_count }} Ratings</span>
                </div>
                
                <h3>₹{{ product.price }} 
                    <span class="text-decoration-line-through text-muted fs-6">₹{{ product.original_price }}</span> 
                    <span class="text-success fs-6">99% off</span>
                </h3>

                <div class="alert alert-warning p-2 mt-2 small">
                    <i class="fas fa-fire"></i> Hurry, Only a few left at this price!
                </div>

                <div class="d-flex justify-content-around border rounded p-2 my-3 text-center small text-muted">
                    <div><i class="fas fa-undo text-primary mb-1"></i><br>7 Day Return</div>
                    <div><i class="fas fa-check-circle text-primary mb-1"></i><br>Genuine</div>
                    <div><i class="fas fa-truck text-primary mb-1"></i><br>Free Delivery</div>
                </div>
            </div>

            <div class="bg-white p-3 mt-2">
                <h6>Similar Products</h6>
                <div class="scroll-row">
                    {% for sim in similar %}
                    <a href="/product/{{ sim.id }}" class="scroll-item text-decoration-none text-dark">
                        <img src="{{ sim.main_image }}" style="height:80px; width:100%; object-fit:contain;">
                        <div class="text-truncate small mt-1">{{ sim.name }}</div>
                        <div class="fw-bold small">₹{{ sim.price }}</div>
                    </a>
                    {% endfor %}
                </div>
            </div>
            
            <div style="height:60px;"></div>
            <div class="sticky-footer">
                <form action="/add_to_cart/{{ product.id }}" method="post" style="flex:1;"><button class="btn-cart w-100">ADD TO CART</button></form>
                <form action="/buy_now/{{ product.id }}" method="post" style="flex:1;"><button class="btn-buy w-100">BUY NOW</button></form>
            </div>

        {% elif page == 'payment' %}
            <div class="bg-white p-3 m-3 rounded shadow-sm">
                <h5>Payment Options</h5>
                <div class="border p-3 rounded mb-3 bg-light">
                    <input type="radio" checked> <b>UPI (PhonePe / GPay)</b>
                </div>
                
                <a href="upi://pay?pa={{ upi_id }}&pn={{ upi_name }}&am={{ total }}&cu=INR" 
                   class="btn btn-warning w-100 fw-bold" onclick="startAutoConfirm()">
                    Pay ₹{{ total }} via App
                </a>
                
                <form action="/success" method="post" id="autoForm" style="display:none;"></form>
                <div id="processing" class="text-center mt-3" style="display:none;">
                    <div class="spinner-border text-primary"></div>
                    <p class="small mt-2">Verifying Payment...</p>
                </div>
            </div>
            <script>
                function startAutoConfirm() {
                    document.getElementById('processing').style.display = 'block';
                    setTimeout(() => document.getElementById('autoForm').submit(), 5000);
                }
            </script>

        {% elif page == 'success' %}
            <div class="text-center mt-5 p-3">
                <i class="fas fa-check-circle text-success display-1"></i>
                <h2 class="mt-3">Order Placed!</h2>
                <p>Delivery by {{ date }}</p>
                <a href="/" class="btn btn-primary mt-3">Shop More</a>
            </div>

        {% elif page == 'login' %}
            <div class="p-4 bg-white m-3 rounded shadow-sm">
                <h4>Login / Signup</h4>
                <form method="post">
                    <input name="name" class="form-control mb-3" placeholder="Full Name" required>
                    <input type="number" name="phone" class="form-control mb-3" placeholder="Mobile Number (+91)" required>
                    <button class="btn btn-warning w-100">Login</button>
                </form>
            </div>

        {% elif page == 'address' %}
            <div class="p-4 bg-white m-3 rounded">
                <h4>Delivery Address</h4>
                <form method="post">
                    <input name="pincode" class="form-control mb-3" placeholder="Pincode" required>
                    <textarea name="addr" class="form-control mb-3" placeholder="Full Address (House No, Colony)" required></textarea>
                    <button class="btn btn-warning w-100">Save Address</button>
                </form>
            </div>

        {% elif page == 'my_orders' %}
            <div class="p-3">
                <h5>My Orders</h5>
                {% if orders %}
                    {% for o in orders %}
                    <div class="card mb-2">
                        <div class="d-flex justify-content-between">
                            <span class="fw-bold">{{ o.item }}</span>
                            <span class="text-success fw-bold">₹{{ o.amount }}</span>
                        </div>
                        <small class="text-muted">Arriving by {{ o.date }}</small>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="text-center mt-5 text-muted">No orders yet.</div>
                {% endif %}
            </div>

        {% elif page == 'cart' %}
            <div class="p-3">
                <h5>My Cart</h5>
                {% if cart_items %}
                    {% for item in cart_items %}
                    <div class="card mb-2 d-flex flex-row p-2">
                        <img src="{{ item.main_image }}" width="50" height="50" style="object-fit:contain;">
                        <div class="ms-2">
                            <div class="fw-bold">{{ item.name }}</div>
                            <div>₹{{ item.price }}</div>
                        </div>
                    </div>
                    {% endfor %}
                    <div class="fixed-bottom p-2 bg-white border-top">
                        <div class="d-flex justify-content-between mb-2">
                            <span class="fw-bold">Total: ₹{{ total }}</span>
                        </div>
                        <a href="/checkout" class="btn btn-warning w-100">Place Order</a>
                    </div>
                {% else %}
                    <div class="text-center mt-5 text-muted">Cart is Empty</div>
                {% endif %}
            </div>

        {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function startTimer() {
            let h=11, m=59, s=30;
            setInterval(() => {
                s--; if(s<0){s=59; m--;} if(m<0){m=59; h--;}
                if(document.getElementById('h')) {
                    document.getElementById('h').innerText = h;
                    document.getElementById('m').innerText = m;
                    document.getElementById('s').innerText = s;
                }
            }, 1000);
        }
        startTimer();
    </script>
</body>
</html>
"""

# ==========================================
# 4. ROUTES
# ==========================================
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, page='home', products=products, session=session)

@app.route('/product/<int:id>')
def product_detail(id):
    p = get_product(id)
    sim = get_similar_products(id)
    return render_template_string(HTML_TEMPLATE, page='detail', product=p, similar=sim, session=session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = {'name': request.form['name'], 'phone': request.form['phone']}
        return redirect(session.get('next', '/'))
    return render_template_string(HTML_TEMPLATE, page='login', session=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/add_to_cart/<int:id>', methods=['POST'])
def add_to_cart(id):
    if 'cart' not in session: session['cart'] = []
    session['cart'].append(id)
    return redirect(request.referrer)

@app.route('/buy_now/<int:id>', methods=['POST'])
def buy_now(id):
    session['checkout_item'] = id
    if not session.get('user'):
        session['next'] = '/buy_now_process'
        return redirect('/login')
    return redirect('/address')

@app.route('/buy_now_process')
def buy_now_process(): return redirect('/address')

@app.route('/address', methods=['GET', 'POST'])
def address():
    if request.method == 'POST': return redirect('/payment')
    return render_template_string(HTML_TEMPLATE, page='address', session=session)

@app.route('/payment')
def payment():
    total = 0
    if 'checkout_item' in session:
        p = get_product(session['checkout_item'])
        if p: total = p['price']
    elif 'cart' in session:
        cart_ids = session.get('cart', [])
        cart_items = [p for p in products if p['id'] in cart_ids]
        total = sum(item['price'] for item in cart_items)
        
    return render_template_string(HTML_TEMPLATE, page='payment', total=total, upi_id=MY_UPI_ID, upi_name=MY_NAME, session=session)

@app.route('/success', methods=['POST'])
def success():
    date = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%d %b")
    amount = 0
    item_name = "Order"
    
    if 'checkout_item' in session:
        p = get_product(session['checkout_item'])
        if p:
            amount = p['price']
            item_name = p['name']
        session.pop('checkout_item', None)
    elif 'cart' in session:
        cart_ids = session.get('cart', [])
        cart_items = [p for p in products if p['id'] in cart_ids]
        amount = sum(item['price'] for item in cart_items)
        item_name = f"Cart Order ({len(cart_items)} items)"
        session['cart'] = [] 
        
    if 'orders' not in session: session['orders'] = []
    session['orders'].append({'item': item_name, 'amount': amount, 'date': date})
    return render_template_string(HTML_TEMPLATE, page='success', date=date, session=session)

@app.route('/my_orders')
def my_orders():
    if not session.get('user'): return redirect('/login')
    return render_template_string(HTML_TEMPLATE, page='my_orders', orders=session.get('orders', []), session=session)

@app.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    cart_items = [p for p in products if p['id'] in cart_ids]
    total = sum(item['price'] for item in cart_items)
    return render_template_string(HTML_TEMPLATE, page='cart', cart_items=cart_items, total=total, session=session)

@app.route('/checkout')
def checkout():
    if not session.get('user'):
        session['next'] = '/address'
        return redirect('/login')
    return redirect('/address')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
