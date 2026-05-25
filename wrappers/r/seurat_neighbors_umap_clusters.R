#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(Seurat)
  library(jsonlite)
})

args <- commandArgs(trailingOnly = TRUE)

arg_value <- function(name, default = NULL) {
  idx <- which(args == name)
  if (length(idx) == 0 || idx == length(args)) {
    return(default)
  }
  args[[idx + 1]]
}

parse_dims <- function(value) {
  if (grepl(":", value, fixed = TRUE)) {
    parts <- as.integer(strsplit(value, ":", fixed = TRUE)[[1]])
    return(seq(parts[[1]], parts[[2]]))
  }
  as.integer(strsplit(value, ",", fixed = TRUE)[[1]])
}

input_rds <- arg_value("--input-rds")
output_rds <- arg_value("--output-rds")
report_json <- arg_value("--report-json")
reduction <- arg_value("--reduction", "pca")
dims <- parse_dims(arg_value("--dims", "1:30"))
graph_name <- arg_value("--graph-name", "RNA_snn")
cluster_key <- arg_value("--cluster-key", "seurat_clusters")
umap_key <- arg_value("--umap-key", "umap")
resolution <- as.numeric(arg_value("--resolution", "0.8"))
seed <- as.integer(arg_value("--seed", "0"))

if (is.null(input_rds) || is.null(output_rds) || is.null(report_json)) {
  stop("required args: --input-rds, --output-rds, --report-json", call. = FALSE)
}

set.seed(seed)
object <- readRDS(input_rds)
if (!inherits(object, "Seurat")) {
  stop("input object is not a Seurat object", call. = FALSE)
}
if (!(reduction %in% Reductions(object))) {
  stop(sprintf("reduction not found: %s", reduction), call. = FALSE)
}
if (cluster_key %in% colnames(object[[]])) {
  stop(sprintf("cluster key already exists: %s", cluster_key), call. = FALSE)
}

object <- FindNeighbors(object, reduction = reduction, dims = dims, graph.name = graph_name, verbose = FALSE)
object <- RunUMAP(object, reduction = reduction, dims = dims, reduction.name = umap_key, seed.use = seed, verbose = FALSE)
object <- FindClusters(object, graph.name = graph_name, resolution = resolution, cluster.name = cluster_key, random.seed = seed, verbose = FALSE)

dir.create(dirname(output_rds), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(report_json), recursive = TRUE, showWarnings = FALSE)
saveRDS(object, output_rds)

clusters <- object[[cluster_key, drop = TRUE]]
report <- list(
  schema_version = "0.1.0",
  input_path = normalizePath(input_rds, mustWork = FALSE),
  output_path = normalizePath(output_rds, mustWork = FALSE),
  package_versions = list(
    R = as.character(getRversion()),
    Seurat = as.character(packageVersion("Seurat"))
  ),
  parameters = list(
    reduction = reduction,
    dims = dims,
    graph_name = graph_name,
    umap_key = umap_key,
    cluster_key = cluster_key,
    resolution = resolution,
    seed = seed
  ),
  outputs = list(
    graphs = Graphs(object),
    reductions = Reductions(object),
    cluster_key = cluster_key,
    cluster_counts = as.list(table(clusters))
  )
)
write_json(report, report_json, auto_unbox = TRUE, pretty = TRUE)
