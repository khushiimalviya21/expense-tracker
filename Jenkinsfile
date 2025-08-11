pipeline {
    agent any

    environment {
        ACR_NAME = 'youracrname' // without .azurecr.io
        IMAGE_NAME = 'expense-tracker'
        IMAGE_TAG = 'latest'
        K8S_NAMESPACE = 'default'
        SUBSCRIPTION_ID = 'fc6f7b5a-00d0-4ea1-b48a-2ebd00c943df'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // If public repo
                git branch: 'main', url: 'https://github.com/khushiimalviya21/expense-tracker.git'

                // If private repo, uncomment below & comment above
                // git credentialsId: 'github-creds', url: 'https://github.com/khushiimalviya21/expense-tracker.git', branch: 'main'
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
                    kubectl apply -f deployment.yaml -n $K8S_NAMESPACE
                    kubectl apply -f service.yaml -n $K8S_NAMESPACE
                '''
            }
        }
    }
}
