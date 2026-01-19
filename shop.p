from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import datetime
import os

app = Flask(__name__)
app.secret_key = 'flipkart_daily_update_v30'

# ==========================================
# 1. SETTINGS
# ==========================================
MY_UPI_ID = "9653314458@naviaxis"
MY_NAME = "Apni Dukaan"
START_DATE = datetime.date(2023, 11, 1) # Yahan se din ginti shuru hogi

# ==========================================
# 2. DATA POOL (Yahan se daily naye product ayenge)
# ==========================================
# Isme maine bahut sare real products bhar diye hain
PRODUCT_POOL = [
    ("Redmi 12 5G", 11999, "Mobile", "https://m.media-amazon.com/images/I/71d7rfSl0wL._AC_UY327_FMwebp_QL65_.jpg"),
    ("OnePlus Nord CE 3", 19999, "Mobile", "https://m.media-amazon.com/images/I/6175SlKKECL._AC_UY327_FMwebp_QL65_.jpg"),
    ("Poco C51 (Loot)", 499, "Mobile", "https://m.media-amazon.com/images/I/81ogvU1sn6L._AC_UY327_FMwebp_QL65_.jpg"),
    ("Men Striped Shirt", 299, "Fashion", "https://m.media-amazon.com/images/I/71abcde.jpg"),
    ("Women Kurta Set", 499, "Fashion", "https://m.media-amazon.com/images/I/910x4c2I9GL._AC_UL480_FMwebp_QL65_.jpg"),
    ("Nike Air Max", 2499, "Fashion", "https://m.media-amazon.com/images/I/61utX8kBDlL._AC_UL480_FMwebp_QL65_.jpg"),
    ("Sony Bluetooth Speaker", 1999, "Electronics", "https://m.media-amazon.com/images/I/71+y+z+0+1L._AC_UY327_FMwebp_QL65_.jpg"),
    ("Smart Watch Fireboltt", 999, "Electronics", "https://m.media-amazon.com/images/I/61+m+n+o+pL._AC_UY327_FMwebp_QL65_.jpg"),
    ("Gold Plated Ring", 199, "Beauty", "https://m.media-amazon.com/images/I/71+Q+R+S+TL._UY695_.jpg"),
    ("Lakme Eye Liner", 149, "Beauty", "https://m.media-amazon.com/images/I/51+Y+Z+0+1L._AC_UL480_FMwebp_QL65_.jpg"),
    ("Printed Back Cover", 49, "Accessories", "https://m.media-amazon.com/images/I/71+a+b+c+dL._AC_UL480_FMwebp_QL65_.jpg"),
    ("Gaming Mouse", 399, "Electronics", "https://m.media-amazon.com/images/I/61+q+r+s+tL._SX679_.jpg"),
    ("Kids Tricycle", 899, "Toys", "https://m.media-amazon.com/images/I/81+6+7+8+9L._SX679_.jpg"),
    ("School Bag", 299, "Fashion", "https://m.media-amazon.com/images/I/91y+S0r+jXL._UY879_.jpg"),
    ("Men Jeans", 699, "Fashion", "https://m.media-amazon.com/images/I/61q+w+e+r+tL._UY879_.jpg"),
    ("Samsung M14", 9999, "Mobile", "https://m.media-amazon.com/images/I/81vxWpPpgNL._AC_UY327_FMwebp_QL65_.jpg"),
    ("Boat Airdopes", 899, "Electronics", "https://m.media-amazon.com/images/I/51+a+b+c+dL._AC_UY327_FMwebp_QL65_.jpg"),
    ("Water Bottle Steel", 199, "Home", "https://m.media-amazon.com/images/I/61+u+v+w+xL._SX679_.jpg"),
    ("Bedsheet Double", 349, "Home", "https://m.media-amazon.com/images/I/71+M+N+O+PL._AC_UL480_FMwebp_QL65_.jpg"),
    ("Led Bulb Set", 99, "Home", "https://m.media-amazon.com/images/I/61+m+n+o+pL._AC_UY327_FMwebp_QL65_.jpg")
]

products = []
next_id = 1

def create_item(name, price, category, img, is_daily_add=False):
    global next_id
    
    # MRP Logic
    if price < 500: 
        original_price = price * random.randint(4, 8)
        discount = random.randint(80, 95)
    else:
        original_price = int(price * random.uniform(1.3, 1.5))
        discount = random.randint(20, 50)

    # Agar Daily add hai, to 'New Arrival' tag lagayenge
    is_new = is_daily_add 

    products.append({
        'id': next_id,
        'name': name,
        'price': price,
        'original_price': original_price,
        'discount': discount,
        'category': category,
        'main_image': img,
        'images': [img, img, img], # 3 images same rakh rahe hain real feel ke liye
        'rating': round(random.uniform(3.5, 4.9), 1),
        'rating_count': f"{random.randint(100, 10000)}",
        'delivery': random.randint(3, 7),
        'is_new': is_new
    })
    next_id += 1

# ==========================================
# 3. AUTO-UPDATE LOGIC (DAILY 5 PRODUCTS)
# ==========================================
def initialize_shop():
    # 1. Pehle Fixed Maal Daalo (Jo hamesha rahega)
    create_item("iPhone 15 (Blue)", 65999, "Mobile", "https://m.media-amazon.com/images/I/71d7rfSl0wL._AC_UY327_FMwebp_QL65_.jpg")
    create_item("Plastic Bat (Kids)", 99, "Sports", "https://rukminim2.flixcart.com/image/416/416/xif0q/bat/q/t/y/1-plastic-cricket-bat-for-kids-plastic-cricket-bat-full-size-original-imagpyz5a5z5z5ze.jpeg")
    create_item("Kashmir Willow Bat", 499, "Sports", "https://rukminim2.flixcart.com/image/416/416/xif0q/bat/4/r/2/-original-imagrgd6b3zzzzzu.jpeg")
    create_item("Saree (Silk)", 499, "Fashion", "https://m.media-amazon.com/images/I/910x4c2I9GL._AC_UL480_FMwebp_QL65_.jpg")

    # 2. Ab Check Karo Kitne Din Beete?
    today = datetime.date.today()
    days_passed = (today - START_DATE).days
    
    # Logic: Har din 5 naye product
    # Agar 2 din beete hain to 10 products dikhenge extra.
    # Hum Loop (Cycle) use karenge taaki pool khatam na ho.
    
    products_to_add = days_passed * 5
    
    # Limit lagate hain taaki site hang na ho (Max 100 extra items)
    if products_to_add > 100: products_to_add = 100
    if products_to_add < 0: products_to_add = 0

    print(f"--- AUTO UPDATE: Adding {products_to_add} New Products ---")

    for i in range(products_to_add):
        # Pool me se round-robin tarike se item uthao
        item_data = PRODUCT_POOL[i % len(PRODUCT_POOL)]
        # Price thoda change karte hain taaki har baar alag lage
        new_price = item_data[1] + random.choice([-50, 0, 50, 100])
        if new_price < 9: new_price = 9
        
        create_item(item_data[0], new_price, item_data[2], item_data[3], is_daily_add=True)

# App start hote hi dukaan sajao
initialize_shop()

# ==========================================
# 4. HTML TEMPLATE (New Badge Added)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Flipkart Daily</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --fk-blue: #2874f0; --fk-yellow: #ff9f00; --bg: #f1f2f4; }
        body { background: var(--bg); padding-bottom: 70px; font-family: sans-serif; }
        a { text-decoration: none; color: inherit; }
        
        .navbar { background: var(--fk-blue); padding: 10px; position: sticky; top: 0; z-index: 1000; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; padding: 6px; }
        .card { background: white; border-radius: 4px; overflow: hidden; position: relative; border: 1px solid #e0e0e0; display:flex; flex-direction:column; }
        .card img { width: 100%; height: 160px; object-fit: contain; padding: 10px; }
        
        /* TAGS */
        .tag-loot { position: absolute; top: 0; left: 0; background: #26a541; color: white; font-size: 10px; padding: 2px 6px; }
        .tag-new { position: absolute; top: 0; right: 0; background: #ff4d4d; color: white; font-size: 10px; padding: 2px 6px; font-weight:bold; }
        
        .p-name { font-size: 0.85rem; color: #000; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; padding: 0 5px; }
        .p-price { font-size: 1rem; font-weight: bold; padding: 0 5px; }
        .p-disc { font-size: 0.75rem; color: #388e3c; font-weight: bold; margin-left: 5px; }
        
        .bottom-nav { position: fixed; bottom: 0; left: 0; width: 100%; background: white; display: flex; border-top: 1px solid #ddd; z-index: 1000; padding: 8px 0; }
        .nav-item { flex: 1; text-align: center; font-size: 0.7rem; color: #666; }
        .nav-item.active { color: var(--fk-blue); font-weight: bold; }
        .nav-item i { font-size: 1.2rem; display: block; margin-bottom: 2px; }
        
        /* SEARCH */
        .search-bar { width: 100%; border-radius: 2px; border: none; padding: 8px; margin-top: 5px; }
    </style>
</head>
<body>

    <div class="navbar flex-column align-items-start">
        <div class="d-flex w-100 justify-content-between align-items-center">
             <div class="d-flex align-items-center gap-2 text-white">
                 <i class="fas fa-bars" data-bs-toggle="offcanvas" data-bs-target="#sidebar"></i>
                 <div style="font-weight:bold; font-style:italic;">Flipkart<span style="color:var(--fk-yellow)">Plus</span></div>
             </div>
             <a href="/cart" class="text-white position-relative">
                 <i class="fas fa-shopping-cart fs-5"></i>
                 {% if session.get('cart') %}
                 <span class="badge rounded-pill bg-danger position-absolute top-0 start-100 translate-middle">{{ session.get('cart')|length }}</span>
                 {% endif %}
             </a>
        </div>
        <form action="/" method="get" class="w-100">
            <input type="text" name="q" class="search-bar" placeholder="Search for products..." value="{{ request.args.get('q', '') }}">
        </form>
    </div>

    <div class="offcanvas offcanvas-start" style="width: 75%;" id="sidebar">
        <div class="offcanvas-header bg-primary text-white"><h5>Menu</h5></div>
        <div class="offcanvas-body p-0">
            <a href="/" class="d-block p-3 border-bottom">Home</a>
            <a href="/my_orders" class="d-block p-3 border-bottom">My Orders</a>
            <a href="/logout" class="d-block p-3 text-danger">Logout</a>
        </div>
    </div>

    {% if page == 'home' %}
        
        <div class="d-flex gap-3 p-3 bg-white overflow-auto mb-2 shadow-sm">
            <a href="/?cat=all" class="text-center text-dark" style="min-width:60px;"><div class="bg-light p-2 rounded-circle mb-1">ALL</div></a>
            <a href="/?cat=Mobile" class="text-center text-dark" style="min-width:60px;"><div class="bg-light p-2 rounded-circle mb-1">📱</div></a>
            <a href="/?cat=Fashion" class="text-center text-dark" style="min-width:60px;"><div class="bg-light p-2 rounded-circle mb-1">👕</div></a>
            <a href="/?cat=Electronics" class="text-center text-dark" style="min-width:60px;"><div class="bg-light p-2 rounded-circle mb-1">🔌</div></a>
        </div>

        <div class="bg-white">
            <div class="p-2 fw-bold text-muted">Just for You</div>
            <div class="grid">
                {% for p in products %}
                <a href="/product/{{ p.id }}" class="card text-dark">
                    {% if p.is_new %}<span class="tag-new">NEW</span>{% endif %}
                    {% if p.discount > 80 %}<span class="tag-loot">{{ p.discount }}% OFF</span>{% endif %}
                    
                    <img src="{{ p.main_image }}" onerror="this.src='https://placehold.co/300x300?text=No+Img'">
                    <div class="p-name">{{ p.name }}</div>
                    <div>
                        <span class="p-price">₹{{ p.price }}</span>
                        <span class="text-muted text-decoration-line-through small">₹{{ p.original_price }}</span>
                        <span class="p-disc">{{ p.discount }}% off</span>
                    </div>
                </a>
                {% endfor %}
            </div>
        </div>

    {% elif page == 'detail' %}
        <div class="bg-white">
            <img src="{{ product.main_image }}" class="d-block w-100" style="height:350px; object-fit:contain;">
            <div class="p-3">
                <div class="text-muted small">{{ product.category }}</div>
                <h5>{{ product.name }}</h5>
                <div class="mb-2"><span class="badge bg-success">{{ product.rating }} ★</span> <small>{{ product.rating_count }} Ratings</small></div>
                <h1 class="mb-0">₹{{ product.price }}</h1>
                <div class="mb-3">
                    <span class="text-muted text-decoration-line-through">₹{{ product.original_price }}</span>
                    <span class="text-success fw-bold ms-2">{{ product.discount }}% off</span>
                </div>
            </div>
        </div>
        <div style="height:60px;"></div>
        <div style="position:fixed; bottom:0; width:100%; display:flex; z-index:2000;">
            <form action="/add_to_cart/{{ product.id }}" method="post" style="flex:1;"><button style="background:white; border:none; padding:15px; width:100%; font-weight:bold;">ADD CART</button></form>
            <form action="/buy_now/{{ product.id }}" method="post" style="flex:1;"><button style="background:var(--fk-yellow); border:none; padding:15px; width:100%; font-weight:bold; color:white;">BUY NOW</button></form>
        </div>

    {% elif page == 'cart' %}
        <div class="p-3 bg-white" style="min-height:90vh;">
            <h5>My Cart</h5>
            {% for item in cart_items %}
            <div class="d-flex gap-3 border-bottom py-3">
                <img src="{{ item.main_image }}" style="width:80px; height:80px; object-fit:contain;">
                <div><div class="fw-bold">{{ item.name }}</div><div class="fw-bold">₹{{ item.price }}</div></div>
            </div>
            {% endfor %}
            {% if cart_items %}
            <div class="fixed-bottom p-3 bg-white border-top"><a href="/checkout" class="btn btn-warning w-100 fw-bold">Place Order (₹{{ total }})</a></div>
            {% else %}
            <div class="text-center mt-5">Cart Empty</div>
            {% endif %}
        </div>

    {% elif page == 'payment' %}
        <div class="bg-white p-4 m-3 rounded shadow-sm">
            <h5>Confirm Payment</h5>
            <div class="alert alert-success">Total: <b>₹{{ total }}</b></div>
            <a href="upi://pay?pa={{ upi_id }}&pn={{ upi_name }}&am={{ total }}&cu=INR" class="btn btn-success w-100 py-3 fw-bold" onclick="ok()">Pay Now</a>
            <form id="okForm" action="/success" method="post"></form>
            <script>function ok(){setTimeout(()=>document.getElementById('okForm').submit(),5000);}</script>
        </div>

    {% elif page == 'success' %}
        <div class="text-center mt-5 p-4"><h1 style="color:green; font-size:60px;">✔</h1><h2>Order Placed!</h2><a href="/my_orders" class="btn btn-primary mt-3">Track Order</a></div>

    {% elif page == 'my_orders' %}
        <div class="p-3">
            <h5>My Orders</h5>
            {% for o in orders %}
            <div class="card mb-3 p-3 shadow-sm border-0">
                <div class="d-flex gap-3"><img src="{{ o.image }}" style="width:60px;"><div><div class="fw-bold">{{ o.item }}</div><div class="text-muted">₹{{ o.amount }}</div></div></div>
                <div class="bg-light p-2 mt-2 rounded small"><div class="fw-bold text-success">Arriving {{ o.date }}</div><div>Status: {{ o.status }}</div></div>
            </div>
            {% else %}<div class="text-center mt-5">No Orders</div>{% endfor %}
        </div>

    {% elif page == 'login' %}
        <div class="p-4 bg-white m-3 rounded shadow-sm mt-5"><h4>Login</h4><form method="post"><input type="number" name="phone" class="form-control mb-3" placeholder="Mobile" required><button class="btn btn-warning w-100">Continue</button></form></div>
    {% endif %}

    <div class="bottom-nav">
        <a href="/" class="nav-item active"><i class="fas fa-home"></i>Home</a>
        <a href="/my_orders" class="nav-item"><i class="fas fa-box"></i>Orders</a>
        <a href="/cart" class="nav-item"><i class="fas fa-shopping-cart"></i>Cart</a>
        <a href="/login" class="nav-item"><i class="fas fa-user"></i>User</a>
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
    query = request.args.get('q', '').lower()
    cat = request.args.get('cat', 'all')
    filtered = products
    if query: filtered = [p for p in products if query in p['name'].lower()]
    elif cat != 'all': filtered = [p for p in products if p['category'] == cat]
    return render_template_string(HTML_TEMPLATE, page='home', products=filtered)

@app.route('/product/<int:pid>')
def product_detail(pid):
    p = next((i for i in products if i['id'] == pid), None)
    if not p: return redirect('/')
    return render_template_string(HTML_TEMPLATE, page='detail', product=p)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST': session['user']=request.form['phone']; return redirect('/')
    return render_template_string(HTML_TEMPLATE, page='login')

@app.route('/add_to_cart/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    cart = session.get('cart', []); cart.append(pid); session['cart'] = cart; return redirect('/cart')

@app.route('/cart')
def cart():
    cart_items = [next((p for p in products if p['id']==id),None) for id in session.get('cart',[])]
    total = sum(i['price'] for i in cart_items if i)
    return render_template_string(HTML_TEMPLATE, page='cart', cart_items=[i for i in cart_items if i], total=total)

@app.route('/buy_now/<int:pid>', methods=['POST'])
def buy_now(pid): session['cart'] = [pid]; return redirect('/checkout')

@app.route('/checkout')
def checkout(): return redirect('/login') if not session.get('user') else redirect('/payment')

@app.route('/payment')
def payment():
    total = sum(next((p for p in products if p['id']==id),{'price':0})['price'] for id in session.get('cart',[]))
    return render_template_string(HTML_TEMPLATE, page='payment', total=total, upi_id=MY_UPI_ID, upi_name=MY_NAME)

@app.route('/success', methods=['POST'])
def success():
    orders = session.get('orders', [])
    for id in session.get('cart', []):
        p = next((i for i in products if i['id']==id), None)
        if p: orders.insert(0, {'item':p['name'], 'amount':p['price'], 'date':"7 Days", 'image':p['main_image'], 'status':'Shipped'})
    session['orders'] = orders; session['cart'] = []
    return render_template_string(HTML_TEMPLATE, page='success')

@app.route('/my_orders')
def my_orders(): return render_template_string(HTML_TEMPLATE, page='my_orders', orders=session.get('orders', []))

@app.route('/logout')
def logout(): session.clear(); return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
