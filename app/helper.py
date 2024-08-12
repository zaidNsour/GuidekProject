import secrets
from flask_mail import Message
from app import mail
from flask import jsonify
from flask import url_for
from app import mail
from PIL import Image
import os
from flask import send_file, jsonify



'''

'''


def upload_picture(image_file, path, output_size = None ):
  random_hex=secrets.token_hex(10)
  _, picture_ext = os.path.splitext(image_file.filename)
  picture_name= random_hex + picture_ext 
  picture_path= os.path.join(path, picture_name)
 
  allowed_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.ico', '.gif', '.svg']
  if picture_ext.lower() not in allowed_extensions:
    return "unsupported"
   
  try:
    i = Image.open(image_file)
    if output_size:
      i.thumbnail(output_size)
    i.save(picture_path)

  except Exception as e:
    return f"error: {str(e)}"
   
  return picture_name


def get_picture(path, filename):
  try:
    picture_path = os.path.abspath(os.path.join(path, filename))
    if not os.path.exists(picture_path):
        return jsonify({"error": "Image not found"}), 404

    extension_to_mime = {
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.bmp': 'image/bmp',
      '.tiff': 'image/tiff',
      '.webp': 'image/webp',
      '.ico': 'image/x-icon'
    }
    _, picture_ext = os.path.splitext(filename)
    # Get the mimetype based on the extension
    mime_type = extension_to_mime.get(picture_ext)
    if mime_type:    
      return send_file(picture_path, mimetype = mime_type)
    else:
      return jsonify({"error": "Unsupported image type"}), 400
    
  except Exception as e:
    return jsonify({"error": str(e)}), 500
  

def delete_picture(path, filename):
    picture_path = os.path.abspath(os.path.join(path, filename))
    try:
      os.remove(picture_path)

    except Exception as e:
      return jsonify({"error": str(e)}), 500
  



#use _external because redirect from email to this route 
def send_reset_email(user):    
  token= user.get_reset_token()
   #change email
  msg=Message('Password reset request', sender= 'zaidnsour1223@gmail.com',
               recipients= [user.email],
               body=f''' To reset your password, visit the following link:
               {url_for('users.reset_password', token=token, _external=True)}  
                if you did not make this request, please ignore this email'''
              )
  mail.send(msg)
   








