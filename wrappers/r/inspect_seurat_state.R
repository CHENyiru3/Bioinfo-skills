#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(Seurat)
  library(SeuratObject)
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

input_rds <- arg_value("--input-rds")
output_json <- arg_value("--output-json")
output_md <- arg_value("--output-md")
versions_json <- arg_value("--versions-json")

if (is.null(input_rds) || is.null(output_json) || is.null(output_md) || is.null(versions_json)) {
  stop("required args: --input-rds, --output-json, --output-md, --versions-json", call. = FALSE)
}

object <- readRDS(input_rds)
if (!inherits(object, "Seurat")) {
  stop("input object is not a Seurat object", call. = FALSE)
}

safe_names <- function(x) {
  values <- tryCatch(names(x), error = function(e) character())
  if (is.null(values)) character() else as.character(values)
}

assay_summary <- function(object, assay_name) {
  assay <- object[[assay_name]]
  layer_names <- tryCatch(SeuratObject::Layers(assay), error = function(e) character())
  list(
    name = assay_name,
    class = class(assay)[[1]],
    cells = length(Cells(assay)),
    features = length(Features(assay)),
    layers = as.character(layer_names),
    variable_features = length(VariableFeatures(object, assay = assay_name))
  )
}

reduction_summary <- function(object, reduction_name) {
  emb <- Embeddings(object, reduction = reduction_name)
  list(
    name = reduction_name,
    class = class(object[[reduction_name]])[[1]],
    dimensions = unname(dim(emb))
  )
}

graph_summary <- function(object, graph_name) {
  graph <- object[[graph_name]]
  list(
    name = graph_name,
    class = class(graph)[[1]],
    dimensions = unname(dim(graph))
  )
}

image_summary <- function(object, image_name) {
  image <- object@images[[image_name]]
  list(name = image_name, class = class(image)[[1]])
}

metadata <- object[[]]
idents <- Idents(object)
report <- list(
  schema_version = "0.1.0",
  input_path = normalizePath(input_rds, mustWork = FALSE),
  object_type = class(object)[[1]],
  dimensions = list(cells = ncol(object), features = nrow(object)),
  active_assay = DefaultAssay(object),
  assays = lapply(Assays(object), function(x) assay_summary(object, x)),
  reductions = lapply(Reductions(object), function(x) reduction_summary(object, x)),
  graphs = lapply(Graphs(object), function(x) graph_summary(object, x)),
  images = lapply(Images(object), function(x) image_summary(object, x)),
  metadata = list(
    columns = colnames(metadata),
    column_count = ncol(metadata),
    row_count = nrow(metadata),
    rownames_unique = !anyDuplicated(rownames(metadata))
  ),
  identities = list(
    levels = levels(idents),
    counts = as.list(table(idents))
  ),
  commands = safe_names(object@commands),
  warnings = list()
)

if (!any(vapply(report$assays, function(x) "counts" %in% x$layers, logical(1)))) {
  report$warnings <- c(report$warnings, "No assay reports a counts layer.")
}
if (length(report$graphs) > 0) {
  bad_graphs <- vapply(report$graphs, function(x) {
    length(x$dimensions) != 2 || x$dimensions[[1]] != ncol(object) || x$dimensions[[2]] != ncol(object)
  }, logical(1))
  if (any(bad_graphs)) {
    report$warnings <- c(report$warnings, "One or more graphs are not cell-by-cell matrices.")
  }
}

versions <- list(
  schema_version = "0.1.0",
  packages = list(
    R = as.character(getRversion()),
    Seurat = as.character(packageVersion("Seurat")),
    SeuratObject = as.character(packageVersion("SeuratObject"))
  )
)

dir.create(dirname(output_json), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(output_md), recursive = TRUE, showWarnings = FALSE)
dir.create(dirname(versions_json), recursive = TRUE, showWarnings = FALSE)
write_json(report, output_json, auto_unbox = TRUE, pretty = TRUE)
write_json(versions, versions_json, auto_unbox = TRUE, pretty = TRUE)

md <- c(
  "# Seurat State Inspection",
  "",
  paste0("- Input: `", report$input_path, "`"),
  paste0("- Cells: `", report$dimensions$cells, "`"),
  paste0("- Features: `", report$dimensions$features, "`"),
  paste0("- Active assay: `", report$active_assay, "`"),
  paste0("- Assays: ", ifelse(length(report$assays), paste(vapply(report$assays, `[[`, "", "name"), collapse = ", "), "none")),
  paste0("- Reductions: ", ifelse(length(report$reductions), paste(vapply(report$reductions, `[[`, "", "name"), collapse = ", "), "none")),
  paste0("- Graphs: ", ifelse(length(report$graphs), paste(vapply(report$graphs, `[[`, "", "name"), collapse = ", "), "none")),
  paste0("- Metadata columns: `", report$metadata$column_count, "`"),
  "",
  "## Warnings",
  ""
)
if (length(report$warnings)) {
  md <- c(md, paste0("- ", unlist(report$warnings)))
} else {
  md <- c(md, "- none")
}
writeLines(md, output_md)
