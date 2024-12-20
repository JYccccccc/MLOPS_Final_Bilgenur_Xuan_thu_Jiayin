variable "project_id" {
  description = "GCP project id"
}

variable "region" {
  description = "GCP region"
  default     = "us-central1"
}

variable "instance_type" {
  description = "VM instance_type"
  default     = "e2-medium"
}

variable "instance_count" {
  description = "instance count"
  default     = 1
}
