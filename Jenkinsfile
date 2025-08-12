pipeline {
    agent any

    environment {
        ACR_NAME = 'khushiacr2025' // without .azurecr.io
        IMAGE_NAME = 'expense-tracker-app'
        IMAGE_TAG = "v${BUILD_NUMBER}"         // Changed to unique tag per build
        K8S_NAMESPACE = 'default'
        SUBSCRIPTION_ID = 'fc6f7b5a-00d0-4ea1-b48a-2ebd00c943df'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // If public repo
                // git branch: 'main', url: 'https://github.com/khushiimalviya21/expense-tracker.git'

                // If private repo, uncomment below & comment above
                git credentialsId: 'git-creds', url: 'https://github.com/khushiimalviya21/expense-tracker.git', branch: 'main'
            }
        }

        stage('Azure Login') {
            steps {
                withCredentials([string(credentialsId: 'azure-sp-creds', variable: 'AZURE_SP_JSON')]) {
                    sh '''
                        echo "$AZURE_SP_JSON" > sp.json
                        CLIENT_ID=$(jq -r .appId sp.json)
                        CLIENT_SECRET=$(jq -r .password sp.json)
                        TENANT_ID=$(jq -r .tenant sp.json)

                        az login --service-principal \
                            -u $CLIENT_ID \
                            -p $CLIENT_SECRET \
                            --tenant $TENANT_ID

                        az account set --subscription $SUBSCRIPTION_ID
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }

        stage('Push to ACR') {
            steps {
                sh '''
                    az acr login --name $ACR_NAME
                    docker push $ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to AKS') {
            steps {
                sh '''
                    az aks get-credentials --resource-group expense-rg --name khushiaks --overwrite-existing

                    # Replace __IMAGE__ placeholder in deployment.yaml with the current image tag
                    sed "s|__IMAGE__|$ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG|" k8s/deployment.yaml > k8s/deployment-updated.yaml

                    kubectl apply -f k8s/deployment-updated.yaml -n $K8S_NAMESPACE
                    kubectl apply -f k8s/service.yaml -n $K8S_NAMESPACE

                    # Wait for rollout to finish
                    kubectl rollout status deployment/expense-tracker-deployment -n $K8S_NAMESPACE
                '''
            }
        }
    }
}
