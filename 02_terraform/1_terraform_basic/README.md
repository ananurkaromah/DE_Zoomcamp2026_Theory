#### flow 
terraform/
│
├── 1_terraform_basic/
│   └── main.tf
│
├── 2_terraform_with_variables/
    ├── main.tf
    └── variables.tf
<br>

#### Setting up GCS (data lake)

1. create GCP account
    https://cloud.google.com/
    
    a. Sign in with your Google account
    b. Activate free trial (EUR 300 credits)
2. Create a New Project
    https://console.cloud.google.com/
    
    a. Click Project dropdown (top left)
    b. Click New Project
    c. Name it eg: DTC DE Course
    d. click Create
    e. copy your project id and keep it
3. Create Service Account
    a. fill field name e.g: dtc-de-zoomcamp
    b. fill  field description e.g: Service account for zoomcamp
    c. click Create and Continue
    d. grant role
    e. Click continue and done
4. Download JSON Key
    a. click your service account
    > -Viewer
    > -Storage Admin
    > -Storage Object Admin
    > -BigQuery Admin

    b. go to Keys
    c. click Add Key → Create New Key
    d. choose: JSON
    e. Click Create (The file will download. Move  and keep it somewhere safe). You can make a directory name **keys** and file with name **my_creds.json.**
    for safety your key credential in bash you run code:
    
    ```jsx
    export GOOGLE_APPLICATION_CREDENTIALS="path/to/file.json"
    
    ```
    
    verify with
    
    ```jsx
    echo $GOOGLE_APPLICATION_CREDENTIALS
    ```
    
    output:
    
    ```jsx
    /workspaces/.../my_creds.json
    ```
<br>

### GCS init

1. After GCS install in linux , run:
    
    ```jsx
    gcloud init
    ```
    
2. Copy the long URL shown in terminal
3. Open it in your browser
4. Login with your Google account (the one with your GCP project) →Click  **Allow**
5. Google will show you a **verification code**
6. Copy that code
7.  Paste it back into the terminal and press Enter
8. gcloud will:
    - List your available projects
    - Ask you to select one
        
        ```
        Pick cloud project to use:
         [1] project-1
         [2] dtc-de-course-12345
         [3] Create a new project
        ```
        
        Type the number corresponding to your Zoomcamp project.
        
        Finish for gcloud init.
        
        ### After gcloud init Finishes
        
        Run this (VERY important for Terraform):
        
        ```
        gcloud auth application-default login
        ```
        
        This is different from `gcloud init`.
        
        Why?
        
        - `gcloud init` → configures CLI
        - `application-default login` → creates credentials Terraform uses
        
        Terraform needs the second one.
        
        This will:
        
        - Open a browser link
        - Ask for login
        - Generate Application Default Credentials (ADC)
        
        Terraform uses this authentication.
        
        If successful, you’ll see something like:
        
        ```
        Credentials saved to file:
        ~/.config/gcloud/application_default_credentials.json
        ```
        
        That means Terraform can now talk to GCP.
        
        Don`t forget to add extention terraform in VSCode

### Making bucket in GCS for terraform_basic

1. Go to https://console.cloud.google.com/
2. in navigation menu and click Cloud Storage and choose Bucket, for the first it will still empty
3. go to [terraform google provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs?q=google+cloud+platform+provider)
    
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
    
    but in this module go to site  [de zoomcamp for main.tf terraform_basic](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/terraform/terraform/terraform_basic/main.tf) you use version "4.51.0"
    
    ```jsx
    terraform {
      required_providers {
        google = {
          source  = "hashicorp/google"
          version = "4.51.0"
        }
      }
    }
    ```
    
    for #configuration options we can copy this in website
    
    ```jsx
    project     = "dtc-de-course-488404"
    region      = "us-central1"
    ```
    
    **Define a GCP Bucket, t**o create a storage bucket in GCP, update your `main.tf` with the following resource definition:
    
    ```jsx
    terraform {
      required_providers {
        google = {
          source  = "hashicorp/google"
          version = "4.51.0"
        }
      }
    }
    
    provider "google" {
    # Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
    #  credentials = 
      project = "dtc-de-course-488404"
      region  = "us-central1"
    }
    
    resource "google_storage_bucket" "data-lake-bucket" {
      name          = "dtc-de-course-488404-data-lake-2026-ana"
      location      = "US"
    
      # Optional, but recommended settings:
      storage_class = "STANDARD"
      uniform_bucket_level_access = true
    
      versioning {
        enabled     = true
      }
    
      lifecycle_rule {
        action {
          type = "Delete"
        }
        condition {
          age = 30  // days
        }
      }
    
      force_destroy = true
    }
    
    resource "google_bigquery_dataset" "dataset" {
      dataset_id = "dtc_demo_bucket_terraform_488404"
      project    = "dtc-de-course-488404"
      location   = "US"
    }
    ```
    
    Here’s what each part does:
    
    - **`name`**: Specifies the bucket name, which must be globally unique.
    - **`location`**: Sets the bucket’s geographic region.
    - **`force_destroy`**: Ensures the bucket and its contents are deleted when the resource is destroyed.
    - **`lifecycle_rule`**: Configures the bucket lifecycle. In this example, it deletes incomplete multipart uploads after one day.

4.  **Initializes & configures the backend,**

```jsx
terraform init
```

Terraform will output:

```jsx
Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/google versions matching "4.51.0"...
- Installing hashicorp/google v4.51.0...
- Installed hashicorp/google v4.51.0 (signed by HashiCorp)
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

5. **Plan and Apply**
    
    Next, preview the changes with:
    
    ```jsx
    terraform plan
    ```
    
    Terraform will output a plan detailing the resources to be created.
    
    ```jsx
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create
    
    Terraform will perform the following actions:
    
      # google_bigquery_dataset.dataset will be created
      + resource "google_bigquery_dataset" "dataset" {
          + creation_time              = (known after apply)
          + dataset_id                 = "dtc_demo_bucket_terraform_488404"
          + delete_contents_on_destroy = false
          + etag                       = (known after apply)
          + id                         = (known after apply)
          + labels                     = (known after apply)
          + last_modified_time         = (known after apply)
          + location                   = "US"
          + project                    = "dtc-de-course-488404"
          + self_link                  = (known after apply)
    
          + access (known after apply)
        }
    
      # google_storage_bucket.data-lake-bucket will be created
      + resource "google_storage_bucket" "data-lake-bucket" {
          + force_destroy               = true
          + id                          = (known after apply)
          + location                    = "US"
          + name                        = "dtc-de-course-488404-data-lake-2026-ana"
          + project                     = (known after apply)
          + public_access_prevention    = (known after apply)
          + self_link                   = (known after apply)
          + storage_class               = "STANDARD"
          + uniform_bucket_level_access = true
          + url                         = (known after apply)
    
          + lifecycle_rule {
              + action {
                  + type          = "Delete"
                    # (1 unchanged attribute hidden)
                }
              + condition {
                  + age                    = 30
                  + matches_prefix         = []
                  + matches_storage_class  = []
                  + matches_suffix         = []
                  + with_state             = (known after apply)
                    # (3 unchanged attributes hidden)
                }
            }
    
          + versioning {
              + enabled = true
            }
    
          + website (known after apply)
        }
    
    Plan: 2 to add, 0 to change, 0 to destroy.
    
    ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    
    Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run "terraform apply" now.
    ```
    
    Confirm the plan with:
    
    ```jsx
    terraform apply
    ```
    
    Asks for approval to the proposed plan, and applies changes to cloud
    
    Once applied, navigate to the GCP Storage console to verify that the bucket has been created. Terraform also updates the `terraform.tfstate` file to store the current state of your infrastructure.
    
    the output:
    
    ```jsx
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create
    
    Terraform will perform the following actions:
    
      # google_bigquery_dataset.dataset will be created
      + resource "google_bigquery_dataset" "dataset" {
          + creation_time              = (known after apply)
          + dataset_id                 = "dtc_demo_bucket_terraform_488404"
          + delete_contents_on_destroy = false
          + etag                       = (known after apply)
          + id                         = (known after apply)
          + labels                     = (known after apply)
          + last_modified_time         = (known after apply)
          + location                   = "US"
          + project                    = "dtc-de-course-488404"
          + self_link                  = (known after apply)
    
          + access (known after apply)
        }
    
      # google_storage_bucket.data-lake-bucket will be created
      + resource "google_storage_bucket" "data-lake-bucket" {
          + force_destroy               = true
          + id                          = (known after apply)
          + location                    = "US"
          + name                        = "dtc-de-course-488404-data-lake-2026-ana"
          + project                     = (known after apply)
          + public_access_prevention    = (known after apply)
          + self_link                   = (known after apply)
          + storage_class               = "STANDARD"
          + uniform_bucket_level_access = true
          + url                         = (known after apply)
    
          + lifecycle_rule {
              + action {
                  + type          = "Delete"
                    # (1 unchanged attribute hidden)
                }
              + condition {
                  + age                    = 30
                  + matches_prefix         = []
                  + matches_storage_class  = []
                  + matches_suffix         = []
                  + with_state             = (known after apply)
                    # (3 unchanged attributes hidden)
                }
            }
    
          + versioning {
              + enabled = true
            }
    
          + website (known after apply)
        }
    
    Plan: 2 to add, 0 to change, 0 to destroy.
    
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.
    
      Enter a value: yes
    
    google_bigquery_dataset.dataset: Creating...
    google_storage_bucket.data-lake-bucket: Creating...
    google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/dtc-de-course-488404/datasets/dtc_demo_bucket_terraform_488404]
    google_storage_bucket.data-lake-bucket: Creation complete after 1s [id=dtc-de-course-488404-data-lake-2026-ana]
    
    Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
    ```
    

7. **Destroy Resources**

When you no longer need the resources, clean up with:

```
terraform destroy
```

After the command executes, refresh the GCP console to confirm the bucket has been deleted.

<br>

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
