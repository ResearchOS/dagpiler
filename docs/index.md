# dagpiler

Compile data processing pipelines from independent packages as a DAG.
```bash
pip install dagpiler
```

## Problem Statement
It is challenging to integrate data analyses written by other people or organizations into your own data processing pipelines due to the large variation in data analyses and data. Presently, many organizations custom building their data processing pipelines, spending much of their time managing the uninteresting aspects such as file saving/loading, handling dependencies, etc. wasting lots of time re-creating infrastructure that already exists elsewhere.

While there are established workflow orchestration tools such as Apache Airflow, they do not focus on being able to share and use data processing pipelines written by others. There is a need for a lightweight, standardized way to define data processing pipelines that can be shared and used by others.

## Solution
The `dagpiler` package solves the problem of reusing and sharing data analysis pipelines by providing a flexible standard to develop shareable data processing pipelines. In the same way that modern software development reuses and shares software by building on existing libraries, `dagpiler` aims to build data processing pipelines by building on prior pipelines, shared as packages. These packages use [TOML files](https://toml.io/en/v1.0.0) and Python's native packaging system to define and publicly share data processing pipelines. These packages can then be installed using `pip install` and incorporated by others in their own data processing pipelines via a "[bridging](Packaging/bridging_packages.md)" mechanism. The compilation process converts TOML files into a Directed Acyclic Graph (DAG) that is intended to provide all of the requisite metadata for running the data processing pipeline.

## Future Toolkit
`dagpiler` is part of a larger suite of tools that will be developed to support the entire data processing pipeline lifecycle, from dataset creation to data analysis, visualization, and reporting. The goal is to make it easy to share and use data processing pipelines, and to make it easy to integrate data analyses from multiple sources into a single pipeline.

