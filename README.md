# Customer API

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

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

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
