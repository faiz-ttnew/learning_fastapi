from app.schemas.auth_schema import UserRegister

user = UserRegister(
    name="  Faijuddin  ",
    email="faiz@example.com",
    password="MyLearningPassword123"
)

print("Name:", user.name)
print("Email:", user.email)
print("Password:", user.password)