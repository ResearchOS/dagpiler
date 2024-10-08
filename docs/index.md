# Package-DAG-Compiler

Build data processing pipelines from independent packages.

## Problem Statement
It is challenging to share data processing pipelines due to the large variety of data analyses and data. Presently, many organizations custom build their data processing pipelines, making it difficult for others to build on their work, and wasting lots of time duplicating existing infrastructure. 

While there are established workflow orchestration tools such as Apache Airflow, they tend to be overkill for smaller teams or academic settings in which a large-scale "production" environment is not required, and are not focused on sharing and building upon existing pipelines.

## Solution
This package aims to solve the problem of combining independently developed packages by providing a lightweight, standardized way to define data processing pipelines using [TOML files](https://toml.io/en/v1.0.0). It is designed to be flexible and extensible, allowing users to define their own data processing steps and connect them in a Directed Acyclic Graph (DAG) to create a data processing pipeline. 

The Package-DAG-Compiler focuses on compiling a data processing pipeline from independent packages, similar to how software development uses packages published by others to build software. It is the first of a larger suite of tools that will be developed to support the entire data processing pipeline lifecycle, from data collection to analysis to visualization.

