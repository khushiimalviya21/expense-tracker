pipeline {
    agent any

    environment {
        ACR_NAME = 'khushiac2025'
        IMAGE_NAME = 'expense-tracker-app'
        IMAGE_TAG = "v${BUILD_NUMBER}"
        K8S_NAMESPACE = 'default'
        SUBSCRIPTION_ID = '23774a2f-cbc0-4b0a-8ac2-c3375e8ac4a2'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'git-creds', url: 'https://github.com/khushiimalviya21/expense-tracker.git', branch: 'main'
            }
        }

        stage('Azure Login') {
            steps {
                withCredentials([string(credentialsId: 'azure-sp-creds', variable: 'AZURE_SP_JSON')]) {
                    sh '''
                        echo "$AZURE_SP_JSON" > sp.json
                        CLIENT_ID=$(jq -r .clientId sp.json)
                        CLIENT_SECRET=$(jq -r .clientSecret sp.json)
                        TENANT_ID=$(jq -r .tenantId sp.json)

                        az login --service-principal \
                            --username $CLIENT_ID \
                            --password $CLIENT_SECRET \
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

                    # Apply PVC before deployment & service
                    kubectl apply -f k8s/pvc.yaml -n $K8S_NAMESPACE

                    sed "s|__IMAGE__|$ACR_NAME.azurecr.io/$IMAGE_NAME:$IMAGE_TAG|" k8s/deployment.yaml > k8s/deployment-updated.yaml

                    kubectl apply -f k8s/deployment-updated.yaml -n $K8S_NAMESPACE
                    kubectl apply -f k8s/service.yaml -n $K8S_NAMESPACE

                    kubectl rollout status deployment/expense-tracker-deployment -n $K8S_NAMESPACE
                '''
            }
        }
    }
}
