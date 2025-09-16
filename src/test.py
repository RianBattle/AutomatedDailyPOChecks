with open("./data.txt", mode="r") as file:
  data = file.read()
  
arr = data.split("\n")
output = ""
for line in arr:
  output += "'" + line + "',\n"

with open("./output.txt", mode="w") as file:
  file.write(output)