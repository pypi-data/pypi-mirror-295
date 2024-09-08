# ClusterArena

ClusterArena is a Python library that provides easy access to the Cluster Arena API. It allows you to manage jobs, add new jobs, and fetch job details seamlessly.

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Initializing ClusterArena](#initializing-clusterarena)
  - [Fetching Jobs](#fetching-jobs)
  - [Adding a Job](#adding-a-job)
  - [Fetching Job Details](#fetching-job-details)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the ClusterArena package, run the following command:

```sh
pip install cluster_arena
```

## Configuration

Before using the ClusterArena library, you need to set up your API key. You can do this by setting the `CLUSTER_ARENA_API_KEY` environment variable or passing the API key directly when initializing the library.

## Usage

### Initializing ClusterArena

To use ClusterArena, first import the library and create an instance of the `ClusterArena` class:

```python
from cluster_arena import ClusterArena

cluster_arena = ClusterArena('your-api-key-here')
```

Alternatively, you can set the `CLUSTER_ARENA_API_KEY` environment variable and initialize without passing the API key:

```python
from cluster_arena import ClusterArena

cluster_arena = ClusterArena()
```

### Fetching Jobs

To fetch all jobs, use the `get_jobs` method:

```python
def fetch_jobs():
    try:
        jobs = cluster_arena.get_jobs()
        print('Jobs:', jobs)
    except Exception as error:
        print('Error fetching jobs:', str(error))

fetch_jobs()
```

### Adding a Job

To add a new job, use the `add_job` method. The job data must include a `title` and `description`:

```python
from cluster_arena import JobData

def add_new_job():
    job_data = JobData(
        title='New Job Title',
        description='Description of the new job',
        # Add more fields as needed
    )
    try:
        new_job = cluster_arena.add_job(job_data)
        print('New Job Added:', new_job)
    except Exception as error:
        print('Error adding job:', str(error))

add_new_job()
```

### Fetching Job Details

To fetch details of a specific job, use the `get_job_details` method and pass the job ID:

```python
def fetch_job_details(job_id: str):
    try:
        job_details = cluster_arena.get_job_details(job_id)
        print('Job Details:', job_details)
    except Exception as error:
        print('Error fetching job details:', str(error))

fetch_job_details('job-id-here')
```

## Error Handling

The ClusterArena library raises exceptions when API requests fail or when invalid data is provided. Make sure to handle these exceptions appropriately in your application:

```python
try:
    # Your code here
except Exception as error:
    print('An error occurred:', str(error))
```

## Contributing

We welcome contributions to the ClusterArena library! If you have suggestions, bug reports, or want to contribute code, please open an issue or submit a pull request on our [GitHub repository](https://github.com/your-repo/cluster_arena).

### Steps to Contribute

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with a descriptive message.
4. Push your changes to your fork.
5. Open a pull request on the main repository.

## License

This project is licensed under the MIT License.