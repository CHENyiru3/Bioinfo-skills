rule scrna_marker_ranking:
    input:
        h5ad=config["input_h5ad"]
    output:
        h5ad=config["outputs"]["h5ad"],
        markers_tsv=config["outputs"]["markers_tsv"],
        group_sizes_json=config["outputs"]["group_sizes_json"],
        params_json=config["outputs"]["params_json"],
        versions_json=config["outputs"]["versions_json"]
    log:
        config["logs"]["marker_ranking"]
    benchmark:
        config["benchmarks"]["marker_ranking"]
    conda:
        "../envs/scverse.yaml"
    params:
        groupby=config["params"]["groupby"],
        expression_source=config["params"]["expression_source"],
        layer=config["params"].get("layer", ""),
        method=config["params"]["method"],
        reference=config["params"]["reference"],
        n_genes=config["params"]["n_genes"],
        key_added=config["params"]["key_added"]
    shell:
        (
            "python wrappers/python/scanpy_rank_cluster_markers.py "
            "--input-h5ad {input.h5ad:q} "
            "--output-h5ad {output.h5ad:q} "
            "--output-table {output.markers_tsv:q} "
            "--group-sizes-json {output.group_sizes_json:q} "
            "--params-json {output.params_json:q} "
            "--versions-json {output.versions_json:q} "
            "--groupby {params.groupby:q} "
            "--expression-source {params.expression_source:q} "
            "--layer {params.layer:q} "
            "--method {params.method:q} "
            "--reference {params.reference:q} "
            "--n-genes {params.n_genes:q} "
            "--key-added {params.key_added:q} "
            "> {log:q} 2>&1"
        )
