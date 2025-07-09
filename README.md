
### CRUD app using FastAPI 
#### hosted on local using Docker

#### Install Docker on local using wsl

```
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
```

#### Build and run this application

```
sudo docker build -t fastapi-crud .
sudo docker run -d -p 8000:8000 fastapi-crud
```

##### Now the app is running at localhost:8000/users
To see and test the API go to localhost:8000/docs


---






Old version:
### CRUD app using FastAPI 
##### hosted on local using uvicorn
![CRUD Operation](https://github.com/user-attachments/assets/4816a8f8-b334-441c-93f3-2445cf4de909)
---

#### Create Operation

![Screenshot 2025-06-13 165957](https://github.com/user-attachments/assets/3d6582b7-5e27-46bd-8297-dce0bc4895c8)
![Screenshot 2025-06-13 170058](https://github.com/user-attachments/assets/e3bac5b8-b683-4035-b5e0-4df55c268dc1)

#### Read operation:
![Screenshot 2025-06-13 170306](https://github.com/user-attachments/assets/088283d0-a18f-4fb9-8124-603746a48c13)

#### Patch(Update) Operation:


![Screenshot 2025-06-13 170155](https://github.com/user-attachments/assets/cc9e921a-ef34-48bc-b04c-01d8e1bbf535)
![Screenshot 2025-06-13 170227](https://github.com/user-attachments/assets/f0b2bf22-34a1-400c-b833-26bf7ee03e29)

#### Delete operation:

![Screenshot 2025-06-13 170406](https://github.com/user-attachments/assets/13dce056-1611-4f18-8180-bdee501f44bd)

