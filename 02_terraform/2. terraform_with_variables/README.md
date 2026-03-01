#### Making bucket in GCS for terrraform with variable

1. Go to google and search 
    
    [terraform google provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs?q=google+cloud+platform+provider)
    
    in upper right we can click **USE PROVIDER** and copy.
    
    ```jsx
    terraform {
      required_providers {
        google = {
          source = "hashicorp/google"
          version = "7.21.0"
        }
      }
    }
    
    provider "google" {
      # Configuration options
    }
    ```
    
    but in this module go to site  [de zoomcamp for main.tf terraform_](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/terraform/terraform/terraform_basic/main.tf)with_version you use version "5.6.0""
    
2. **Define a GCP Bucket, t**o create a storage bucket in GCP, update your `main.tf` with the following resource definition like above:
    
    ```jsx
    terraform {
      required_providers {
        google = {
          source  = "hashicorp/google"
          version = "5.6.0"
        }
      }
    }
    
    provider "google" {
      credentials = file(var.credentials)
      project     = var.project
      region      = var.region
    }
    
    resource "google_storage_bucket" "demo-bucket" {
      name          = var.gcs_bucket_name
      location      = var.location
      force_destroy = true
    
      lifecycle_rule {
        condition {
          age = 1
        }
        action {
          type = "AbortIncompleteMultipartUpload"
        }
      }
    }
    
    resource "google_bigquery_dataset" "demo_dataset" {
      dataset_id = var.bq_dataset_name
      location   = var.location
    }
    ```
    

3. **Using Variables**

      To make your configuration more dynamic, replace hardcoded values with variables. Create a `variables.tf` file for variable declarations. For instance, to define variables for a BigQuery dataset and storage bucket:

    ```jsx
    variable "credentials" {
    description = "My Credentials"
    default     = "<Path to your Service Account json file>"
    #ex: if you have a directory where this file is called keys with your service account json file
    #saved there as my-creds.json you could use default = "./keys/my-creds.json"
    }

    variable "project" {
    description = "Project"
    default     = "<Your Project ID>"
    }

    variable "region" {
    description = "Region"
    #Update the below to your desired region
    default     = "us-central1"
    }

    variable "location" {
    description = "Project Location"
    #Update the below to your desired location
    default     = "US"
    }

    variable "bq_dataset_name" {
    description = "My BigQuery Dataset Name"
    #Update the below to what you want your dataset to be called
    default     = "demo_dataset"
    }

    variable "gcs_bucket_name" {
    description = "My Storage Bucket Name"
    #Update the below to a unique bucket name
    default     = "terraform-demo-terra-bucket"
    }

    variable "gcs_storage_class" {
    description = "Bucket Storage Class"
    default     = "STANDARD"
    }
    ```
<br>
<br>

###### Don’t push your credential file, add this code in file gitignore

```
# Ignore GCP credentials
*.json
keys/
```