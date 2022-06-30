from flask import render_template, redirect, request, url_for, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user

from myimageapp import app, dt, db, get_class_by_tablename
from sqlalchemy.sql import sqltypes

from myimageapp.queryextreme import *
from myimageapp.modelhelper import *
# from myimageapp.modelhelper2 import *

import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
@app.route('/home')
def home_page():
    return render_template("the_home.html", current_user=current_user)

@app.route('/scratch')
def scratch_page():
    return render_template("scratch.html", current_user=current_user)


dt.display_table()


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    column_list = ['user_name', 'password']
    err_msg = request.args.get('err_msg', None)
    
    column_list_dict = {"user_name": [[1, "users", "user_name"], True],                       
                        "password": [[2], False]}
    
    drop_down_data = fetch_drop_down_data(column_list_dict)

    if request.method == 'POST':
        attempted_user = Users.query.filter_by(user_name=request.form[column_list[0]]).first()

        if attempted_user is None or not attempted_user.check_password_correction(request.form[column_list[1]]):
            err_msg = "Invalid login details"
            return render_template('login.html', err_msg=err_msg, column_list=column_list, column_list_dict=column_list_dict, drop_down_data=drop_down_data)

            
        if attempted_user and attempted_user.check_password_correction(request.form[column_list[1]]):
            login_user(attempted_user)
            
            return redirect(url_for('home_page'))        

    return render_template('login.html', err_msg=err_msg, column_list=column_list, column_list_dict=column_list_dict, drop_down_data=drop_down_data)


@app.route('/register', methods=['POST', 'GET'])
def register_page():
    column_list = ['user_name', 'password']
    err_msg = None
    
    column_list_dict = {"user_name": [[1, "users", "user_name"], True],                       
                        "password": [[2], False]}        

    if request.method == 'POST':
        attempted_user = Users.query.filter_by(user_name=request.form[column_list[0]]).first()

        if attempted_user is not None:
            err_msg = "Username already exists. Try logging in."
            drop_down_data = fetch_drop_down_data(column_list_dict)

            return redirect(url_for('login_page', err_msg=err_msg, column_list=column_list, column_list_dict=column_list_dict, drop_down_data=drop_down_data))

        if attempted_user is None:
            attempted_user = Users(user_name=request.form[column_list[0]], password=request.form[column_list[1]])
            db.session.add(attempted_user)
            db.session.commit()
            login_user(attempted_user)
            
            return redirect(url_for('home_page'))        

    return render_template('register.html', err_msg=err_msg, column_list=column_list, column_list_dict=column_list_dict)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    # flash("You have been logged out", category="info")
    return redirect(url_for('home_page'))


@app.route('/<filename>')
def send_image(filename):
    # This method returns the path to the file with the provided filename
    # In order to go levels deeper you can do the following

    # optional path in the case of products
    foldername = request.args.get('foldername', None)
    foldername_str = ""
    if foldername:
        foldername_str = f'{foldername}/'

    return send_from_directory("img", f'{foldername_str}{filename}')


@app.route('/upload_image', methods=['POST', 'GET'])
@login_required
def upload_page():
    # add image_name to images table
    # create image folder if folder does not exist
    # add image to image_folder

    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
@login_required
def upload():
    # we want to store the image in the img dir in the subdir of the current user
    # create img folder if it does not exist 
    imgfolder = os.path.join(APP_ROOT, f'img/')
    
    if not os.path.isdir(imgfolder):  # Check if image folder of current user exists
        os.mkdir(imgfolder)
    
    # we want to store the image in the img dir in the subdir of the current user
    target = os.path.join(APP_ROOT, f'img/{current_user.user_name}')
    filename = None
    # print(f'target: {target}')

    if not os.path.isdir(target):  # Check if image folder of current user exists
        os.mkdir(target)

    # we allowed multiple files so we need to loop through them    
    if request.files.getlist("file")[0].filename == "":
        return redirect(url_for('upload_page'))

    for file in request.files.getlist("file"):  # this returns a list of file names
        # print(file)
        filename = file.filename  # we need to obtain the filename from the file object

        # we need to obtain the file extensions if we want to validate extension name
        # extension = os.path.splitext(filename)[i]

        # we need to tell the server to upload the file with this specific name to this specific location
        destination = "/".join([target, filename])

        # here we can change the file name to a variable of our liking
        # destination = "/".join([target, "temp.jpg"])

        # print(destination)
        file.save(destination)  # save the file
        imageobj = db.session.query(Images).filter(Images.image_name==filename).first()

        if imageobj is None:
            add_image(current_user.id, filename)   # add filename to db

    return redirect(url_for('view_images', user_id=current_user.id))

    #  A method to have the image downloaded
    # return send_from_directory('images', filename, as_attachment=True)


@app.route('/view_images', methods=['GET', 'POST'])
@login_required
def view_images():
    # This function obtains image names and folder name required to display
    # images of a single user           
    
    # user name is same as directory name
    folder_name = db.session.query(Users.user_name).filter(Users.id==current_user.id).first()[0]

    # query image names
    image_objs = db.session.query(Images).filter(Images.user_id==current_user.id).all()    

    return render_template('images.html', image_objs=image_objs, folder_name=folder_name)    


@app.route('/delete/<id_given>')
def delete_image(id_given):
    id_given = int(id_given)
    record = Images.query.get_or_404(id_given)    
    image_name = record.image_name

    target = os.path.join(APP_ROOT, f'img/{current_user.user_name}')
    destination = "/".join([target, image_name])    

    try:
        os.remove(destination)
        db.session.delete(record)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'