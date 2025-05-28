from flask import Blueprint, render_template
import pandas as pd
import logging
from app.extensions import db
from app.models.user import Order

ui_bp = Blueprint('ui', __name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_csv_to_model(csv_file_path):
    """
    Load data from a CSV file into the Order model and commit to the database.
    Returns: (success_count, error_count)
    """
    success_count = 0
    error_count = 0

    try:
        # Load CSV with pandas
        df = pd.read_csv(csv_file_path)
        df = df.dropna(how='all').fillna('')  # Clean: drop empty rows, fill NaN

        for _, row in df.iterrows():
            try:
                # Skip if order already exists
                if Order.query.get(int(row['Order Id'])):
                    logger.info(f"Skipping existing Order ID {row['Order Id']}")
                    continue

                # Parse dates
                order_date = pd.to_datetime(row['order date (DateOrders)'], errors='coerce')
                shipping_date = pd.to_datetime(row['shipping date (DateOrders)'], errors='coerce')

                # Create Order instance
                order = Order(
                    type=row['Type'] or None,
                    days_for_shipping_real=int(row['Days for shipping (real)']) if row['Days for shipping (real)'] else None,
                    days_for_shipment_scheduled=int(row['Days for shipment (scheduled)']) if row['Days for shipment (scheduled)'] else None,
                    benefit_per_order=float(row['Benefit per order']) if row['Benefit per order'] else None,
                    sales_per_customer=float(row['Sales per customer']) if row['Sales per customer'] else None,
                    delivery_status=row['Delivery Status'] or None,
                    late_delivery_risk=int(row['Late_delivery_risk']) if row['Late_delivery_risk'] else None,
                    category_id=int(row['Category Id']) if row['Category Id'] else None,
                    category_name=row['Category Name'] or None,
                    customer_city=row['Customer City'] or None,
                    customer_country=row['Customer Country'] or None,
                    customer_email=row['Customer Email'] or None,
                    customer_fname=row['Customer Fname'] or None,
                    customer_id=int(row['Customer Id']) if row['Customer Id'] else None,
                    customer_lname=row['Customer Lname'] or None,
                    customer_password=row['Customer Password'] or None,
                    customer_segment=row['Customer Segment'] or None,
                    customer_state=row['Customer State'] or None,
                    customer_street=row['Customer Street'] or None,
                    customer_zipcode=float(row['Customer Zipcode']) if row['Customer Zipcode'] else None,
                    department_id=int(row['Department Id']) if row['Department Id'] else None,
                    department_name=row['Department Name'] or None,
                    latitude=float(row['Latitude']) if row['Latitude'] else None,
                    longitude=float(row['Longitude']) if row['Longitude'] else None,
                    market=row['Market'] or None,
                    order_city=row['Order City'] or None,
                    order_country=row['Order Country'] or None,
                    order_customer_id=int(row['Order Customer Id']) if row['Order Customer Id'] else None,
                    order_date=order_date if pd.notnull(order_date) else None,
                    order_id=int(row['Order Id']),
                    order_item_cardprod_id=int(row['Order Item Cardprod Id']) if row['Order Item Cardprod Id'] else None,
                    order_item_discount=float(row['Order Item Discount']) if row['Order Item Discount'] else None,
                    order_item_discount_rate=float(row['Order Item Discount Rate']) if row['Order Item Discount Rate'] else None,
                    order_item_id=int(row['Order Item Id']) if row['Order Item Id'] else None,
                    order_item_product_price=float(row['Order Item Product Price']) if row['Order Item Product Price'] else None,
                    order_item_profit_ratio=float(row['Order Item Profit Ratio']) if row['Order Item Profit Ratio'] else None,
                    order_item_quantity=int(row['Order Item Quantity']) if row['Order Item Quantity'] else None,
                    sales=float(row['Sales']) if row['Sales'] else None,
                    order_item_total=float(row['Order Item Total']) if row['Order Item Total'] else None,
                    order_profit_per_order=float(row['Order Profit Per Order']) if row['Order Profit Per Order'] else None,
                    order_region=row['Order Region'] or None,
                    order_state=row['Order State'] or None,
                    order_status=row['Order Status'] or None,
                    order_zipcode=float(row['Order Zipcode']) if row['Order Zipcode'] else None,
                    product_card_id=int(row['Product Card Id']) if row['Product Card Id'] else None,
                    product_category_id=int(row['Product Category Id']) if row['Product Category Id'] else None,
                    product_description=row['Product Description'] or None,
                    product_image=row['Product Image'] or None,
                    product_name=row['Product Name'] or None,
                    product_price=float(row['Product Price']) if row['Product Price'] else None,
                    product_status=int(row['Product Status']) if row['Product Status'] else None,
                    shipping_date=shipping_date if pd.notnull(shipping_date) else None,
                    shipping_mode=row['Shipping Mode'] or None
                )

                db.session.add(order)
                db.session.commit()
                success_count += 1
                logger.info(f"Added Order ID {row['Order Id']}")

            except Exception as e:
                db.session.rollback()
                error_count += 1
                logger.error(f"Error on Order ID {row.get('Order Id', 'unknown')}: {str(e)}")

    except Exception as e:
        logger.error(f"Error reading CSV: {str(e)}")
        error_count += 1

    logger.info(f"Finished loading: {success_count} success, {error_count} errors")
    return success_count, error_count

@ui_bp.route('/')
def home():
    return render_template('dashboard.html')

@ui_bp.route('/update_data')
def update_data():
    path = "/home/syngentai/mysite/app/csv_file/table.csv"
    success_count, error_count = load_csv_to_model(path)
    return f"Successfully inserted: {success_count}, Errors: {error_count}"EOFFILE


# File: ./app/__init__.py
mkdir -p "./app"
cat > "./app/__init__.py" << 'EOFFILE'
from flask import Flask
from flask_cors import CORS
from app.extensions import db, migrate, security
from app.models.user import user_datastore
from app.auth.routes import auth_bp
from app.routes.ui_routes import ui_bp
from app.routes.api_routes import api_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config.Config')
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)
    migrate.init_app(app, db)
    security.init_app(app, user_datastore)
    @app.before_request
    def create_admin_user():
        db.create_all()
        if not user_datastore.find_user(email="admin@example.com"):
            user_datastore.create_user(email="admin@example.com", password="admin1234")
            db.session.commit()


    # ✅ Enable CORS for frontend origin
    # Add allow_headers and methods explicitly
    CORS(
        app,
        origins=["https://syngent-ai.vercel.app"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "OPTIONS"]
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(ui_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


