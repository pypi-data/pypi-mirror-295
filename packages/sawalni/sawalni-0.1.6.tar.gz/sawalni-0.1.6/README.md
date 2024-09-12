# Sawalni Python SDK

This is the official Python SDK for the Sawalni API, providing easy access to language-related services such as embedding generation, language identification, and translation. Sawalni API is developed by [Omneity Labs](https://sawalni.com/developers), and provides unique multilingual models and NLP capabilities, including pioneering Moroccan Darija support.

## Installation

Install the package using pip:

```bash
pip install sawalni
```

## Quick Start

To use the Sawalni SDK, you'll need an API key. You can set it as an environment variable or pass it directly to the client:

```py
from sawalni import Sawalni

client = Sawalni(api_key='your_api_key_here') 
# or specify the key via SAWALNI_API_KEY in the environment
```

## Features

The SDK supports both synchronous and asynchronous operations for the following services:

1. Generate Embeddings (languages depend on the model)
2. Identify Language (35 languages supported)
3. Translate Text (13 languages supported)

### Generate Embeddings

```py
embeddings = client.embed("Hello, world!")
```

### Identify Language

```py
language = client.identify("Bonjour le monde")
```

### Translate Text

```py
translation = client.translate("Hello", source="eng_Latn", target="ary_Latn")
```

## Asynchronous Usage

For asynchronous operations, use the SawalniAsync client:

```py
from sawalni import SawalniAsync

async_client = SawalniAsync(api_key='your_api_key_here')
embeddings = await async_client.embed("Hello, world!")
```

## Documentation

For detailed information about available models, parameters, languages and and response formats, please refer to the complete API documentation at https://api.sawalni.com.

## Support

If you encounter any issues or have questions, please contact api@sawalni.com.