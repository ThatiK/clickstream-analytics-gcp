# Clickstream Analytics on GCP (CAEC)

A portfolio project to build a production-grade, modular data pipeline for analyzing real-world clickstream data using Spark, Airflow, dbt, and Terraform on Google Cloud Platform (GCP).

## Project Objectives

- Process and sessionize raw web logs from E commerce datasets
- Transform data into analytical models with dbt and BigQuery
- Showcase infrastructure automation and IAM governance via Terraform
- Demonstrate real-world data engineering workflows with orchestration, modeling, and access control

## Business Value

Clickstream analytics provides critical insights into user behavior, session activity, and web traffic trends. This helps product teams:
- Optimize user experience
- Reduce bounce rate
- Personalize content
- Drive data-informed decisions

## Expected Outcomes

- Sessionized Logs: Raw logs transformed into session-level records using PySpark 
- Analytical Models: Staging, intermediate, and mart layers in dbt/BigQuery 
- Orchestrated Pipelines: Airflow DAGs to schedule and monitor transformations 
- Governed Access: Role-based data access managed via IAM & Terraform 
- GitHub CI/CD: CI workflows for infra, DAGs, and dbt models deployment 

## Architecture Overview


User Logs → GCS (Raw) → PySpark (Sessionize) → GCS (Staging) → dbt → BigQuery (Marts) → Dashboard
                                ↓
                           Orchestrated by Airflow
                                ↓
                Deployed via GitHub Actions + Terraform


## Personas & Roles

- Platform Engineer: Infra setup (GCS, BigQuery, IAM, Terraform) 
- Data Engineer: Build Spark pipelines, DAGs, CI/CD 
- Data Analyst: Query and analyze sessionized and modeled data 
- Data Steward: Audit access, validate data quality & governance rules 

## Repo Structure

/terraform         → Infra-as-code for GCP (modularized)
/airflow           → DAGs and configs
/spark             → Sessionization scripts
/dbt               → dbt project and models
/docs              → Architecture, personas, use case notes
.github/workflows  → CI/CD pipelines
README.md          → Top-level overview (this file)


## Future Add-ons

- Sample dashboards in Looker Studio or Metabase
- dbt tests and data contracts
- Monitoring (e.g., GCP Cloud Logging, Airflow UI alerts)