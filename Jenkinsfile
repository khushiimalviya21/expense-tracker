pipeline {
    agent any
    
    environment {
        ACR_NAME = "khushiacr2025"                 // your ACR name
        IMAGE_NAME = "expense-tracker-app"
        RESOURCE_GROUP = "expense-rg"
        AKS_CLUSTER_NAME = "khushi-aks"
        AZURE_CREDENTIALS_ID = "azure-sp"          // your Azure credentials ID in Jenkins
        ACR_CREDENTIALS_ID = "acr-creds"            // your ACR credentials ID in Jenkins
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"  // tag image with build number
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/khushiimalviya21/expense-tracker.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${DOCKER_IMAGE_TAG}")
                }
            }
        }
        
        stage('Login to ACR') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${ACR_CREDENTIALS_ID}", passwordVariable: 'ACR_PASS', usernameVariable: 'ACR_USER')]) {
                    sh "docker login ${ACR_NAME}.azurecr.io -u $ACR_USER -p $ACR_PASS"
                }
            }
        }
        
        stage('Push Image to ACR') {
            steps {
                sh "docker push ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
            }
        }
        
        stage('Deploy to AKS') {
            steps {
                withCredentials([azureServicePrincipal(credentialsId: "${AZURE_CREDENTIALS_ID}")]) {
                    sh '''
                    az login --service-principal -u $AZURE_CLIENT_ID -p $AZURE_CLIENT_SECRET --tenant $AZURE_TENANT_ID
                    az aks get-credentials --resource-group ${RESOURCE_GROUP} --name ${AKS_CLUSTER_NAME} --overwrite-existing
                    kubectl set image deployment/expense-tracker-deployment expense-tracker=${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${DOCKER_IMAGE_TAG}
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo 'Deployment succeeded!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}
