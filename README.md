# CICD Tech Sessions July 2022

Example of CICD pipeline for demo purposes during Databricks' Tech Sessions in July 2022.

## Useful commands

While using this project, you need Python 3.X and `pip` or `conda` for package management.

### Installing project requirements

The following installs the Databricks CLI and other requirements to run CICD commands locally.

```bash
pip install -r requirements-cicd.txt
```

### Unit testing

Running tests locally requires the installation of the `app` itself: 

```bash
pip install -e .
```
plus requirements for running spark locally:
```bash
pip install -r requirements-local.txt
```

After that, please use `pytest` for running the tests:
```
pytest tests/unit
```

### CI/CD pipeline settings

In the CI/CD pipeline, please set the following secrets or environment variables. 
Follow the documentation for [GitHub Actions](https://docs.github.com/en/actions/reference) or for 
[Azure DevOps Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch):
- `QA_HOST`
- `QA_TOKEN`

### Testing and releasing via CI pipeline

- To trigger the CI pipeline, simply push your code to the repository. If CI provider is correctly set, 
it shall trigger the general testing pipeline
- To trigger the release pipeline, get the current version from the `app/__init__.py` file and tag 
the current code version:
```
git tag -a v<your-project-version> -m "Release tag for version <your-project-version>"
git push origin --tags
```
