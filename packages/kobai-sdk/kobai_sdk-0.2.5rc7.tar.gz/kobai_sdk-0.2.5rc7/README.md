# Kobai SDK for Python (Alpha)

Alpha: This SDK is not currently supported for production use while we stabilize the interface.

The Kobai SDK for Python includes functionality to accelerate development with Python on the Kobai Semantic Layer. It does not cover all Kobai Studio features, but rather focuses on integrating a Kobai tenant with data science and AI activities on the backend.

## Getting Started

This exercise demonstrates using the Kobai SDK to create a Databricks "Genie" Data Room environment, enabling users to interact with Kobai data in an AI Chat interface.

1. Please install Kobai SDK for Python via `pip install kobai-sdk`, gather some configuration details of the Kobai instance and tenant to connect to, and instantiate `TenantClient`:

```python
from kobai import tenant_client, spark_client, databricks_client

schema = 'main.demo'
uri = 'https://demo.kobai.io'
tenant_id = '1'
tenant_name = 'My Demo Tenant'

k = tenant_client.TenantClient(tenant_name, tenant_id, uri, schema)
```

2. Authenticate with the Kobai instance:

```python
client_id = 'your_Entra_app_id_here'
tenant_id = 'your_Entra_directory_id_here'

k.authenticate(client_id, tenant_id)
```

3. Initialize a Spark client using your current `SparkSession`, and generate semantically-rich SQL views describing this Kobai tenant:

```python
k.spark_init_session(spark)
k.spark_generate_genie_views()
```

4. Initialize a Databricks API client using your Notebook context, and create a Genie Data Rooms environment for this Kobai tenant.

```python
notebook_context = dbutils.notebook.entry_point.getDbutils().notebook().getContext()
sql_warehouse = '8834d98a8agffa76'

k.databricks_init_notebook(notebook_context, sql_warehouse)
k.databricks_build_genie()
```

## Limitations

This version of the SDK is limited to use in certain contexts, as described below:

- Authentication is limited to MS Entra AD.
- Functionality limited to Databricks Notebook environments at this time.