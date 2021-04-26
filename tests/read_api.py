f = open(".api_key")

api_key = "".join([char for char in f.read() if char.isalnum()])

print(api_key)

f.close()
