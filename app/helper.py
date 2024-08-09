from flask_mail import Message
from app import mail
from flask import current_app
from flask import url_for
from app import mail

def send_email(subject, recipient, body):
    msg = Message(subject, sender='your_email@example.com', recipients=[recipient])
    msg.body = body
    mail.send(msg)

'''


def save_picture( form_picture, path, output_size=None ):
	random_hex=secrets.token_hex(8)
	#return the extension of an Image and ignore the name of it
	_, picture_ext = os.path.splitext(form_picture.filename) 
	picture_name= random_hex + picture_ext
	picture_path= os.path.join(current_app.root_path, path, picture_name)
	i=Image.open(form_picture)
	if output_size:
		output_size=output_size
		i.thumbnail(output_size)
	i.save(picture_path)
	return picture_name


def delete_picture(picture_name, path):
    picture_path = os.path.join(current_app.root_path, path, picture_name)
    try:
        os.remove(picture_path)
    except:
        pass
          
    
'''




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
   

