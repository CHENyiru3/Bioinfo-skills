# Template only. Replace placeholders when binding an approved task.
rule example_python_task:
    input:
        input_file="{input_file}"
    output:
        output_file="{output_file}"
    log:
        "logs/example_python_task.log"
    benchmark:
        "benchmarks/example_python_task.tsv"
    conda:
        "envs/scverse-python.yml"
    params:
        params_json="{params_json}"
    shell:
        "python {wrapper} --params {params.params_json:q} > {log:q} 2>&1"
