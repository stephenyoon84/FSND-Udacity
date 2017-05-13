from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)


#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree','restaurant_id' : '1', 'id' : '1'}


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/new')
def newRestaurants():
    return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit')
def editRestaurants(restaurant_id):
    return render_template('editRestaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurants(restaurant_id):
    return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>')
@app.route('/restaurants/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return render_template('editMenuItem.html', restaurant_id=restaurant_id, item=item)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, item=item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
