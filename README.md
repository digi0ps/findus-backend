# FindUS - The People Gallery

📚 Backend for the project FindUs done for the course Content Based Image Retrieval (CSE3018). 📚

🐍 Done completely using **Django** in **Python** 🐍

🎭 Thanks to Ageitgey's amazing [Face Recognition Library](https://github.com/ageitgey/face_recognition) 🎭

## About FindUs

FindUs is a Web App which gives users a *photo gallery on steroids*. User's can upload and store images on the website. The faces of people are identified in the images uploaded. This allows user to label them, group photos by person and retrieve similar images of a person from a search image.


## Features

- Receive images via POST and store/serve them from Media folder.
- Identify all persons in an image with the help of the Face Recognition library and save them in Person's database.
- API endpoint to return images with the details of person's in them.

## How does it work? 

1. When an image is uploaded, it is run through DLib's algorithm and faces are detected first.
2. Once the face is detected, the encoding is calculated. 
3. If the database is empty, a new Person entry is created with this encoding and a random name.
4. Else, the encoding is compared with existing encodings. 
   - If an existing encoding matches, then the Person is added to the Image entry.
   -  Else a new entry is created and is added to the image.

## Endpoints
- `/api/gallery/` **GET**: Returns a list of images with persons details attached.
- `/api/gallery/` **POST**: Upload an image to the website.
- `/api/person/` **GET**: Returns the list of persons existing in thedatabase.
- `/api/person/` **POST**: Update the name of a person with ID.
- `/api/search/` **POST**: Upload a search image and returns list of images matching the persons in the search image.