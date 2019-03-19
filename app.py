

import torch
import torch.nn as nn
from torchvision import models
from PIL import Image
import torchvision.transforms as transforms

from flask import Flask, request, render_template
app = Flask(__name__)

from commons import get_tensor
from inference import get_rice_name
from resources import get_recipe, get_restaurants

@app.errorhandler(401)
def FUN_401(error):
    return render_template("page_401.html"), 401

@app.errorhandler(403)
def FUN_403(error):
    return render_template("page_403.html"), 403

@app.errorhandler(404)
def FUN_404(error):
    return render_template("page_404.html"), 404

@app.errorhandler(405)
def FUN_405(error):
    return render_template("page_405.html"), 405

@app.errorhandler(413)
def FUN_413(error):
    return render_template("page_413.html"), 413

@app.route('/', methods=['GET', 'POST'])
def FUN_shinkafa():
	# If get request
	if request.method == 'GET':
		return render_template('index.html', rice = None)

	# If post request
	if request.method == 'POST':
		# if image not present and image name is there, 
		# return the recipe or the restaurants depending on the user request.
		if 'file' not in request.files:
			rice_name = request.form.get('rice', None)

			# if no file and no rice name, redirect to the home page
			if rice_name == None:
				return render_template('index.html', rice = None)
			rice_name = rice_name.lower()
			if request.form['action'] == 'recipe':
				recipe = get_recipe(rice_name)
				return render_template('index.html', rice=rice_name.title(), results=recipe)
			elif request.form['action'] == 'restaurant':
				restaurants = get_restaurants(rice_name) 
				return render_template('index.html', rice=rice_name.title(), results=restaurants)
			else:
				print('Error: invalid request')
				return
		else:
			# If image present, predict the image
			file = request.files['file']
			image = file.read()
			category, rice_name = get_rice_name(image_bytes=image)
			return render_template('index.html', rice=rice_name.title(), category=category)


if __name__ == '__main__':
	app.run(debug=True)