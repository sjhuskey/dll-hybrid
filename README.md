# DLL Catalog Hybrid Model

This is a git repo for a hybrid approach to processing metadata records for editions of Latin works to be added to the [DLL Catalog](https://catalog.digitallatin.org/).

Specifically, this hybrid approach combines deterministic matching, fuzzy matching, and deep learning approaches to processing incoming bibliographical metadata. The file `python/hybrid.ipynb` implements these approaches.

## Disclosure

Much of the code in this repository was written and/or modified by Samuel J. Huskey. The following sources have influenced practically every line:

- François Chollet, _Deep Learning with Python_, Second Edition (Manning, 2021)
- Patrick J. Burns, Getting Started with LatinCy (2024): <https://diyclassics.github.io/latincy-book/>
- Chat GPT 4o: <https://chatgpt.com/>
- Gemini on Colab: <https://gemini.google.com/>
- HuggingFace API and Tutorials: <https://huggingface.co/>
- PyTorch Tutorials: <https://pytorch.org/>

Indeed, this entire project is an example of how AI can accelerate digital scholarship, since most of it emerged from conversations with chatbots, particularly Chat GPT 4o, but also GitHub's Copilot and Google's Gemini.

## Structure of this Repository

### data

The `data` directory contains several CSV files used in the Jupyter Notebooks in the `python` directory.

The most important files in `data` are:

- `authors_db.csv`: Used for mapping variant names to authorized names and DLL IDs.
- `deduped-greek_and_latin.csv`: Used for training the Greek-Latin classifier model. It was renamed to `greek_latin_authors.csv` for storage as a [dataset on HuggingFace Hub](https://huggingface.co/datasets/sjhuskey/greek_latin_authors).
- `distilbert_data.csv`: Used for training the author classification model. It was renamed to `latin_author_dll_id.csv` for storage as a [dataset on HuggingFace Hub](https://huggingface.co/datasets/sjhuskey/latin_author_dll_id)
- `1908698974-1722799169.txt`: The original file downloaded from HathiTrust.
- `works_db.csv`: Used for mapping works to their authors.

The `greek_cleanup` directory contains files used to create the Greek part of the dataset for the Greek-Latin model.

### output

The `output` directory contains files generated during analysis.

### python

This directory contains the Jupyter notebooks and Python files used in working with and analyzing the data.

The file `python/fine_tune_distilmbert_author.ipynb` was used to fine-tune the [DistilBERT Multilingual Cased](https://huggingface.co/distilbert/distilbert-base-multilingual-cased) model to create a model for matching the names of authors of Latin texts with their Digital Latin Library ID: [sjhuskey/distilbert_multilingual_cased_latin_author_identifier](<https://huggingface.co/sjhuskey/distilbert_multilingual_cased_latin_author_identifier>).

The file `python/fine_tune_distilmbert_greek.ipynb` was used to fine-tune the [DistilBERT Multilingual Cased](https://huggingface.co/distilbert/distilbert-base-multilingual-cased) model to create a model for labeling names of authors as "Greek" or "Latin", according to the language in which they primarily wrote: [sjhuskey/distilbert_multilingual_cased_greek_latin_classifier](<https://huggingface.co/sjhuskey/distilbert_multilingual_cased_greek_latin_classifier>).

The file `inference_testing.ipynb` is the most recent and complete file for analyzing the output of `python/hybrid.ipynb`, the main notebook for running the models to match authors and titles. Older analysis files are in the aptly named `old_analyses`.🙂

The `cleaning_exploration` directory contains files used to, well, clean the data and explore it.🧐

### vector_stores

Since there are many author names to keep track of, I'm going to save them in a vector store for easier and more rapid searching instead of keeping them in memory.

I've used [FAISS (Facebook AI Similarity Search)](https://faiss.ai/) because it is reliable, open-source, and relatively easy to use. In previous versions of this experiment, I tried using [Chroma](https://www.trychroma.com/) and found that it was too buggy to use.

The vector stores and their mapping files are in the directory `vector_stores`. The file for creating them is `python/vector_stores`.

### Directory Tree

```bash
|-- LICENSE
|-- README.md
|-- data
|-- output
|-- python
  |-- cleaning_exploration
    |-- greek_cleanup
    |-- input
    |-- output
  |-- data-preparation.ipynb
  |-- dll_rag.ipynb
  |-- fine_tune_distilmbert.ipynb
  |-- fine_tune_distilmbert_greek.ipynb
  |-- greek-data-prep.ipynb
  |-- hybrid.ipynb
  |-- inference-testing.ipynb
  |-- llama_rag.ipynb
  |-- old_analyses
  |-- sam_dropbox.py
  |-- utilities.py
|-- requirements.txt
|-- vector_stores
```
