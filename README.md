[![Build Status](https://travis-ci.com/camptocamp/odoo-cloud-platform.svg?token=Lpp9PcS5on9AGbp76WKB&branch=7.0)](https://travis-ci.com/camptocamp/odoo-cloud-platform)

# Odoo Cloud Addons

Camptocamp odoo addons used on our Cloud Platform.

## Introduction

On the platform we want to achieve having:

* No data stored on the local filesystem so we can move an instance
  between hosts and even have several running front-ends
* Logs sent to ElasticSearch-Kibana structured as JSON for better searching

For the storage, we store all the attachments on an object storage such as S3 or
Swift, and we store the werkzeug sessions on Redis.

## Setup

### Python dependencies

Libraries that must be added in ``requirements.txt``:

```
redis==2.10.5
python-json-logger==0.1.5

# For S3 object storage (Exoscale, AWS)
boto==2.42.0

# For Swift object storage (Openstack, OVH)
python-swiftclient==3.4.0
python-keystoneclient==3.13.0
```

### Odoo Startup

The `--load` option of Odoo must contains the following addons:

* `session_redis`
* `logging_json`

Example:

`--load=web,web_kanban,session_redis,logging_json`

### Server Environment

The addon `cloud_platform` is an addon that we use for 2 things:

* validate that we setup the required environment variables depending on the running environment
* install and configure the cloud addons

For this purpose, we use the `server_environment` with the following envs:

* `prod`
* `integration`
* `test`
* `dev`

The exact naming is important, because the `cloud_platform` addon rely on these keys to know and check the running environment.


### Attachments in the Object Storage

* prod: stored RW in the object storage
 * `AWS_HOST`: depends of the platform
 * `AWS_ACCESS_KEY_ID`: depends of the platform
 * `AWS_SECRET_ACCESS_KEY`: depends of the platform
 * `AWS_BUCKETNAME`: `<project>-odoo-prod`
* integration:
 * `AWS_HOST`: depends of the platform
 * `AWS_ACCESS_KEY_ID`: depends of the platform
 * `AWS_SECRET_ACCESS_KEY`: depends of the platform
 * `AWS_BUCKETNAME`: `<project>-odoo-integration`
* test: attachments are stored in database

Besides, the attachment location should be set to `s3` (this is
automatically done by the `install` methods of the `cloud_platform` module).
 * `ir.config_parameter` `ir_attachment.location`: `s3`


### Attachments in the Object Storage Swift

* prod: stored RW in the object storage
 * `SWIFT_AUTH_URL`: depends of the platform
 * `SWIFT_ACCOUNT`: depends of the platform
 * `SWIFT_PASSWORD`: depends of the platform
 * `SWIFT_WRITE_CONTAINER`: `<project>-odoo-prod`
* integration:
 * `SWIFT_AUTH_URL`: depends of the platform
 * `SWIFT_ACCOUNT`: depends of the platform
 * `SWIFT_PASSWORD`: depends of the platform
 * `SWIFT_WRITE_CONTAINER`: `<project>-odoo-integration`
* test: attachments are stored in database

Besides, the attachment location should be set to `swift` (this is
automatically done by the `install` methods of the `cloud_platform` module).
 * `ir.config_parameter` `ir_attachment.location`: `swift`

### Sessions in Redis

* prod:
 * `ODOO_SESSION_REDIS`: 1
 * `ODOO_SESSION_REDIS_HOST`: depends of the platform
 * `ODOO_SESSION_REDIS_PASSWORD`: depends of the platform
 * `ODOO_SESSION_REDIS_PREFIX`: `<project>-odoo-prod`
* integration:
 * `ODOO_SESSION_REDIS`: 1
 * `ODOO_SESSION_REDIS_HOST`: depends of the platform
 * `ODOO_SESSION_REDIS_PASSWORD`: depends of the platform
 * `ODOO_SESSION_REDIS_PREFIX`: `<project>-odoo-integration`
* test:
 * `ODOO_SESSION_REDIS`: 1
 * `ODOO_SESSION_REDIS_HOST`: depends of the platform
 * `ODOO_SESSION_REDIS_PASSWORD`: depends of the platform
 * `ODOO_SESSION_REDIS_PREFIX`: `<project>-odoo-test`
 * `ODOO_SESSION_REDIS_EXPIRATION`: `86400` (1 day)

### JSON Logging

At least on production and integration, activate:
* `ODOO_LOGGING_JSON`: 1
* Add ``logging_json`` in the ``server_wide_modules`` option in the
  configuration file

### Startup checks

At loading of the database, the addon will check if the environment variables
for Redis and the object storage are set as expected for the loaded
environment. It will refuse to start if anything is badly configured.

The checks can be bypassed with the environment variable
`ODOO_CLOUD_PLATFORM_UNSAFE` set to `1`.
