import os

path = "../pages/24"

for subdir, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".html") and file.find("#") >= 0:
            filename = os.path.join(subdir, file)
            os.rename(filename, filename.replace("#", "Event "))
            print(filename.replace("#", "Event"))
