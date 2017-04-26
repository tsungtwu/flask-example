

def init_model(sqlDAO):
    from .userModel import User
    sqlDAO.create_all()
