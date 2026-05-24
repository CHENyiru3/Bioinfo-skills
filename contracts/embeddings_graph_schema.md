# Embeddings And Graph Schema Policy

Status: draft

Embedding, graph, and representation keys must be explicit so stages can be
composed without assuming one fixed Scanpy default.

## Semantic Keys

- `representation_key`: low-dimensional representation such as `X_pca`.
- `neighbors_key`: neighbor graph metadata key.
- `embedding_key`: embedding such as `X_umap`.
- `cluster_key`: group labels used for marker ranking or annotation.

## Guardrails

- Do not cluster on UMAP unless explicitly approved.
- Do not overwrite existing graph or cluster keys without a new key.
- Record random seeds and graph/embedding parameters.

