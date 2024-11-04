from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

# Model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

# Initialize database
def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

# Routes
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/item/<int:id>')
def get_item(id):
    item = Item.query.get_or_404(id)
    return render_template('item_detail.html', item=item)

@app.route('/create', methods=['POST'])
def create():
    name = request.form.get('name')
    description = request.form.get('description')
    new_item = Item(name=name, description=description)
    db.session.add(new_item)
    db.session.commit()
    flash('Item created successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    item = Item.query.get(id)
    item.name = request.form.get('name')
    item.description = request.form.get('description')
    db.session.commit()
    flash('Item updated successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
