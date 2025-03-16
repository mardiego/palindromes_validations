#!/bin/bash

DOCKER_REGISTRY="diegomartinezazcona"
DOCKER_IMAGE_NAME="palindromes"
HELM_RELEASE_NAME="palindromes"
HELM_CHART_PATH="./helm"
HELM_VALUES_PATH="./helm/values-dev.yaml"
DOCKER_TAG="dev"
NAMESPACE="development"

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "No environment argument provided. Use default development environment."
else
  if [[ "$1" == "development" ]]; then
    echo "Environment is set to: $1"
    NAMESPACE=$1
    DOCKER_TAG="dev"
  elif [[ "$1" == "production" ]]; then
    echo "Environment is set to: $1"
    NAMESPACE=$1
    DOCKER_TAG="prod"
  else
    echo "Invalid environment. Use default development environment."
  fi
fi

#Update values.yml file
if [[ "$NAMESPACE" == "development" ]]; then
  echo "Updating values.yml file to development"
  HELM_VALUES_PATH="./helm/values-dev.yaml"
else
  echo "Updating values.yml file to production"
  HELM_VALUES_PATH="./helm/values-prod.yaml"
fi

# Step 1: Build the Docker image
echo "Building Docker image..."
docker build -t $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_TAG .

if [ $? -ne 0 ]; then
  echo "Docker build failed!"
  exit 1
fi

# Step 2: Login to Docker (if required)
echo "Logging into Docker..."
docker login

if [ $? -ne 0 ]; then
  echo "Docker login failed!"
  exit 1
fi


# Step 3: Push the Docker image to Docker registry
echo "Pushing Docker image to $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_TAG..."
docker push $DOCKER_REGISTRY/$DOCKER_IMAGE_NAME:$DOCKER_TAG

if [ $? -ne 0 ]; then
  echo "Docker push failed!"
  exit 1
fi

# Step 4: Ensure kubectl is configured
echo "Ensuring kubectl is configured..."
kubectl config current-context

if [ $? -ne 0 ]; then
  echo "kubectl is not properly configured! Please configure kubectl first."
  exit 1
fi

# Step 6: Validate if the namespace exists using kubectl
kubectl get namespace $NAMESPACE &> /dev/null

# Step 7: Check if the command was successful (namespace exists)
if [ $? -ne 0 ]; then
  echo "Namespace '$NAMESPACE' does not exist. Creating it..."
  kubectl create namespace $NAMESPACE
else
  echo "Namespace '$NAMESPACE' exists."
fi

# Step 8: Deploy the application to Kubernetes using Helm
echo "Deploying with Helm..."
helm upgrade --install $HELM_RELEASE_NAME $HELM_CHART_PATH --namespace $NAMESPACE -f $HELM_VALUES_PATH --set image.tag=$DOCKER_TAG  --recreate-pods --reuse-values

if [ $? -ne 0 ]; then
  echo "Helm deployment failed!"
  exit 1
fi

echo "Deployment successful!"
