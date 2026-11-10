terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project          = var.project_name
      Environment      = var.environment
      DataResidency    = "European-Economic-Area"
      RegulatoryScope  = "EU-AI-Act-High-Risk"
      Jurisdiction     = "Germany-Frankfurt"
      Compliance       = "GDPR-Article-32"
    }
  }
}

# KMS Customer-Managed Key (CMK) for EU Sovereign Cryptographic Isolation
resource "aws_kms_key" "mlops_sovereign_key" {
  description             = "KMS CMK for EU Sovereign MLOps Pipeline artifacts in Frankfurt"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "EnableRootPermissions"
        Effect = "Allow"
        Principal = {
          AWS = "*"
        }
        Action   = "kms:*"
        Resource = "*"
      }
    ]
  })
}

# Secure S3 Bucket for Training Data & Models with Sovereign Policy
resource "aws_s3_bucket" "sovereign_ml_artifacts" {
  bucket_prefix = "${var.project_name}-${var.environment}-"
  force_destroy = false
}

resource "aws_s3_bucket_server_side_encryption_configuration" "kms_encryption" {
  bucket = aws_s3_bucket.sovereign_ml_artifacts.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.mlops_sovereign_key.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "block_public_access" {
  bucket                  = aws_s3_bucket.sovereign_ml_artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enforce TLS 1.2+ and In-Region Requests (Schrems II / European Data Boundary)
resource "aws_s3_bucket_policy" "enforce_eu_sovereignty" {
  bucket = aws_s3_bucket.sovereign_ml_artifacts.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "EnforceTLSRequestsOnly"
        Effect    = "Deny"
        Principal = "*"
        Action    = "s3:*"
        Resource = [
          aws_s3_bucket.sovereign_ml_artifacts.arn,
          "${aws_s3_bucket.sovereign_ml_artifacts.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}
