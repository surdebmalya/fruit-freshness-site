from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import controlling_img, error, prediction
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
upload = os.getcwd() + "\\uploads"

app = Flask(__name__)
app.config["DEBUG"] = False
app.config['UPLOAD_FOLDER'] = upload

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            error_code, msg = error.errors(404)
            return render_template('error.html', code = error_code, info = msg)
        file = request.files['file']
        if file.filename == '':
            error_code, msg = error.errors(404)
            return render_template('error.html', code = error_code, info = msg)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # save file locally first
            ultimate_file_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(ultimate_file_name)
            # upload to server
            status, link = controlling_img.upload_img_to_server(ultimate_file_name)
            # remove local image
            controlling_img.remove_local_pic(ultimate_file_name)

            if status=='ERROR':
                error_code, msg = error.errors(500)
                return render_template('error.html', code = error_code, info = msg)

            return render_template('uploaded.html', img_path = link)
    else:
        return render_template('home.html')

@app.route('/task',methods = ['POST', 'GET'])
def task_clicked():
    if request.method=='POST':
        img_link = request.form['img_path']
        # load the image locally
        base_path = app.config['UPLOAD_FOLDER']
        status, local_path = controlling_img.load_url_local(base_path, img_link)
        if status != 'ERROR':
            if request.form.get("classification_submit"):
                # use local_path
                try:
                    result = prediction.predicting_classification(local_path)
                    # Delete local file
                    controlling_img.remove_local_pic(local_path)
                    if result == 1:
                        pic = 'FRESH'
                    else:
                        pic = 'BAD'
                    return render_template('result.html', 
                                            code = 'Classification Report', 
                                            array = 0,
                                            pic_result = pic,
                                            url = img_link
                                        )
                except:
                    error_code, msg = error.errors(500)
                    return render_template('error.html', code = error_code, info = msg)

            elif request.form.get("regression_submit"):
                try:
                    result = prediction.predicting_regression(local_path)
                    # Delete local file
                    controlling_img.remove_local_pic(local_path)
                    return render_template('result.html', 
                                            code = 'Regression Report', 
                                            array = 1,
                                            colour_rating = round(result[0], 2),
                                            shape_rating = round(result[1], 2),
                                            texture_rating = round(result[2], 2),
                                            avg = round((round(result[0], 2) + round(result[1], 2) + round(result[2], 2))/3, 2),
                                            url = img_link
                                        )
                except:
                    error_code, msg = error.errors(500)
                    return render_template('error.html', code = error_code, info = msg)
            
            elif request.form.get("combined_submit"):
                try:
                    result1 = prediction.predicting_classification(local_path)
                    result2 = prediction.predicting_regression(local_path)
                    # Delete local file
                    controlling_img.remove_local_pic(local_path)
                    if result1 == 1:
                        pic = 'FRESH'
                    else:
                        pic = 'BAD'
                    return render_template('result.html', 
                                            code = 'Combined Report', 
                                            array = 2,
                                            pic_result = pic,
                                            colour_rating = round(result2[0], 2),
                                            shape_rating = round(result2[1], 2),
                                            texture_rating = round(result2[2], 2),
                                            avg = round((round(result2[0], 2) + round(result2[1], 2) + round(result2[2], 2))/3, 2),
                                            url = img_link
                                        )
                except:
                    error_code, msg = error.errors(500)
                    return render_template('error.html', code = error_code, info = msg)
            else:
                error_code, msg = error.errors(500)
                return render_template('error.html', code = error_code, info = msg)
        else:
            error_code, msg = error.errors(500)
            return render_template('error.html', code = error_code, info = msg)
    else:
        error_code, msg = error.errors(401)
        return render_template('error.html', code = error_code, info = msg)

# For running locally or deploying on heroku
if __name__=="__main__":
    if 'uploads' not in os.listdir():
        # create "uploads" folder
        os.mkdir("uploads")
    app.run()

# For deploying on the GCP
# if __name__=="__main__":
#     app.run(host="127.0.0.1", port=8080, debug=True)