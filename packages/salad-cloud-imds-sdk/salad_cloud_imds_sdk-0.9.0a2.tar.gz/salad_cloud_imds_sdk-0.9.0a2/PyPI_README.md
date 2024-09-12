# SaladCloudImdsSdk Python SDK 0.9.0-alpha.2<a id="saladcloudimdssdk-python-sdk-090-alpha2"></a>

Welcome to the SaladCloudImdsSdk SDK documentation. This guide will help you get started with integrating and using the SaladCloudImdsSdk SDK in your project.

## Versions<a id="versions"></a>

- API version: `0.9.0-alpha.1`
- SDK version: `0.9.0-alpha.2`

## About the API<a id="about-the-api"></a>

The SaladCloud Instance Metadata Service (IMDS). Please refer to the [SaladCloud API Documentation](https://docs.salad.com/api-reference) for more details.

## Table of Contents<a id="table-of-contents"></a>

- [Setup & Configuration](#setup--configuration)
  - [Supported Language Versions](#supported-language-versions)
  - [Installation](#installation)
- [Setting a Custom Timeout](#setting-a-custom-timeout)
- [Sample Usage](#sample-usage)
- [Services](#services)
- [Models](#models)
- [License](#license)

## Setup & Configuration<a id="setup--configuration"></a>

### Supported Language Versions<a id="supported-language-versions"></a>

This SDK is compatible with the following versions: `Python >= 3.7`

### Installation<a id="installation"></a>

To get started with the SDK, we recommend installing using `pip`:

```bash
pip install salad-cloud-imds-sdk
```

## Setting a Custom Timeout<a id="setting-a-custom-timeout"></a>

You can set a custom timeout for the SDK's HTTP requests as follows:

```py
from salad_cloud_imds_sdk import SaladCloudImdsSdk

sdk = SaladCloudImdsSdk(timeout=10000)
```

# Sample Usage<a id="sample-usage"></a>

Below is a comprehensive example demonstrating how to authenticate and call a simple endpoint:

```py
from salad_cloud_imds_sdk import SaladCloudImdsSdk, Environment

sdk = SaladCloudImdsSdk(
    base_url=Environment.DEFAULT.value,
    timeout=10000
)

result = sdk.metadata.get_container_status()

print(result)

```

## Services<a id="services"></a>

The SDK provides various services to interact with the API.

<details> 
<summary>Below is a list of all available services:</summary>

| Name     |
| :------- |
| metadata |

</details>

## Models<a id="models"></a>

The SDK includes several models that represent the data structures used in API requests and responses. These models help in organizing and managing the data efficiently.

<details> 
<summary>Below is a list of all available models:</summary>

| Name                | Description                                              |
| :------------------ | :------------------------------------------------------- |
| ReallocateContainer | Represents a request to reallocate a container.          |
| ContainerStatus     | Represents the health statuses of the running container. |
| ContainerToken      | Represents the identity token of the running container.  |

</details>

## License<a id="license"></a>

This SDK is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more details.
