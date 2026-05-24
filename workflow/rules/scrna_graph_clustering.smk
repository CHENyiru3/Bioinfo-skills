rule scrna_graph_clustering:
    input:
        h5ad=config["input_h5ad"]
    output:
        h5ad=config["outputs"]["h5ad"],
        embedding_tsv=config["outputs"]["embedding_tsv"],
        cluster_sizes_json=config["outputs"]["cluster_sizes_json"],
        params_json=config["outputs"]["params_json"],
        versions_json=config["outputs"]["versions_json"]
    log:
        config["logs"]["graph_clustering"]
    benchmark:
        config["benchmarks"]["graph_clustering"]
    conda:
        "../envs/scverse.yaml"
    params:
        representation_key=config["params"]["representation_key"],
        neighbors_key=config["params"]["neighbors_key"],
        embedding_key=config["params"]["embedding_key"],
        cluster_key=config["params"]["cluster_key"],
        n_neighbors=config["params"]["n_neighbors"],
        n_pcs=config["params"]["n_pcs"],
        metric=config["params"]["metric"],
        neighbors_method=config["params"]["neighbors_method"],
        umap_min_dist=config["params"]["umap_min_dist"],
        umap_spread=config["params"]["umap_spread"],
        resolution=config["params"]["resolution"],
        random_state=config["params"]["random_state"],
        leiden_flavor=config["params"]["leiden_flavor"],
        overwrite_flag="--overwrite" if config["params"].get("overwrite", False) else ""
    shell:
        (
            "python wrappers/python/scanpy_neighbors_umap_leiden.py "
            "--input-h5ad {input.h5ad:q} "
            "--output-h5ad {output.h5ad:q} "
            "--embedding-tsv {output.embedding_tsv:q} "
            "--cluster-sizes-json {output.cluster_sizes_json:q} "
            "--params-json {output.params_json:q} "
            "--versions-json {output.versions_json:q} "
            "--representation-key {params.representation_key:q} "
            "--neighbors-key {params.neighbors_key:q} "
            "--embedding-key {params.embedding_key:q} "
            "--cluster-key {params.cluster_key:q} "
            "--n-neighbors {params.n_neighbors:q} "
            "--n-pcs {params.n_pcs:q} "
            "--metric {params.metric:q} "
            "--neighbors-method {params.neighbors_method:q} "
            "--umap-min-dist {params.umap_min_dist:q} "
            "--umap-spread {params.umap_spread:q} "
            "--resolution {params.resolution:q} "
            "--random-state {params.random_state:q} "
            "--leiden-flavor {params.leiden_flavor:q} "
            "{params.overwrite_flag} "
            "> {log:q} 2>&1"
        )
