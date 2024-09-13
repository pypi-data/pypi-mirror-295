import logging
from .models import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_user(username, hashed_password, email, full_name=None):
    # Add a new user
    user = User(username=username, email=email, hashed_password=hashed_password, full_name=full_name, disabled=False)
    user.save()
    return user


def register_user(username, password, email, full_name=None):
    # Add a new user
    pwd_hash = pwd_context.hash(password)
    user = create_user(username, pwd_hash, email, full_name=full_name)   
    return user

def read_user(user_pk: str):
  try:
     user = User.find(User.pk==user_pk).first()
     return user
  except Exception:
     logging.error(f"User {user_pk} not found.")


def read_user_by_name(username: str):
   try:
     user = User.find(User.username==username).first()
     return user
   except Exception:
     logging.error(f"User {username} not found.")
   
  

def update_user(user_pk: str, **kwargs):
   # Update user email or name
   try:
      user = read_user(user_pk)
      logging.info(f"Found user: {user.username}")
      if kwargs: 
         user.__dict__.update(kwargs)
         user.save()
         return user
   except Exception as e:
      logging.info(f"Error updating user {user_pk}: {str(e)}")
  

def delete_user(user_pk: str):
  try:
      user = read_user(user_pk)
      if user:
         user.delete(user.pk)
         logging.info(f"User {user.username} deleted.")
      else:
         logging.error(f"User {user_pk} not found.")
  except Exception as e:
      logging.error(f"Error deleting user {user_pk}: {str(e)}")

def disable_user(user_pk: str):
  try:
      user = read_user(user_pk)
      if user: 
         user.disabled = True
         user.save()
         return user
      else:
         logging.error(f"User {user_pk} not found")
  except Exception as e:
      logging.error(f"Error disabling user {user_pk}: {str(e)}")


def enable_user(user_pk: str):
  try:
      user = read_user(user_pk)
      if user: 
         user.disabled = False
         user.save()
         return user
      else:
         logging.error(f"User {user_pk} not found")
  except Exception as e:
      logging.error(f"Error enabling user {user_pk}: {str(e)}")

