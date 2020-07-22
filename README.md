[//]: # (Image References)

[image0]: infrastructure/images/Docker_Repo.PNG
[image1]: infrastructure/images/Deploy_Before.PNG
[image2]: infrastructure/images/Deploy_During.PNG
[image3]: infrastructure/images/Deploy_After.PNG
[image4]: infrastructure/images/Lint_fails.PNG
[image5]: infrastructure/images/Lint_passes.PNG

# fancy_microservice_in_aws

GitHub repo: https://github.com/vikiscience/fancy_microservice_in_aws

An ML microservice is deployed to Kubernetes Cluster in AWS via CI/CD pipeline using Jenkins


## Prerequisites

#### DockerHub repository

The docker images with the application inside are uploaded here by the Jenkins pipeline:

![Deployment][image0]


#### Jenkins server:

* EC2 instance `t2.micro` on AWS
* has Jenkins with BlueOcean and AWS plugins installed
* has Docker, `kubectl`, `hadolint` and `tidy` installed
* polls every 2 minutes for code changes in this GitHub repository


#### Kubernetes Cluster

The Infrastructure is created using CloudFormation scripts, see [this doku](infrastructure/README.md) in subfolder `infrastructure`.

Some manual steps on the cluster are needed before the Jenkins pipeline can run:

```shell script
aws eks --region us-west-2 update-kubeconfig --name fancy_cluster  --kubeconfig="~/.kube/config_aws"

kubectl --kubeconfig="~/.kube/config_aws" create namespace fancy-namespace

kubectl --kubeconfig="~/.kube/config_aws" get all -n fancy-namespace

kubectl --kubeconfig="~/.kube/config_aws" describe -n fancy-namespace pods
```

## Deployment

Rolling deployment strategy was chosen for the application, meaning that the updated app is gradually rolled out. 

Given the current deployment:

![Deployment][image1]

The rolling strategy is done by setting `strategy: type: RollingUpdate` in the `infrastructure/deployment.yaml`. 

Further on, if we set `initialDelaySeconds` to 5 minutes, then we see that there are 2 pods on the cluster for some time: one with the old deployment (state = `Running`), the other is new and has state = `ContainerCreating`:

![Deployment][image2]

After the new pod is ready, only the new deployment is seen:

![Deployment][image3]

## Tests

In order to see Jenkins pipeline in action, we can build an error in Linting step:

![Deployment][image4]

And after fixing the error this step passes, and the whole pipeline is green:

![Deployment][image5]
