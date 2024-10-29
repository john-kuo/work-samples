from flask import Flask, render_template
from flask_security import Security, login_required, roles_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beefnet.db'

# Setup Flask-Security
db = SQLAlchemy(app)
security = Security(app)

@app.route('/brand', methods=['GET'])
@login_required
def browse_brands():
    return render_template('brand/browse.html')

@app.route('/brand/<int:brand_id>', methods=['GET'])
@login_required
def view_sub_brand(brand_id):
    return render_template('brand/brand_view.html', brand_id=brand_id)

if __name__ == '__main__':
    app.run(debug=True)