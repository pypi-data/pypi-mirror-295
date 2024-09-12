# mkdoc-qcm

[![CI](https://github.com/bdallard/mkdoc-qcm/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/bdallard/mkdoc-qcm/actions/workflows/ci.yml)

This guide will help you set up and use the Quiz Plugin with a custom JSON file in your MkDocs project. Follow these steps to integrate and configure the plugin with your custom quizzes.

> First, ensure you have MkDocs installed. If you don't have it installed go check it [here](https://github.com/mkdocs/mkdocs)


## Create your project 

If you don't already have a MkDocs project, create one:
```bash
mkdocs new my-project
cd my-project
```

Ensure your project directory looks like this:
```
my_project/
├── docs/
│   ├── javascripts
│   ├   └── extra.js
│   └── stylesheets
│   ├   └── extra.css
│   ├── static/
│   │   └── audios/img/videos
├── mkdocs.yml
└── quizzes.json
```

### Add a JSON QCM file 

Ensure the JSON file includes hints (indice) for each option:
```json
{
    "quizzes": {
        "quiz1": {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "What is the capital of France?",
                        "fr": "Quelle est la capitale de la France?"
                    },
                    "media": {
                        "type": "image",
                        "src": "./static/images/test.png",
                        "alt": {
                            "en": "Paris",
                            "fr": "Paris"
                        }
                    },
                    "options": [
                        {
                            "text": {
                                "en": "Berlin",
                                "fr": "Berlin"
                            },
                            "correct": false,
                            "indice": {
                                "en": "This is the capital of Germany.",
                                "fr": "Ceci est la capitale de l'Allemagne."
                            }
                        },
                        {
                            "text": {
                                "en": "Madrid",
                                "fr": "Madrid"
                            },
                            "correct": false,
                            "indice": {
                                "en": "This is the capital of Spain.",
                                "fr": "Ceci est la capitale de l'Espagne."
                            }
                        },
                        {
                            "text": {
                                "en": "Paris",
                                "fr": "Paris"
                            },
                            "correct": true,
                            "indice": {
                                "en": "Paris is the city of light",
                                "fr": ""
                            }
                        },
                        {
                            "text": {
                                "en": "Rome",
                                "fr": "Rome"
                            },
                            "correct": false,
                            "indice": {
                                "en": "This is the capital of Italy.",
                                "fr": "Ceci est la capitale de l'Italie."
                            }
                        }
                    ]
                },
                {
                    "type": "true-false",
                    "question": {
                        "en": "The Earth is flat.",
                        "fr": "La Terre est plate."
                    },
                    "media": {
                        "type": "video",
                        "src": "./static/videos/test.mp4",
                        "alt": {
                            "en": "Earth",
                            "fr": "Terre"
                        }
                    },
                    "options": [
                        {
                            "text": {
                                "en": "True",
                                "fr": "Vrai"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The Earth is round.",
                                "fr": "La Terre est ronde."
                            }
                        },
                        {
                            "text": {
                                "en": "False",
                                "fr": "Faux"
                            },
                            "correct": true,
                            "indice": {
                                "en": "",
                                "fr": ""
                            }
                        }
                    ]
                },
                {
                    "type": "fill-in-the-blank",
                    "question": {
                        "en": "____ is the largest planet in our solar system.",
                        "fr": "____ est la plus grande planète de notre système solaire."
                    },
                    "media": {
                        "type": "audio",
                        "src": "./static/audios/test.mp3",
                        "alt": {
                            "en": "Largest planet",
                            "fr": "Plus grande planète"
                        }
                    },
                    "answer": {
                        "en": "Jupiter",
                        "fr": "Jupiter"
                    },
                    "indice": {
                        "en": "It is a gas giant.",
                        "fr": "C'est une géante gazeuse."
                    }
                },
                {
                    "type": "multi-choice",
                    "question": {
                        "en": "Select the primary colors:",
                        "fr": "Sélectionnez les couleurs primaires :"
                    },
                    "options": [
                        {
                            "text": {
                                "en": "Red",
                                "fr": "Rouge"
                            },
                            "correct": true,
                            "indice": {
                                "en": "Red is a primary color.",
                                "fr": "Rouge est une couleur primaire."
                            }
                        },
                        {
                            "text": {
                                "en": "Blue",
                                "fr": "Bleu"
                            },
                            "correct": true,
                            "indice": {
                                "en": "Blue is a primary color.",
                                "fr": "Bleu est une couleur primaire."
                            }
                        },
                        {
                            "text": {
                                "en": "Green",
                                "fr": "Vert"
                            },
                            "correct": false,
                            "indice": {
                                "en": "Green is a secondary color.",
                                "fr": "Vert est une couleur secondaire."
                            }
                        },
                        {
                            "text": {
                                "en": "Yellow",
                                "fr": "Jaune"
                            },
                            "correct": true,
                            "indice": {
                                "en": "Yellow is a primary color.",
                                "fr": "Jaune est une couleur primaire."
                            }
                        }
                    ]
                }
            ]
        },
        "quiz2": {
            "questions": [
                {
                    "type": "multiple-choice",
                    "question": {
                        "en": "Which element has the chemical symbol 'O'?",
                        "fr": "Quel élément a le symbole chimique 'O'?"
                    },
                    "media": {
                        "type": "image",
                        "src": "./static/images/test.jpg",
                        "alt": {
                            "en": "Oxygen",
                            "fr": "Oxygène"
                        }
                    },
                    "options": [
                        {
                            "text": {
                                "en": "Oxygen",
                                "fr": "Oxygène"
                            },
                            "correct": true,
                            "indice": {
                                "en": "",
                                "fr": ""
                            }
                        },
                        {
                            "text": {
                                "en": "Gold",
                                "fr": "Or"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The symbol for gold is 'Au'.",
                                "fr": "Le symbole de l'or est 'Au'."
                            }
                        },
                        {
                            "text": {
                                "en": "Osmium",
                                "fr": "Osmium"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The symbol for osmium is 'Os'.",
                                "fr": "Le symbole de l'osmium est 'Os'."
                            }
                        },
                        {
                            "text": {
                                "en": "Hydrogen",
                                "fr": "Hydrogène"
                            },
                            "correct": false,
                            "indice": {
                                "en": "The symbol for hydrogen is 'H'.",
                                "fr": "Le symbole de l'hydrogène est 'H'."
                            }
                        }
                    ]
                },
                {
                    "type": "true-false",
                    "question": {
                        "en": "Water boils at 100°C.",
                        "fr": "L'eau bout à 100°C."
                    },
                    "options": [
                        {
                            "text": {
                                "en": "True",
                                "fr": "Vrai"
                            },
                            "correct": true,
                            "indice": {
                                "en": "",
                                "fr": ""
                            }
                        },
                        {
                            "text": {
                                "en": "False",
                                "fr": "Faux"
                            },
                            "correct": false,
                            "indice": {
                                "en": "At sea level, water boils at 100°C.",
                                "fr": "Au niveau de la mer, l'eau bout à 100°C."
                            }
                        }
                    ]
                },
                {
                    "type": "fill-in-the-blank",
                    "question": {
                        "en": "The chemical formula for water is ___.",
                        "fr": "La formule chimique de l'eau est ___."
                    },
                    "answer": {
                        "en": "H2O",
                        "fr": "H2O"
                    },
                    "indice": {
                        "en": "It consists of two hydrogen atoms and one oxygen atom.",
                        "fr": "Elle se compose de deux atomes d'hydrogène et d'un atome d'oxygène."
                    }
                }
            ]
        }
    }
}
```


### Update your `mkdocs.yml`

Ensure the CSS and JavaScript files are referenced in your `mkdocs.yml`:

```yaml
site_name: My Docs

plugins:
  - search
  - my_quiz_plugin:
      quiz_file: quizzes.json
      language: en
      show_refresh_button: true
      show_indice_on_answer: true
      show_score: true
      show_progress_bar: true
      logging: true

extra_css:
  - stylesheets/extra.css
  - https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css


extra_javascript:
  - javascripts/extra.js
```

### Use the plugin in your code

Run MkDocs to test the updated plugin:
```bash
mkdocs serve
```

Example Markdown with Quizzes
Here’s how you can reference quizzes in your markdown files:

Example `docs/index.md`

```
# Page 1

This is a quiz about geography.

<!-- QUIZ_ID: quiz1 -->

# Page 2

This is a quiz about space.

<!-- QUIZ_ID: quiz2 -->

```


--- 

## Testing

This test suite is designed to ensure the correctness and robustness of the MkDocs Quiz Plugin, covering multiple aspects such as HTML generation, quiz logic, UI components, and configuration options. The suite includes unit tests, integration tests, and end-to-end tests, providing comprehensive coverage for both core functionality and optional features.

- **Tools used**: 
  - **unittest** for writing tests
  - **BeautifulSoup** for parsing and asserting HTML
  - **mock** for simulating quiz data

The test suite is organized into four main files:
1. **`test_html_generation.py`** – Tests for generating quiz HTML
2. **`test_logic.py`** – Tests for quiz logic and functionality
3. **`test_ui_components.py`** – Tests for optional UI elements
4. **`test_mock.py`** – End-to-end testing and mock data integration

To run the tests just use `tox` command, you should see this kind of output 🚀

```
============================================================ test session starts =============================================================
platform darwin -- Python 3.7.0, pytest-7.4.4, pluggy-1.2.0
rootdir: /Users/mac/workspace/mkdoc-plugin/PROD/mkdoc-qcm
plugins: dash-2.8.1, anyio-3.7.1, requests-mock-1.7.0
collected 34 items                                                                                                                           

test_html_generation.py ..........                                                                                                     [ 29%]
test_logic.py ...........                                                                                                              [ 61%]
test_mock.py .....                                                                                                                     [ 76%]
test_ui_components.py ........                                                                                                         [100%]

============================================================= 34 passed in 0.67s =============================================================
```

---

### General Guidelines for Writing Tests**

#### **Test Naming**
- **Prefix tests based on functionality**:
  - **HTML Tests**: Use `test_generate_` as a prefix for tests that check HTML rendering.
  - **Logic Tests**: Use `test_logic_` for testing the underlying quiz logic (e.g., scoring, question types).
  - **UI Tests**: Use `test_ui_` for testing UI elements and optional components.
  - **End-to-End Tests**: Use `test_end_to_end_` for comprehensive tests involving multiple components.

#### **Code Coverage**
- Each test should focus on a single feature or behavior.
- Aim for **high coverage** of the quiz plugin's functionality, including edge cases (e.g., no quiz data, unsupported media types).
- Maintain **separation of concerns**: 
  - UI component tests should focus solely on visual elements.
  - Logic tests should focus solely on the correctness of computations.

#### **Mocking and Data Setup**
- Use **mock data** where applicable to simulate quiz data, ensuring your tests remain independent of external data sources.
- `mock_quiz_data.py` provides reusable mock quiz structures, and you can extend this file to accommodate additional features as the plugin evolves.

#### **Test Configuration**:
- Test functions often depend on a configuration loaded by `self.load_plugin_config`. Ensure all configurations are explicitly defined when writing new tests.
- **Key Configurations**:
  - **`show_indice_on_answer`**: Enables or disables the display of hints (indices).
  - **`show_score`**: Enables or disables score tracking.
  - **`show_progress_bar`**: Toggles the progress bar in the quiz.
  - **`show_refresh_button`**: Toggles the display of the refresh button in the UI.
  
#### **Assertions**
- Use **assertions** to verify some expected behavior:
  - **HTML Rendering**: Use `assertIsNotNone`, `assertIn`, and `assertEqual` to validate the structure and presence of HTML elements.
  - **Logic and Scoring**: Use `assertEqual` to compare expected and actual scores or results.
  
#### **Fixture Setup**
- Ensure that all test classes inherit from `BaseTestCase`, which handles the initialization of the plugin object and configuration.
- Use `super().setUp()` in any custom test classes to ensure the base setup is correctly executed.

---


## Push to PyPi


### TODO: 
- [ ] rename pluging 
- [ ] write doc on how to push to pipy simple basic

Sure! Here are the steps to push your Python package to PyPI:

### 1. Update `setup.py` with necessary metadata

Make sure your `setup.py` contains all the necessary metadata for PyPI:

```python
from setuptools import setup, find_packages

setup(
    name='my_quiz_plugin',
    version='0.1',
    description='A MkDocs plugin to create quizzes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/my_quiz_plugin',
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1.0.4',
    ],
    entry_points={
        'mkdocs.plugins': [
            'my_quiz_plugin = my_quiz_plugin.plugin:QuizPlugin'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
```

### 2. Create a `.pypirc` file (optional but recommended)

A `.pypirc` file stores your PyPI credentials, making the upload process easier. Create this file in your home directory (`~/.pypirc`):

```ini
[distutils]
index-servers =
  pypi

[pypi]
username = yourusername
password = yourpassword
```

### 3. Build your package

Use `setuptools` and `wheel` to build your package:

```bash
python setup.py sdist bdist_wheel
```

### 4. Upload your package to PyPI

Use `twine` to securely upload your package:

```bash
pip install twine
twine upload dist/*
```

If you didn't create a `.pypirc` file, you'll need to provide your username and password during the upload process.

### 5. Automate with GitHub Actions

You can also automate this process using GitHub Actions. Here is an example workflow file (`release.yml`) to automate the release on tag creation:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  build-and-publish:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.7

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install setuptools wheel twine

    - name: Build package
      run: |
        python setup.py sdist bdist_wheel

    - name: Publish package
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        twine upload dist/*
```

### 6. Add PyPI credentials to GitHub Secrets

1. Go to your GitHub repository.
2. Navigate to `Settings` > `Secrets` > `New repository secret`.
3. Add `PYPI_USERNAME` with your PyPI username.
4. Add `PYPI_PASSWORD` with your PyPI password.

### Summary

By following these steps, you will be able to push your Python package to PyPI and automate the process using GitHub Actions. This ensures that your package is uploaded to PyPI whenever you create a new tag in your repository.