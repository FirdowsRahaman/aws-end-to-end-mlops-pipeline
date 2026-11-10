# EU AI Act Technical Documentation (MLOps Infrastructure)

**Regulation Reference**: Regulation (EU) 2024/1689 (EU AI Act)  
**System**: Production Automated MLOps Infrastructure & Continuous Retraining Pipeline  
**Classification**: High-Risk AI Platform Support System (Article 10 & Article 15)  
**Version**: 1.0.0  
**Data Residency**: European Economic Area (EEA) • `eu-central-1` (Frankfurt, Germany)  

---

## 1. Scope & Objective
This documentation specifies conformity measures for automated training, evaluation, drift monitoring, and continuous deployment pipelines operating under European Union regulatory oversight.

## 2. Article 10: Data Governance & Continuous Quality Management
1. **Automated Drift Detection**: Evidentiary data drift monitoring via SageMaker Model Monitor with automated alerts upon statistical distribution shift (Kolmogorov-Smirnov / PSI > 0.15).
2. **Lineage Tracking**: Every model artifact is registered with immutable S3 digest, training commit SHA, dataset snapshot ID, and evaluation metrics before promotion to production.
3. **Data Provenance**: Datasets reside within encrypted S3 buckets in Frankfurt with public access strictly blocked and TLS 1.2+ forced.

## 3. Article 12: Automated Audit Trails & Reproducibility
1. **Pipeline Reproducibility**: Complete pipeline definition declared via Infrastructure-as-Code (Terraform / CloudFormation) ensuring identical reproducibility across audit instances.
2. **Model Registry**: SageMaker Model Registry maintains immutable metadata for model versions, approval statuses, and evaluator IDs.

## 4. Article 15: Cybersecurity & Operational Robustness
1. **Zero Egress**: VPC Endpoints (AWS PrivateLink) ensure data never traverses the public internet between SageMaker, ECR, and S3.
2. **Cryptographic Protection**: All at-rest data encrypted using AWS KMS Customer Managed Keys (CMK) with automated 365-day rotation.

## 5. European ESG & Green AI Tracking
* Integrated carbon emission tracking measuring energy consumption (kWh) and greenhouse gas footprint (kg CO2e) per training job.
