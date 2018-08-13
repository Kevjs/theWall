from django.db import models
import re, bcrypt

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]")

class UserManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First Name is too short"
        elif not NAME_REGEX.match(postData["first_name"]):
            errors["first_name"] = "Not a valid first name"
        if len(postData["last_name"]) < 2:
            errors["last_name"] = "Last Name is too short"
        elif not NAME_REGEX.match(postData["last_name"]):
            errors["last_name"] = "Not a valid last name"
        if len(postData["email"]) < 1:
            errors["email"] = "Email is blank"
        elif not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Email is not valid"
        if len(postData["password"]) < 8:
            errors["password"] = "Passwords is not long enough"
        elif not PASSWORD_REGEX.match(postData["password"]):
            errors["password"] = "Password is not valid"
        elif postData["password"] != postData["confirm_password"]:
            errors["confirm_password"] = "Passwords don't match"
        return errors
    
    def creator(self, postData):
        return User.objects.create(first_name=postData["first_name"], last_name=postData["last_name"], email=postData["email"], password = bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt()))
    
    def login_validator(self, postData):
        errors = {}
        if len(postData["email"]) < 1:
            errors["email"] = "Email is blank"
            return errors
        elif User.objects.filter(email=postData["email"]):
            user = User.objects.get(email=postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                return errors
        errors["matching"] = "Password or Email was incorrect"
        return errors
        
        

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()