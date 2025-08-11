pipeline {
    agent any

    environment {
        // GitHub credentials configured in Jenkins
        GIT_CREDENTIALS_ID = 'github-creds'
        // ACR credentials configured in Jenkins
        ACR_CREDENTIALS_ID = 'acr-creds'
        // Azure Service Principal credentials configured in Jenkins
        AZURE_CLIENT_ID = credentials('azure-client-id')
        AZURE_CLIENT_SECRET = credentials('azure-client-secret')
        AZURE_TENANT_ID = credentials('azure-tenant-id')

        // Your Azure resources info
        AZURE_SUBSCRIPTION_ID = '12345678-aaaa-bbbb-cccc-1234567890ab'     // Replace with your subscription ID
        ACR_NAME = 'khushiacr2025'
        AKS_RESOURCE_GROUP = 'expense-rg'
        AKS_CLUSTER_NAME = 'khushiaks'

        IMAGE_NAME = "${ACR_NAME}.azurecr.io/expense-tracker-app:${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/khushiimalviya21/expense-tracker.git', credentialsId: "${GIT_CREDENTIALS_ID}"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t expense-tracker-app:${BUILD_NUMBER} ."
            }
        }

        stage('Login to ACR') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${ACR_CREDENTIALS_ID}", usernameVariable: 'ACR_USER', passwordVariable: 'ACR_PASS')]) {
                    sh "echo $ACR_PASS | docker login ${ACR_NAME}.azurecr.io -u $ACR_USER --password-stdin"
                }
            }
        }

        stage('Tag and Push Image') {
            steps {
                sh "docker tag expense-tracker-app:${BUILD_NUMBER} ${IMAGE_NAME}"
                sh "docker push ${IMAGE_NAME}"
            }
        }

        stage('Deploy to AKS') {
            steps {
                sh """
                az login --service-principal -u ${AZURE_CLIENT_ID} -p ${AZURE_CLIENT_SECRET} --tenant ${AZURE_TENANT_ID}
                az account set --subscription ${AZURE_SUBSCRIPTION_ID}
                az aks get-credentials --resource-group ${AKS_RESOURCE_GROUP} --name ${AKS_CLUSTER_NAME} --overwrite-existing

                kubectl set image deployment/expense-tracker-deployment expense-tracker-container=${IMAGE_NAME}
                kubectl rollout status deployment/expense-tracker-deployment
                """
            }
        }
    }

    post {
        always {
            sh 'az logout || true'
            sh "docker logout ${ACR_NAME}.azurecr.io || true"
        }
    }
}

