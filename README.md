# DLL Catalog Hybrid Model

This is a git repo for a hybrid approach to processing metadata records for editions of Latin works to be added to the [DLL Catalog](https://catalog.digitallatin.org/).

Specifically, this hybrid approach combines deterministic matching, fuzzy matching, and deep learning approaches to processing incoming bibliographical metadata. The file `python/hybrid.ipynb` implements these approaches.

## Structure

### data

The `data` directory contains several CSV files used in the Jupyter Notebooks in the `python` directory.

The most important files in `data` are:

- `authors_db.csv`: Used for mapping variant names to authorized names and DLL IDs.
- `deduped-greek_and_latin.csv`: Used for training the Greek-Latin classifier model. It was renamed to `greek_latin_authors.csv` for storage as a [dataset on HuggingFace Hub](https://huggingface.co/datasets/sjhuskey/greek_latin_authors).
- `distilbert_data.csv`: Used for training the author classification model. It was renamed to `latin_author_dll_id.csv` for storage as a [dataset on HuggingFace Hub](https://huggingface.co/datasets/sjhuskey/latin_author_dll_id)
- `1908698974-1722799169.txt`: The original file downloaded from HathiTrust.
- `works_db.csv`: Used for mapping works to their authors.

### output

The `output` directory contains files generated during analysis.

### python

This directory contains the Jupyter notebooks and Python files used in working with and analyzing the data.

The file `python/fine_tune_distilmbert.ipynb` was used to fine-tune the [DistilBERT Multilingual Cased](https://huggingface.co/distilbert/distilbert-base-multilingual-cased) model to create a model for matching the names of authors of Latin texts with their Digital Latin Library ID: [sjhuskey/distilbert_multilingual_cased_latin_author_identifier](<https://huggingface.co/sjhuskey/distilbert_multilingual_cased_latin_author_identifier>).

The file `python/fine_tune_distilmbert_greek.ipynb` was used to fine-tune the [DistilBERT Multilingual Cased](https://huggingface.co/distilbert/distilbert-base-multilingual-cased) model to create a model for labeling names of authors as "Greek" or "Latin", according to the language in which they primarily wrote: [sjhuskey/distilbert_multilingual_cased_greek_latin_classifier](<https://huggingface.co/sjhuskey/distilbert_multilingual_cased_greek_latin_classifier>).

### vector_stores

Since there are many author names to keep track of, I'm going to save them in a vector store for easier and more rapid searching instead of keeping them in memory.

I've used [FAISS (Facebook AI Similarity Search)](https://faiss.ai/) because it is reliable, open-source, and relatively easy to use. In previous versions of this experiment, I tried using [Chroma](https://www.trychroma.com/) and found that it was too buggy to use.

The vector stores and their mapping files are in the directory `vector_stores`. The file for creating them is `python/vector_stores`.

### Directory Tree

```bash
dll-hybrid
|_vector_stores
  |_author_map.pkl
  |_title_index.faiss
  |_author_index.faiss
  |_title_map.pkl
|_requirements.txt
|_python
  |_vector_stores.ipynb
  |_prepare-data-for-fine-tuning.ipynb
  |___pycache__
    |_utilities.cpython-310.pyc
  |_fine_tune_distilmbert.ipynb
  |_emissions.csv
  |_data-preparation.ipynb
  |_sam_dropbox.py
  |_analysis-2.ipynb
  |_hybrid.ipynb
  |_prepare_hathi.ipynb
  |_fine_tune_distilmbert_greek.ipynb
  |_emissions.ipynb
  |_utilities.py
  |_greek-data-prep.ipynb
  |_analysis.ipynb
|_output
  |_grouped_distilbert_author_matches.csv
  |_grouped_distilbert_author_matches_90_100.csv
  |_unmatched_authors_fuzzy.txt
  |_unique_authors_fuzzy_scores.csv
  |_unique_authors_fuzzy_scores_2.csv
  |_unique_authors_fuzzy_scores_3.csv
  |_unique_authors_with_stdev.csv
  |_fuzzy-distilbert-comparison-bar-graph.png
|_README.md
|_data
  |_works_db.csv
  |_output_df.csv
  |_classified_metadata.csv
  |_unknown_title_known_author_classified_metadata.csv
  |_authors.csv
  |_1908698974-1722799169.txt
  |_unknown_title_known_author_greek_authors.csv
  |_deterministic_author.csv
  |_unknown_title_known_author_latin_authors.csv
  |_unknown_title_known_authors.csv
  |_deterministic_author_2.csv
  |_titles.csv
  |_distilbert-data.csv
  |_authors_db.csv
  |_processed_unknowns_matches.csv
  |_greek_cleanup
    |_sorted_variants.csv
    |_deduped_greek_with_authorized_and_variants.csv
    |_sorted_df_by_variants.csv
    |_sorted_df_by_url.csv
    |_greek-authors.csv
    |_greek.csv
    |_exploded_variants.csv
    |_sorted_df_by_name.csv
    |_viaf_greek_variants.csv
  |_works.csv
  |_latin_authors.csv
  |_greek_authors.csv
  |_deduped_greek_and_latin.csv
  |_hathi.csv
  |_hathi2.csv
  |_unknown_title_known_author_output.csv
```