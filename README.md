# Customer API

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)
[![Build Status](https://github.com/CSCI-GA-2820-FA23-003/customers/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-FA23-003/customers/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-FA23-003/customers/graph/badge.svg?token=7IZGAQOHX2)](https://codecov.io/gh/CSCI-GA-2820-FA23-003/customers)

## Overview

The Customer API is organized around REST. Our API has predictable resource-oriented URLs, accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes and verbs.

## Available Endpoints

### List all customers

* `GET /customers`

### Create a new customer

* `POST /customers`
* Parameters:
  
  | Parameter name | Type | Required |
  | ----------- | ----------- | --------- |
  | first_name | String | Yes |
  | last_name | String | Yes |
  | email | String | Yes |
  | address | String | Yes |

### Retrieve a customer

* `GET /customers/{customer_id}`

### Update a customer

* `PUT /customers/{customer_id}`
* Parameters:
  
  | Parameter name | Type | Required |
  | ----------- | ----------- | --------- |
  | first_name | String | Yes |
  | last_name | String | Yes |
  | email | String | Yes |
  | address | String | Yes |

### Delete a customer

* `DELETE /customers/{customer_id}`

## Deploy to Local Kubernetes Cluster

### Prerequisites
- Kubernetes: Open the Extensions view in VS Code, search for and install Kubernetes Extensions.
- [Make](https://www.gnu.org/software/make/): Make sure Make is installed on your system.

### Getting Started

#### Step 1: Create a Kubernetes cluster with K3d

Run the following command in the terminal to start a Kubernetes cluster:

```bash
make cluster
```

#### Step 2: Build and Push Docker image

Using the following command to build the project as a Docker image, tag with the registry location, and push it to the registry. Don't forget to mapped cluster-registry:32000 to 127.0.0.1 in the /etc/hosts file before push.

```bash
docker build -t customer:1.0 .
docker tag customer:1.0 cluster-registry:32000/customer:1.0
docker push cluster-registry:32000/customer:1.0
```

#### Step 3: Run Command to Deploy the Kubernetes Cluster

Run the following command in turn to deploy Postgres database as StatefulSet and image we created. Using kubectl get all to check if *pod/postgres-statefulset* and *pod/customer* are running.

```bash
kubectl apply -f k8s/pv.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/postgress.yaml

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

### Cleanup

After testing, clean up the deployed resources:

```bash
make cluster-down
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
