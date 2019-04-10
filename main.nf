#!/usr/bin/env nextflow

Channel
    .fromPath("${params.input_folder}/*")
    .ifEmpty { exit 1, "Input folder containing zipped .ecw files not found: ${params.input_folder}" }
    .set { input_folder }

process unzip {
    tag "$zip"
    container 'lifebitai/ecw_converter:latest'

    input:
    file zip from input_folder

    output:
    file("**.ecw") into ecw

    script:
    """
    unzip $zip
    """
}

ecw
    .map { file -> tuple(file.baseName, file) }
    .set { ecw_to_valiadte }

process ecw_converter {
    tag "$ecw"
    publishDir 'results', mode: 'copy'
    container 'lifebitai/ecw_converter:latest'

    input:
    set val(name), file(ecw) from ecw_to_valiadte

    output:
    set val(name), file("img/compliant-cog/${name}.tif") into tif

    script:
    """
    ecw_convert_2_cog.py . . ?
    """
}

process validate_tif {
    tag "$tif"
    publishDir 'results', mode: 'copy'
    container 'lifebitai/ecw_converter:latest'

    input:
    set val(name), file(tif) from tif

    output:
    file("**.log") into log

    script:
    """
    mkdir logs
    validate_cog.py $tif &> logs/validate_cog_${name}.log
    """
}