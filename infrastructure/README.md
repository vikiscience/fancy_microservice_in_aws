[//]: # (Image References)

[image1]: images/Snapshot_CF_Stacks.PNG
[image2]: images/Snapshot_Cluster.PNG
[image3]: images/Snapshot_Node.PNG

# Infrastructure as Code using AWS CloudFormation

The Company is creating a web application called **Fancy App** with ML in the backend, which predicts some valuable outcome based on user's input. Developers pushed the latest version of their code in a GitHub repository.

The task is now to create Infrastructure as Code, where the application will be deployed to later on. This needs to be done in an automated fashion so that the infrastructure can be replicated to be the productive environment or discarded as soon as the testing team finishes their work within the testing environment.

Note: we assume that the AWS CLI is installed on a DevOp's working station in order to run the CloudFormation scripts below.


## Create Network Infrastructure

Run following scripts:

```batch
run_create_stack.bat prj-network-stack infra_network.yaml infra_network_params.json

run_update_stack.bat prj-network-stack infra_network.yaml infra_network_params.json
```


## Add Kubernetes Cluster

Run following scripts:

```batch
run_create_stack.bat prj-cluster-stack infra_cluster.yaml infra_cluster_params.json

run_update_stack.bat prj-cluster-stack infra_cluster.yaml infra_cluster_params.json
```


## Test

See the status of 2 stacks:

![Stacks][image1]

We can check if the Cluster appears in the AWS Management Console under "EKS" Service:

![App][image2]

Also, the only node is running as EC2 instance alongside with Jenkins Box:

![App][image3]
