# Template only. Replace placeholders when binding an approved R task.
rule example_rscript_task:
    input:
        input_file="{input_file}"
    output:
        output_file="{output_file}"
    log:
        "logs/example_rscript_task.log"
    benchmark:
        "benchmarks/example_rscript_task.tsv"
    conda:
        "envs/r-seurat.yml"
    params:
        params_json="{params_json}"
    shell:
        "Rscript {script} --params {params.params_json:q} > {log:q} 2>&1"
