## az_storage_tools

This package is developed for simplifying various Azure Storage operations. 

### Getting Started
Make sure to include azure storage connection string or url and key as `env` variables. Namely
```
AZ_STORAGE_ACCOUNT_NAME
AZ_STORAGE_KEY
```
or
```
AZ_CONNECTION_URL
```
#### Container Name
If `AZStorageTools` is not initialized with a container name, then following `env` variable must be set:
```
AZ_STORAGE_CONTAINER_NAME
```
