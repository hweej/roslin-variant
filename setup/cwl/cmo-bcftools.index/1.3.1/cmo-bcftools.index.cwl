#!/usr/bin/env cwl-runner

$namespaces:
  dct: http://purl.org/dc/terms/
  foaf: http://xmlns.com/foaf/0.1/
  doap: http://usefulinc.com/ns/doap#

$schemas:
- http://dublincore.org/2012/06/14/dcterms.rdf
- http://xmlns.com/foaf/spec/20140114.rdf
- http://usefulinc.com/ns/doap#

doap:release:
- class: doap:Version
  doap:name: cmo-bcftools.index
  doap:revision: 1.3.1
- class: doap:Version
  doap:name: cwl-wrapper
  doap:revision: 1.0.0

dct:creator:
- class: foaf:Organization
  foaf:name: Memorial Sloan Kettering Cancer Center
  foaf:member:
  - class: foaf:Person
    foaf:name: Zuojian Tang
    foaf:mbox: mailto:tangz@mskcc.org

dct:contributor:
- class: foaf:Organization
  foaf:name: Memorial Sloan Kettering Cancer Center
  foaf:member:
  - class: foaf:Person
    foaf:name: Zuojian Tang
    foaf:mbox: mailto:tangz@mskcc.org
  - class: foaf:Person
    foaf:name: Cyriac Kandoth
    foaf:mbox: mailto:ckandoth@gmail.com

cwlVersion: cwl:v1.0

class: CommandLineTool
baseCommand: [cmo_bcftools, index]

requirements:
  InlineJavascriptRequirement: {}
  ResourceRequirement:
    ramMin: 8
    coresMin: 1

doc: |
  index VCF/BCF files

inputs:
  
  csi:
    type: ["null", boolean]
    doc: generate CSI-format index for VCF/BCF files [default]
    inputBinding:
      prefix: --csi 

  force:
    type: ["null", boolean]
    doc: overwrite index if it already exists [default]
    inputBinding:
      prefix: --force 

  min_shift:
    type: ["null", str]
    doc: INT set minimal interval size for CSI indices to 2^INT [14]
    inputBinding:
      prefix: --min-shift 

  nrecords:
    type: ["null", boolean]
    default: False
    doc: print number of records based on existing index file
    inputBinding:
      prefix: --nrecords 

  stats:
    type: ["null", boolean]
    default: False
    doc: print per contig stats based on existing index file
    inputBinding:
      prefix: --stats 

  tbi:
    type: ["null", boolean]
    default: False
    doc: generate TBI-format index for VCF files
    inputBinding:
      prefix: --tbi 

  vcf:
    type: 
    - string
    - File
    inputBinding:
      position: 1


outputs:
  tbi_file:
    type: File
    outputBinding:
      glob: "*.tbi"
