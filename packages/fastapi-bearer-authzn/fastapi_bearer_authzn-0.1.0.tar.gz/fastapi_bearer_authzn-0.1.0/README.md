# FastAPI Bearer Authorization

A robust bearer token authentication and authorization middleware for FastAPI applications.

> [!WARNING]  
> This project is in early development and may not be suitable for production use.

## Features

- Easy-to-use bearer token authentication
- Fine-grained permission-based authorization using unique operation IDs
- Configurable via environment variables or direct configuration
- Secure token generation and validation

## Installation

```bash
pip install fastapi-bearer-authzn
```

## Quick Start

```python
from fastapi import FastAPI, Depends
from fastapi_bearer_authzn import BearerAuthDependency, bootstrap_config, ConfigModel

# Generate a sample configuration with tokens
config_dict, tokens = bootstrap_config(no_identities=3)
config = ConfigModel.model_validate(config_dict)

# Initialize the auth dependency
auth = BearerAuthDependency(config=config)

app = FastAPI()

@app.get("/protected")
def protected_route(user_id: str = Depends(auth)):
    return {"message": "Access granted", "user_id": user_id}
```

## Configuration Structure

The configuration is structured as follows:

```python
from fastapi_bearer_authzn import ConfigModel, PermissionConfig

config_dict = {
    "user_id_1": PermissionConfig(
        hashed_token="...",
        user_identifier="user1@example.com",
        permissions=["operation_id_1", "operation_id_2"]
    ),
    "user_id_2": PermissionConfig(
        hashed_token="...",
        user_identifier="user2@example.com",
        permissions=["*"]  # Wildcard for all permissions
    )
}
config = ConfigModel.model_validate(config_dict)
```

You can use the `bootstrap_config(no_identities=n)` function to generate a sample configuration with `n` number of identities. This function returns both the configuration dictionary and a dictionary of tokens:

```python
config_dict, tokens = bootstrap_config(no_identities=3)
```

The `tokens` dictionary contains the raw tokens for each user, which you can distribute to your users securely.

## Configuration Methods

You can configure the module in two ways:

1. Direct configuration:

```python
auth = BearerAuthDependency(config=config)
```

2. Environment variable:

```python
# Set the FASTAPI_BEARER_AUTHZN_CONFIG environment variable with a JSON string
auth = BearerAuthDependency(from_env=True)
```

## Usage

1. Initialize the `BearerAuthDependency` with your configuration.
2. Use the dependency in your FastAPI route decorators.
3. The middleware will handle authentication and authorization based on the operation IDs.

## Operation ID-based Authorization

This module uses FastAPI's operation IDs for fine-grained authorization. By default, FastAPI generates an operation ID for each route, which can be inspected in the OpenAPI JSON schema. You can also override these with custom operation IDs:

```python
@app.get("/resource1")
def get_resource_1(user_id: str = Depends(auth)):
    # Uses FastAPI's default operation ID
    return {"message": "Access to resource 1 granted"}

@app.post("/resource2", operation_id="create_resource_2")
def create_resource_2(user_id: str = Depends(auth)):
    # Uses custom operation ID
    return {"message": "Resource 2 created"}
```

In your configuration, you can specify which operation IDs a user has permission to access:

```python
config_dict = {
    "user_id": PermissionConfig(
        hashed_token="...",
        user_identifier="user@example.com",
        permissions=["get_resource_1", "create_resource_2"]
    )
}
```

This allows for precise control over which operations each user can perform. You can inspect the OpenAPI JSON schema to see the operation IDs for each route.

## Testing

Run the tests using `pytest`:

```bash
pytest tests/
```

## License

This project is licensed under the MIT License.