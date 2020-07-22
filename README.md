# fancy_microservice_in_aws

An ML microservice is deployed to Kubernetes Cluster in AWS via CI/CD pipeline using Jenkins


## Prerequisites

#### Jenkins server:

* EC2 instance on AWS
* has Jenkins with BlueOcean and AWS plugins 
* has Docker, `kubectl`, hadolint and tidy installed
* polls every 2 minutes for code changes in GitHub repository


#### Kubernetes Cluster

The Infrastructure is created using CloudFormation scripts, see [this doku](infrastructure/README.md) in subfolder `infrastructure`.

Manual steps on the cluster:

```shell script
aws eks --region us-west-2 update-kubeconfig --name fancy_cluster  --kubeconfig="~/.kube/config_aws"

kubectl --kubeconfig="~/.kube/config_aws" create namespace fancy-namespace

kubectl --kubeconfig="~/.kube/config_aws" get all -n fancy-namespace

kubectl --kubeconfig="~/.kube/config_aws" describe -n fancy-namespace pods
```


