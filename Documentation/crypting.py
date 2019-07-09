from flask_bcrypt import Bcrypt

"""
Usefull functions for the crypting part

app is a Flask object
bcrypt = Bcrypt(app)


bcrypt.generate_password_hash("text")
returns the string but crypted in binary format

bcrypt.generate_password_hash("text").decode('utf-8')
returns the string but crypted in string format


bcrypt.check_password_hash(hashed_password,text_password)
reurns true of the password are the same


"""