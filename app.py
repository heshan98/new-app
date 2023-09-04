from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():

    pred_value = 0
    if request.method == 'POST':
        carat = request.form['carat']
        cut = request.form['cut']
        
        color = request.form['color']
        clarity = request.form['clarity']
        depth = request.form['depth']
        table = request.form['table']
        length = request.form['Length']
        width = request.form['Width']
        height = request.form['Height']

        feature_list = []
        
        feature_list.append(float(carat))
        feature_list.append(float(depth))
        feature_list.append(float(table))
        feature_list.append(float(length))
        feature_list.append(float(width))
        feature_list.append(float(height))

        cut_list = ['0', '2', '3', '4', '1']
        color_list = ['4', '1', '2', '0', '3', '5', '6']
        clarity_list = ['6', '5', '4', '2', '1', '0', '3', '7']

        def traverse_list(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)

        traverse_list(cut_list, cut)
        traverse_list(color_list, color)
        traverse_list(clarity_list, clarity)

        pred_value = prediction(feature_list)
        pred_value = np.round(pred_value[0], 2)

    return render_template('index.html', pred_value=pred_value)

if __name__ == '__main__':
    app.run(debug=True)
