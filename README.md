# 🚀 Palindromes validation

## 📖 Overview
This project is designed to validate if a text is a palindromes. Successful requests will be stored 
in a database so can be later queried or deleted. It includes:
- Python scripts to handle requests
- Helm charts for Kubernetes deployment
- A Dockerfile to containerize the application
- Terraform scripts for infrastructure as code

## 📂 Project Structure
📁 palindromes_validations/
│── 📁 app/               # Python scripts
│── 📁 tests/             # Unit tests
│── 📁 helm/              # Helm charts
│── 📁 terraform/         # Terraform configurations
│── 📁 configs/           # Configuration files
│── Dockerfile            # Docker container setup
│── deployment.sh         # Deployment script for deploying the application in a Kubernetes cluster
│── README.md            # Project documentation
│── requirements.txt     # Python dependencies

---

## ⚙️ **Setup Instructions**

### 🏰️ 1. **Local Python Setup**
#### Install dependencies:
```sh
pip install -r src/requirements.txt
```
#### Run the API locally:
```sh
python3.11 -m uvicorn app.main:app --reload
```
The API will be available at:  
📌 `http://127.0.0.1:8000/`

---

### 🐳 2. **Docker Setup**
#### Build the Docker image:
```sh
 docker build -t palindrome .
```
#### Run the container:
```sh
docker run -p 8080:8080 palindrome
```
---

### 🏭️ 3. **Infrastructure Deployment with Terraform**
#### Navigate to the Terraform directory:
```sh
cd terraform
```
#### Initialize Terraform:
```sh
terraform init
```
#### Apply Terraform configuration:
```sh
terraform apply -auto-approve
```
This will deploy a Kubernetes cluster locally using Minikube.

---

### ☸️ 4. **Deploy to Kubernetes with `deployment.sh`**

The `deployment.sh` script automates the deployment process to a **Minikube Kubernetes cluster**. To deploy the application:

1. **Make the script executable:**
   ```sh
   chmod +x deployment.sh
   ```

2. **Run the deployment script:**
   ```sh
   ./deployment.sh [development | production]
   ```

The script will:
- Build the Docker image
- Push the image to a container registry
- Deploy Kubernetes in the desired environment (development or production)

---


## 📝 **API Endpoints**

### 1. **Validate if a string is a palindrome**
- **Method**: `POST`
- **Endpoint**: `/palindromes/validate_palindromes`
- **Description**: Validate if a string is a Palindrome. If yes, store it in a local sqlite3 db.

#### Request Body (JSON):
```json
{
  "text": "Text to validate",
  "language": "Language of the palindrome"
}
```

#### Example Request:
```sh
curl --location 'http://127.0.0.1:8080/palindromes/validate_palindromes' \
--header 'Content-Type: application/json' \
--data '{
    "text": "racecar",
    "language": "English"
}'
#### Response:
```json
{
    "response": "Palindrome racecar has been successfully added"
}
```

---

### 2. **Get  Palindromes**
- **Method**: `GET`
- **Endpoint**: `/palindromes/get_palindromes`
- **Description**: Retrieve palindromes matching the filters.

#### Query Parameters:
| Parameter  | Type     | Description                                     |
|------------|----------|-------------------------------------------------|
| `text`     | `string` | (Optional) Palindrome string to retrieve        |
| `language` | `string` | (Optional) Palindromes in the required language |

#### Example Request:
```sh
curl --location 'http://127.0.0.1:8080/palindromes/get_palindromes?language=English&text=raceca' \
--header 'sort-method: quick' \
--header 'pivot-position: 4' \
--data ''
```

---

### 3. **Delete a Palindrome**
- **Method**: `DEL`
- **Endpoint**: `/palindromes/delete_palindromes`
- **Description**: Delete a Palindrome.

#### Query Parameters:
| Parameter  | Type     | Description                 |
|------------|----------|-----------------------------|
| `text`     | `string` | Palindrome string to delete |
| `language` | `string` | Palindrome language         |


#### Example Request:
```sh
curl --location --request DELETE 'http://127.0.0.1:8080/palindromes/get_palindromes?language=English&text=raceca' \
--header 'sort-method: quick' \
--header 'pivot-position: 4' \
--data ''
```

#### Response:
```json
{
  "response": "Entry successfully deleted"
}
```

---

## 🧪 **Running Tests**
Run unit tests and review code coverage using:
```sh
 pytest tests --cov=app 
```

---

## 🚀 **Features**
- ✅ Python REST API using **FastAPI**
- ✅ Containerized with **Docker**
- ✅ Deployable on **Kubernetes** using `deployment.sh`
- ✅ Kubernetes cluster using **Minikube**
- ✅ Cloud infrastructure managed via **Terraform**
- ✅ Automated testing using **pytest**

----

---

## 👥 **Contributors**
- **Diego Martínez Azcona** – [email](dmarazc@gmail.com)


