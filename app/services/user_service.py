users = [
    {
        "id": 1,
        "name": "Rahul",
        "email": "rahul@example.com"
    },
    {
        "id": 2,
        "name": "Amit",
        "email": "amit@example.com"
    }
]

def get_all_users():
    return users

def get_user_by_id(id: int):
    for user in users:
        if user["id"] == id:
            return user
    return None
