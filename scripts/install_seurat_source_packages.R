#!/usr/bin/env Rscript

options(repos = c(
  satijalab = "https://satijalab.r-universe.dev",
  bnprks = "https://bnprks.r-universe.dev",
  CRAN = "https://cloud.r-project.org"
))
options(timeout = 600)

source_routes <- list(
  SeuratData = list(
    url = "https://github.com/satijalab/seurat-data/archive/3e51f44303069b64f5dc4d68e6a3d4a343f55c39.tar.gz",
    commit = "3e51f44303069b64f5dc4d68e6a3d4a343f55c39"
  ),
  SeuratWrappers = list(
    url = "https://github.com/satijalab/seurat-wrappers/archive/ffaf74e306279b1ec16e31c9cb2142ebb2bc4bc1.tar.gz",
    commit = "ffaf74e306279b1ec16e31c9cb2142ebb2bc4bc1"
  ),
  SeuratDisk = list(
    url = "https://github.com/mojaveazure/seurat-disk/archive/877d4e18ab38c686f5db54f8cd290274ccdbe295.tar.gz",
    commit = "877d4e18ab38c686f5db54f8cd290274ccdbe295"
  ),
  Azimuth = list(
    url = "https://github.com/satijalab/azimuth/archive/ad5929686e005ae91d8452187a3a1d8c0563fdd5.tar.gz",
    commit = "ad5929686e005ae91d8452187a3a1d8c0563fdd5"
  )
)

azimuth_cran_deps <- c(
  "DT",
  "googlesheets4",
  "shinyBS",
  "shinydashboard",
  "shinyjs"
)

azimuth_bioc_deps <- c(
  "BSgenome.Hsapiens.UCSC.hg38",
  "EnsDb.Hsapiens.v86",
  "JASPAR2020",
  "TFBSTools"
)

parse_packages <- function(args) {
  package_arg <- args[startsWith(args, "--packages=")]
  if (length(package_arg) == 0) {
    return(names(source_routes))
  }
  requested <- strsplit(sub("^--packages=", "", package_arg[[1]]), ",", fixed = TRUE)[[1]]
  requested <- trimws(requested[nzchar(trimws(requested))])
  unknown <- setdiff(requested, names(source_routes))
  if (length(unknown) > 0) {
    stop("Unknown source-route package(s): ", paste(unknown, collapse = ", "))
  }
  ordered <- names(source_routes)[names(source_routes) %in% requested]
  if ("Azimuth" %in% ordered && !requireNamespace("SeuratDisk", quietly = TRUE)) {
    ordered <- unique(c("SeuratDisk", ordered))
  }
  ordered
}

configure_conda_ca <- function() {
  prefix <- dirname(dirname(R.home()))
  ca <- file.path(prefix, "ssl", "cacert.pem")
  old_ca <- "/home/heybro/mnt/workspace/seurat_tutorial/conda_env/ssl/cacert.pem"
  if (file.exists(ca)) {
    if (!nzchar(Sys.getenv("SSL_CERT_FILE")) || identical(Sys.getenv("SSL_CERT_FILE"), old_ca)) {
      Sys.setenv(SSL_CERT_FILE = ca)
    }
    if (!nzchar(Sys.getenv("CURL_CA_BUNDLE")) || identical(Sys.getenv("CURL_CA_BUNDLE"), old_ca)) {
      Sys.setenv(CURL_CA_BUNDLE = ca)
    }
    if (!nzchar(Sys.getenv("REQUESTS_CA_BUNDLE")) || identical(Sys.getenv("REQUESTS_CA_BUNDLE"), old_ca)) {
      Sys.setenv(REQUESTS_CA_BUNDLE = ca)
    }
  }
}

install_if_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}

install_bioc_if_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install_if_missing("BiocManager")
    BiocManager::install(pkg, ask = FALSE, update = FALSE)
  }
}

install_azimuth_dependencies <- function() {
  for (pkg in azimuth_cran_deps) {
    install_if_missing(pkg)
  }
  for (pkg in azimuth_bioc_deps) {
    install_bioc_if_missing(pkg)
  }
}

install_archive_if_missing <- function(pkg, url) {
  if (requireNamespace(pkg, quietly = TRUE)) {
    return(list(package = pkg, status = "already_installed", version = as.character(packageVersion(pkg))))
  }

  if (identical(pkg, "Azimuth")) {
    install_azimuth_dependencies()
  }

  tarball <- tempfile(fileext = ".tar.gz")
  download.file(url, tarball, mode = "wb", quiet = FALSE)
  install.packages(tarball, repos = NULL, type = "source")
  if (!requireNamespace(pkg, quietly = TRUE)) {
    stop(pkg, " did not load after installation")
  }
  list(package = pkg, status = "installed", version = as.character(packageVersion(pkg)))
}

args <- commandArgs(trailingOnly = TRUE)
configure_conda_ca()
packages <- parse_packages(args)
failures <- character()

for (pkg in packages) {
  result <- tryCatch(
    install_archive_if_missing(pkg, source_routes[[pkg]]$url),
    error = function(err) {
      list(package = pkg, status = "failed", version = NA_character_, error = conditionMessage(err))
    }
  )
  if (identical(result$status, "failed")) {
    failures <- c(failures, pkg)
    message(pkg, " was not installed: ", result$error)
  } else {
    message(pkg, " ", result$status, " ", result$version)
  }
}

if (length(failures) > 0) {
  message("Missing optional packages after this run: ", paste(failures, collapse = ", "))
  quit(status = 1)
}
