# ARTS (Assessing Readability & Text Simplicity)

Welcome to **ARTS** — a project that focuses on assessing text readability and simplicity using various models and statistical techniques.

This repository contains scripts and notebooks aimed to analyze text simplicity, generate annotations, develop simplicity regression models, and run simulations—all while ensuring ease of understanding.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Folder and File Structure](#folder-and-file-structure)
- [Setup Instructions](#setup-instructions)
  - [Docker Setup](#docker-setup)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

This work alleviates the problem of Assessing Readability & Text Simplicity. We present ARTS, a method for language-independent construction of datasets for simplicity assessment.
We propose using pairwise comparisons of texts in conjunction with an Elo algorithm to produce a simplicity ranking and simplicity scores. 
Additionally, we provide a high-quality human-labeled and three GPT-labeled simplicity datasets.
Our results show a high correlation between human and LLM-based labels, allowing for an effective and cost-efficient way to construct large synthetic datasets.

---

## Features

- **Text Simplicity Scoring**: Tools to leverage models, including regression techniques, for predicting the simplicity of text segments.
- **GPT Annotation**: Automated annotation using GPT for ranking and scoring simplicity across different text samples.
- **Statistical Analysis**: Scripts and notebooks for performing in-depth statistics on the textual data.
- **Simulation**: Simulate various readability scenarios to test effectiveness.

---

## Folder and File Structure

Here's an overview of the most important files and folders in this repository:

### `/workspace`
Contains all the core resources:

- **`data/`**: Placeholder folder where you place your input datasets.
- **`Histories/`**: Records of past model performance histories.
- **`pages/`**: Various notebook segments or pages with content to analyze and review.
- **`Scores/`**: Folder to store score outputs from the assessment scripts.
- **`5.5_Simplicity Regression Model.ipynb`**: Notebook containing the regression model that predicts simplicity.
- **`A.7_Statistics.ipynb`**: Notebook to perform statistical analysis.
- **`data_preparation.ipynb`**: Notebook to prepare the raw text data for further analysis.
- **`gpt_annotation.ipynb`**: Notebook to generate annotations using GPT.
- **`gpt_annotation_rank_all.ipynb`**: Notebook to generate annotations using GPT based on ranked texts.
- **`gpt_annotation_score_individual.ipynb`**: Notebook for scoring individual text segments using GPT.
- **`rating_interface.py`**: Streamlit application to run the labeling interface for humans.
- **`simulation.ipynb`**: Notebook for running oracle and user simulations.
- **`utils.py`**: Utility functions for the project.

### Root Directory Files

- **`docker-compose.yml`**: Docker Compose configuration.
- **`Dockerfile`**: Defines the Docker image used in this project.
- **`LICENSE`**: License information.
- **`requirements.txt`**: List of Python dependencies required by the project.
- **`README.md`**: This readme file.

---

## Setup Instructions

To run this project, we highly recommend using Docker. Docker simplifies environment setup and ensures consistency across different machines.

### Docker Setup

1. **Install Docker**:
   - Follow the installation guide available at [Docker's official documentation](https://docs.docker.com/get-docker/).
   
2. **Build the ARTS Docker Image**:
   - Navigate to the root of the project directory (where the `Dockerfile` is located).
   - Run the following command to build the Docker image:

     ```bash
     docker build -t arts .
     ```

3. **Run the Container**:
   - After successfully building the image, spin up a container using:

     ```bash
     docker compose up
     ```

   - This command mounts the current directory into the Docker container and opens the required ports for Jupyter Notebook/IPython interface interaction.


---

## Contributing

We welcome contributions of all kinds to improve ARTS. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request.

Please make sure your contribution adheres to defined coding convention and includes necessary tests.

---

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

That's it! 👩‍💻👨‍💻 Happy Scoring with ARTS!
