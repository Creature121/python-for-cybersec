import os  # Unused import?  # noqa: F401

print("Malicious file executed")
with open("out.txt", "w") as f:
    f.write("Executed")
