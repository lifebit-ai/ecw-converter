#!/usr/bin/env nextflow

Channel
    .fromPath("${params.input_folder}/*")
    .ifEmpty { exit 1, "Input folder containing zipped .ecw files not found: ${params.input_folder}" }
    .map { file -> tuple(file.baseName, file) }
    .set { input_folder }

process ecw_converter {
    tag "$zip"
    publishDir 'results', mode: 'copy'
    container 'lifebitai/ecw_converter:latest'

    input:
    set val(name), file(zip) from input_folder

    output:
    file("**.tif") into results
    file("**.log") into logs

    script:
    """
    ecw_to_cog.sh
    cd logs && mkdir ${name} && mv *.log ${name}
    """
}