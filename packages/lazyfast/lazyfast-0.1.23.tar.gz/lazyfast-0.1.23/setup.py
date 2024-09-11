# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lazyfast']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.8.1,<4.0.0',
 'fastapi>=0.111.0,<0.112.0',
 'python-multipart>=0.0.9,<0.0.10']

setup_kwargs = {
    'name': 'lazyfast',
    'version': '0.1.23',
    'description': 'LazyFast = FastAPI + HTMX + Component-based approach + State management',
    'long_description': '# LazyFast\n\nLazyFast is a lightweight Python library designed for building modern web interfaces using a component-based approach. It enables writing page logic on the server side in Python, integrating seamlessly with FastAPI. With LazyFast, interactive elements like inputs, buttons, and selects trigger component reloads that occur on the server, updating the component\'s state dynamically.\n\n## Key Features\n\n1. **Component-Based Server Rendering**: Build web interfaces using lazy loaded components that encapsulate logic, state, and presentation. \n2. **Server-Side Logic**: Handle interactions and state management on the server, reducing client-side complexity.\n3. **FastAPI Integration**: Each component or page is a FastAPI endpoint, allowing for dependency injection and other FastAPI features.\n4. **Lightweight**: The only dependencies are FastAPI for Python and HTMX for JavaScript, which can be included via CDN.\n5. **State Management**: Utilize a state manager that can trigger component reloads, ensuring a reactive user experience.\n\n## Installation\n\nTo install LazyFast, use pip:\n\n```bash\npip install lazyfast\n```\nor\n```bash\npoetry add lazyfast\n```\n\n## Quick Start\n\nHere\'s an example application to demonstrate how LazyFast works:\n\n```python\nfrom fastapi import FastAPI, Request\nfrom lazyfast import LazyFastRouter, Component, tags\n\n\n# LazyFastRouter inherits from FastAPI\'s APIRouter\nrouter = LazyFastRouter()\n\n# Define a lazy-loaded HTML component powered by HTMX\n@router.component()\nclass MyComponent(Component):\n    title: str\n\n    async def view(self, request: Request) -> None:\n        tags.h1(self.title, class_="my-class")\n\n        with tags.div(style="border: 1px solid black"):\n            tags.span(request.headers)\n\n# Initialize the page dependencies for component rendering\n# The page endpoint is also a FastAPI endpoint\n@router.page("/{name}")\ndef root(name: str):\n    with tags.div(class_="container mt-6"):\n        MyComponent(title=f"Hello, World from {name}")\n\n# Embed the router in a FastAPI app\napp = FastAPI()\napp.include_router(router)\n```\nIf you use `uvicorn` instead as a server and want to reload on changes, use the following command:\n```bash\nuvicorn app:app --reload --timeout-graceful-shutdown 1\n```\n\n## Documentation\nDocumentation can be found [here](https://github.com/nikirg/lazyfast/blob/main/DOCS.md).\n\n\n## License\n\nLazyFast is licensed under the [MIT License](https://github.com/nikirg/lazyfast/blob/main/LICENSE).',
    'author': 'Nikita Irgashev',
    'author_email': 'nik.irg@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nikirg/lazyfast',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
