__version__ = "0.3.2"
__author__ = "Bhavyahshree Navaneetha Krishnan"

import os
import requests
import tellurium as te
import tempfile
import ollama
from langchain_text_splitters import CharacterTextSplitter


import fetch_github_json
import search_models as search_models
import download_model_file
import convert_sbml_to_antimony
import split_biomodels
import create_vector_db
import generate_response

# Import functions from other modules
from fetch_github_json import fetch_github_json
from search_models import search_models
from download_model_file import download_model_file
from convert_sbml_to_antimony import convert_sbml_to_antimony
from split_biomodels import split_biomodels
from create_vector_db import create_vector_db
from generate_response import generate_response


# Define __all__ to specify which names are publicly accessible
__all__ = ['fetch_github_json', 'search_models', 'download_model_file', 'convert_sbml_to_antimony', 'split_biomodels','create_vector_db', 'generate_response']
