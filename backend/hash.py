from werkzeug.security import generate_password_hash

senha_hash = generate_password_hash("admin", method="pbkdf2:sha256", salt_length=16)
print(senha_hash)

# Gera hash da senha com bcrypt usada para autenticação, ainda não implementado só testes 