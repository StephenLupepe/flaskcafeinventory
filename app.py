from crypt import methods
from email.policy import default
from pydoc import render_doc
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#Setting up a new db object in sqlalchemy

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content =  db.Column(db.String(100), nullable = False)
    type =  db.Column(db.String(100), nullable = False)
    description =  db.Column(db.String(100), nullable = False)
    date_created =  db.Column(db.DateTime(100), default=datetime.utcnow)

    def __repr__(self):
        return '<Item %r>' %self.id

#Index route: Gets data from the db and displays search form, table and add item form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        inv_content = request.form['content']
        inv_type = request.form['item_type']
        inv_desc = request.form['item_desc']

        new_item = Inventory(
            content= inv_content,
            type = inv_type,
            description = inv_desc
            )

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except: 
            return 'There was an issue entering your item'

    else:
        items = Inventory.query.order_by(Inventory.date_created).all()
        return render_template('index.html', items=items)

#Delete route. Allows you to delete a row from the table
@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Inventory.query.get_or_404(id)
    try: 
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that item'

#Update route. Allows you to update a row in the table
@app.route('/update/<int:id>', methods= ['GET', 'POST'])
def update(id):
    item = Inventory.query.get_or_404(id)

    if request.method == 'POST':
        item.content = request.form['content']
        item.type = request.form['item_type']
        item.description = request.form['item_desc']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your item'
    else:
        return render_template('update.html', item=item)

#Filter route. Displays results when filter/ search is used
@app.route('/filter', methods=['GET', 'POST'])
def filter():

    items = Inventory.query.order_by(Inventory.date_created)
    
    if request.form['search_type'] == 'AV':
        items = Inventory.query.filter(Inventory.type.like('%AV%'))

    elif request.form['search_type'] == 'Periph':
        items = Inventory.query.filter(Inventory.type.like('%Computer%'))

    elif request.form['search_type'] == 'Books':
        items = Inventory.query.filter(Inventory.type.like('%Books%'))
    
    elif request.form['search_type'] == 'Other':
        items = Inventory.query.filter(Inventory.type.like('%Other%'))

    if request.form['search']:
        search = "%{}%".format(request.form['search'])
        items = items.filter(Inventory.content.like(search)).all()
    else:
        items = items.all()

    
    return render_template('filter.html', items=items)

if __name__ == "__main__":
    app.run(debug=True)