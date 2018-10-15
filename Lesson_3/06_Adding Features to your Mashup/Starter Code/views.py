from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


#url = 'https://api.foursquare.com/v2/venues/search'

foursquare_client_id = ""
foursquare_client_secret = ""
google_api_key = ""

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  #YOUR CODE HERE
  print "type request: ", type(request)
  print request

  if request.method == 'GET':
      return getAllRestarants()

  elif request.method == 'POST':
      print "/restaurants: ", request.method
      location = request.args.get('location', '')
      mealtype = request.args.get('mealType', '')
      restaurant_info = findARestaurant(mealtype, location)
      # store into db
      restaurant = Restaurant(restaurant_name=restaurant_info['name'],
                              restaurant_address=restaurant_info['address'],
                              restaurant_image=restaurant_info['image'])
      session.add(restaurant)
      session.commit()
      return jsonify(restaurant=restaurant.serialize)

  else:
      print "TO: '/restaurants': with request.methods = ", request.method


@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE
  if request.method == 'GET':
      return getRestarant(id)
  elif request.method == 'PUT':
      name = request.args.get('name', '')
      address = request.args.get('address', '')
      image = request.args.get('image', '')
      print "PUT of /restaurants/<int:id>: ", id,name,address, image
      return updateRestarant(id, name, address, image)
  elif request.method == 'DELETE':
      return deleteRestarant(id)



def getAllRestarants():
  restaurants = session.query(Restaurant).all()
  return jsonify(restaurants=[i.serialize for i in restaurants])


def updateRestarant(id, name, address, image):
  restaurant = session.query(Restaurant).filter_by(id = id).one()
  print "update"
  if name:
      restaurant.restaurant_name = name
  if address:
      restaurant.restaurant_address = address
  if image:
      restaurant.restaurant_image = image
  session.add(restaurant)
  session.commit()
  print "after commit"
  print "Update restaurant id: %s" % id
  return jsonify(restaurant=restaurant.serialize)


def getRestarant(id):
  restaurant = session.query(Restaurant).filter_by(id = id).one()
  return jsonify(restaurant=restaurant.serialize)


def deleteRestarant(id):
  restaurant = session.query(Restaurant).filter_by(id = id).one()
  session.delete(restaurant)
  session.commit()
  return "Delete restaurant id: %s" % id



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)



