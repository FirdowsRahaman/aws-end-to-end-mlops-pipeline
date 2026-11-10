variable "aws_region" {
  description = "The primary AWS sovereign region within the European Economic Area (EEA)."
  type        = string
  default     = "eu-central-1" # Frankfurt, Germany
}

variable "environment" {
  description = "Target environment tier (dev, staging, prod)."
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Project name identifier."
  type        = string
  default     = "eu-sovereign-mlops"
}

variable "enable_kms_cmk" {
  description = "Enforce Customer Managed Keys (CMK) under EU GDPR Article 32."
  type        = bool
  default     = true
}

variable "enforce_eu_data_boundary" {
  description = "Enforce strict IAM and S3 bucket conditions preventing cross-border egress outside EEA."
  type        = bool
  default     = true
}
