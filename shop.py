from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import datetime
import os

app = Flask(__name__)
app.secret_key = 'flipkart_final_public_release_v10'

# ==========================================
# 1. SETTINGS (UPI ID)
# ==========================================
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"

# ==========================================
# 2. INVENTORY LOGIC
# ==========================================
products = []
next_id = 1

COLORS = ['Red', 'Blue', 'Black', 'Gold', 'Silver', 'Green', 'Yellow', 'Multicolor']

def add_product(name, price, category, keyword, count=1):
    global next_id
    for i in range(count):
        color = COLORS[i % len(COLORS)]
        original_price = price * 100  # Fake MRP to show 99% OFF
        
        # AI Images
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
            'discount': 99,
            'category': category,
            'images': images,
            'main_image': images[0],
            'rating': round(random.uniform(3.5, 5.0), 1),
            'rating_count': f"{random.randint(1, 50)}k",
            'specs': {"Color": color, "Warranty": "6 Months", "Material": "Premium"},
        })
        next_id += 1

# --- LOADING PRODUCTS (Yahan Naye Items Add Kiye Hain) ---

# 1. CRICKET BATS (Total 20 Logic)
# 5 Saste Bat (Rs 99)
add_product("Plastic Cricket Bat", 99, "Sports", "plastic cricket bat toy", 5)
# 15 Mehnge Bat (Rs 200 se upar)
add_product("Heavy Duty Plastic Bat", 249, "Sports", "hard plastic cricket bat", 15)

# 2. BADMINTON (Logic)
# 5 Saste Badminton (Rs 70)
add_product("Kids Badminton Set", 70, "Sports", "badminton racket pair", 5)
# 5 Mehnge Bags (Rs 499)
add_product("Pro Badminton Kit Bag", 499, "Sports", "badminton sports bag", 5)

# 3. EXISTING ITEMS
add_product("iPhone 15 Pro Max", 1500, "Mobile", "iphone 15 pro max titanium", 5)
add_product("Samsung S24 Ultra", 1500, "Mobile", "samsung s24 ultra", 5)
add_product("Vivo T2x 5G", 999, "Mobile", "vivo smartphone", 4)
add_product("Oppo Reno 10", 499, "Mobile", "oppo phone", 4)
add_product("RC Toy Car", 1, "Toys", "remote control toy car", 5)
add_product("Running Shoes", 50, "Fashion", "nike running shoes", 6)
add_product("Digital Watch", 30, "Fashion", "digital led watch band", 5)

def get_product(pid):
    for p in products:
        if p['id'] == pid: return p
    return None

def get_similar_products(current_id):
    sim = [p for p in products if p['id'] != current_id]
    return random.sample(sim, min(len(sim), 6))

# ==========================================
# 3. HTML TEMPLATE (Design wahi purana)
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
        .product-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; padding: 5px; }
        .card { background: white; padding: 10px; position: relative; border: 1px solid #eee; height: 100%; display: flex; flex-direction: column; justify-content: space-between; }
        .tag-badge { position: absolute; top: 5px; left: 5px; background: #388e3c; color: white; padding: 2px 6px; font-size: 10px; border-radius: 2px; }
        .slider-container { overflow-x: auto; display: flex; scroll-snap-type: x mandatory; height: 300px; }
        .slider-img { min-width: 100%; height: 100%; object-fit: contain; scroll-snap-align: center; }
        .timer-box { background: white; color: #333; padding: 2px 5px; border-radius: 3px; font-weight: bold; font-size: 12px; }
        .sticky-footer { position: fixed; bottom: 0; left: 0; width: 100%; display: flex; z-index: 1000; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); }
        .btn-cart { flex: 1; background: white; border: none; padding: 15px; font-weight: bold; }
        .btn-buy { flex: 1; background: #ff9f00; border: none; padding: 15px; font-weight: bold; color: white; }
        .user-dp { width: 30px; height: 30px; background: white; color: var(--fk-blue); border-radius: 50%; font-weight: bold; display: flex; align-items: center; justify-content: center; }
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
            <a href="/logout" class="d-block p-3 border-bottom text-danger">Logout</a>
        </div>
    </div>

    <div class="container-fluid px-0">
        {% if page == 'home' %}
            <div style="background: var(--fk-blue); padding: 0 10px 10px;">
                <input type="text" class="form-control rounded-1 border-0" placeholder="Search for products...">
            </div>
            
            <div class="d-flex gap-2 p-2 overflow-auto bg-white mb-2">
                <a href="/?cat=all" class="btn btn-sm btn-outline-primary rounded-pill">All</a>
                <a href="/?cat=Sports" class="btn btn-sm btn-outline-primary rounded-pill">Sports</a>
                <a href="/?cat=Mobile" class="btn btn-sm btn-outline-primary rounded-pill">Mobiles</a>
                <a href="/?cat=Fashion" class="btn btn-sm btn-outline-primary rounded-pill">Fashion</a>
            </div>

            <div style="background: linear-gradient(90deg, #ff0000, #ff5500); color: white; padding: 10px; display: flex; justify-content: space-between; align-items: center;">
                <div><i class="fas fa-bolt"></i> FLASH SALE 99% OFF</div>
                <div class="d-flex gap-1">
                    <span class="timer-box" id="h">11</span> : <span class="timer-box" id="m">59</span> : <span class="timer-box" id="s">30</span>
                </div>
            </div>

            <div class="bg-white p-2 mb-2">
                <span class="fw-bold text-danger">₹99 Loot Store (Sports & More)</span>
                <div class="scroll-row">
                    {% for p in products if p.price <= 99 %}
                    <a href="/product/{{ p.id }}" class="scroll-item text-decoration-none text-dark">
                        <img src="{{ p.main_image }}" style="height:100px; width:100%; object-fit:contain;">
                        <div style="font-size:12px; margin-top:5px;" class="text-truncate">{{ p.name }}</div>
                        <div class="fw-bold">₹{{ p.price }} <span class="text-success small">99% off</span></div>
                    </a>
                    {% endfor %}
                </div>
            </div>

            <div class="bg-white p-2 mb-2">
                <h6 class="fw-bold">Trending Products</h6>
                <div class="product-grid">
                    {% for p in products if p.price > 99 %}
                    {% if cat == 'all' or p.category == cat %}
                    <a href="/product/{{ p.id }}" class="card text-dark text-decoration-none">
                        <span class="tag-badge">99% Off</span>
                        <img src="{{ p.main_image }}" style="height:120px; object-fit:contain;">
                        <div class="mt-2" style="font-size:13px;">{{ p.name }}</div>
                        <div class="fw-bold">₹{{ p.price }} <span class="text-muted text-decoration-line-through small">₹{{ p.original_price }}</span></div>
                    </a>
                    {% endif %}
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
                <div class="alert alert-warning p-2 mt-2 small"><i class="fas fa-fire"></i> Hurry, Only a few left!</div>
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

        {% elif page == 'my_orders' %}
            <div class="p-3">
                <h5>My Orders</h5>
                {% if orders %}
                    {% for o in orders %}
                    <div class="card mb-2 p-2">
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
# 4. APP ROUTES
# ==========================================

@app.route('/')
def home():
    cat = request.args.get('cat', 'all')
    return render_template_string(HTML_TEMPLATE, page='home', products=products, cat=cat)

@app.route('/product/<int:pid>')
def product_detail(pid):
    product = get_product(pid)
    if not product: return redirect('/')
    similar = get_similar_products(pid)
    return render_template_string(HTML_TEMPLATE, page='detail', product=product, similar=similar)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = {'name': request.form['name'], 'phone': request.form['phone']}
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
    cart_ids = session.get('cart', [])
    orders = session.get('orders', [])
    date = (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%d %b")
    for pid in cart_ids:
        p = get_product(pid)
        orders.append({'item': p['name'], 'amount': p['price'], 'date': date})
    session['orders'] = orders
    session['cart'] = [] 
    return render_template_string(HTML_TEMPLATE, page='success', date=date)

@app.route('/my_orders')
def my_orders():
    orders = session.get('orders', [])
    return render_template_string(HTML_TEMPLATE, page='my_orders', orders=orders)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
