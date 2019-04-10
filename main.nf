#!/usr/bin/env nextflow

Channel
    .fromPath("${params.input_folder}/*")
    .ifEmpty { exit 1, "Input folder containing zipped .ecw files not found: ${params.input_folder}" }
    .set { input_folder }

process ecw_converter {
    tag "$zip"
    publishDir 'results', mode: 'copy'
    container 'lifebitai/ecw_converter:latest'

    input:
    file zip from input_folder

    output:
    file("**.tif") into results

    script:
    """
    ecw_to_cog.sh
    """
}