#!/usr/bin/python

import json
import re
import os
from nose.tools import assert_equals
from nose.tools import assert_true
from nose.tools import nottest


def read_result(filename):
    "this returns JSON"

    with open(filename, 'r') as file_in:
        contents = file_in.read()
        match = re.search(
            "---> PRISM JOB UUID = .*?\n(.*?)<--- PRISM JOB UUID", contents, re.DOTALL)
        # print match
        if match:
            output_metadata = match.group(1).strip()
            if not output_metadata:
                return None
            result = json.loads(output_metadata)
            return result
        else:
            return None


def assert_result_exists(result):
    "the result should exists"

    assert_true(result is not None, "The result is not found, or perhaps work is still in progress?")
    assert_true(len(result) != 0, "The result is empty")


def test_samtools_checksum():
    "samtools.sam2bam should return generate the correct output"

    result = read_result('./outputs/samtools-sam2bam.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['bam']['basename'], 'sample.bam')
    assert_equals(result['bam']['checksum'], 'sha1$ff575d96fdad1e1769425687997d155e1775a9d9')
    assert_equals(result['bam']['class'], 'File')


def test_gatk_FindCoveredIntervals():
    "gatk.findCoveredIntervals should generate the correct output"

    result = read_result('./outputs/cmo-gatk.FindCoveredIntervals.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['fci_list']['basename'], 'intervals.list')
    assert_equals(result['fci_list']['checksum'], 'sha1$bf0fad5c4a0bb7f387eca7f4fea57deb34812a18')
    assert_equals(result['fci_list']['class'], 'File')


def test_abra():
    "abra should generate the correct output"

    result = read_result('./outputs/cmo-abra.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(len(result['outbams']), 2)
    assert_equals(result['outbams'][0]['checksum'], 'sha1$d35d2a2c4251f48cde89cc9c21328ac0360cc142')
    assert_equals(result['outbams'][0]['basename'], 'sample1.abra.bam')
    assert_equals(result['outbams'][0]['class'], 'File')
    assert_equals(result['outbams'][1]['checksum'], 'sha1$d35d2a2c4251f48cde89cc9c21328ac0360cc142')
    assert_equals(result['outbams'][1]['basename'], 'sample2.abra.bam')
    assert_equals(result['outbams'][1]['class'], 'File')


def test_bwa_mem():
    "bwa mem should generate the correct output"

    result = read_result('./outputs/cmo-bwa-mem.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['bam']['checksum'], 'sha1$e775a05c99c5a0fe8b5d864ea3ad1cfc0c7e4fd1')
    assert_equals(result['bam']['basename'], 'P1.bam')
    assert_equals(result['bam']['class'], 'File')


def test_gatk_SomaticIndelDetector():
    "gatk.somaticIndelDetector should generate the correct output"

    result = read_result('./outputs/cmo-gatk.SomaticIndelDetector.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('output' in result)
    assert_equals(result['output']['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.sid.vcf')
    assert_equals(result['output']['class'], 'File')

    assert_true('verbose_output' in result)
    assert_equals(result['verbose_output']['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.sid.txt')
    assert_equals(result['verbose_output']['class'], 'File')


def test_list2bed():
    "list2bed should generate the correct output"

    result = read_result('./outputs/cmo-list2bed.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('output_file' in result)
    assert_equals(result['output_file']['basename'], 'intervals.bed')
    assert_equals(result['output_file']['class'], 'File')


def test_mutect():
    "mutect should generate the correct output"

    result = read_result('./outputs/cmo-mutect.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('output' in result)
    assert_equals(result['output']['basename'],
                  'P1_ADDRG_MD.abra.fmi.printreads.mutect.vcf')
    assert_equals(result['output']['class'], 'File')
    assert_equals(result['callstats_output']['basename'],
                  'P1_ADDRG_MD.abra.fmi.printreads.mutect.txt')
    assert_equals(result['callstats_output']['class'], 'File')


def test_picard_AddOrReplaceReadGroups():
    "picard.addOrReplaceReadGroups should generate the correct output"

    result = read_result('./outputs/cmo-picard.AddOrReplaceReadGroups.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('bam' in result)
    assert_equals(result['bam']['basename'], 'P-0000377-T02-IM3_ARRDRG.bam')
    assert_equals(result['bam']['class'], 'File')

    assert_true('bai' in result)
    assert_equals(result['bai']['basename'], 'P-0000377-T02-IM3_ARRDRG.bai')
    assert_equals(result['bai']['class'], 'File')


def test_picard_MarkDuplicates():
    "picard.markDuplicates should generate the correct output"

    result = read_result('./outputs/cmo-picard.MarkDuplicates.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('bam' in result)
    assert_equals(result['bam']['basename'], 'P-0000377-T02-IM3_ARRDRG_MD.bam')
    assert_equals(result['bam']['class'], 'File')

    assert_true('mdmetrics' in result)
    assert_equals(result['mdmetrics']['basename'], 'P-0000377-T02-IM3_ARRDRG_MD.metrics')
    assert_equals(result['mdmetrics']['class'], 'File')

    assert_true('bai' in result)


def test_pindel():
    "pindel should generate the correct output"

    result = read_result('./outputs/cmo-pindel.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('output' in result)
    assert_equals(result['output']['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.pindel.vcf')
    assert_equals(result['output']['class'], 'File')


def test_trimgalore():
    "trimgalore should generate the correct output"

    result = read_result('./outputs/cmo-trimgalore.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('clfastq1' in result)
    assert_equals(result['clfastq1']['basename'], 'P1_R1_cl.fastq.gz')
    assert_equals(result['clfastq1']['class'], 'File')

    assert_true('clfastq2' in result)
    assert_equals(result['clfastq2']['basename'], 'P1_R2_cl.fastq.gz')
    assert_equals(result['clfastq2']['class'], 'File')

    assert_true('clstats1' in result)
    assert_equals(result['clstats1']['basename'], 'P1_R1_cl.stats')
    assert_equals(result['clstats1']['class'], 'File')

    assert_true('clstats2' in result)
    assert_equals(result['clstats2']['basename'], 'P1_R2_cl.stats')
    assert_equals(result['clstats2']['class'], 'File')


def test_bsub_of_roslin_runner():
    "bsubsing roslin runner should still generate the correct output"

    result = read_result('./outputs/bsub-of-prism-runner.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('bam' in result)
    assert_equals(result['bam']['basename'], 'sample.bam')
    assert_equals(result['bam']['class'], 'File')


def test_basic_filtering_mutect():
    "basic-filtering.mutect should generate the correct output"

    result = read_result('./outputs/basic-filtering.mutect.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true(result['vcf']['size'] > 0)
    assert_equals(result['vcf']['basename'], 'DU874145-T.rg.md.abra.fmi.printreads.mutect_STDfilter.vcf')
    assert_equals(result['vcf']['class'], 'File')

    assert_true(result['txt']['size'] > 0)
    assert_equals(result['txt']['basename'], 'DU874145-T.rg.md.abra.fmi.printreads.mutect_STDfilter.txt')
    assert_equals(result['txt']['class'], 'File')


def test_basic_filtering_pindel():
    "basic-filtering.pindel should generate the correct output"

    result = read_result('./outputs/basic-filtering.pindel.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true(result['vcf']['size'] > 0)
    assert_equals(result['vcf']['basename'], 'DU874145-T.rg.md.abra.fmi.printreads.pindel_STDfilter.vcf')
    assert_equals(result['vcf']['class'], 'File')

    # assert_true(result['txt']['size'] > 0)
    assert_equals(result['txt']['basename'], 'DU874145-T.rg.md.abra.fmi.printreads.pindel_STDfilter.txt')
    assert_equals(result['txt']['class'], 'File')


def test_basic_filtering_sid():
    "basic-filtering.somaticIndelDetector should generate the correct output"

    result = read_result('./outputs/basic-filtering.somaticIndelDetector.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true(result['vcf']['size'] > 0)
    assert_equals(result['vcf']['basename'], 'DU874145-T.rg.md.abra.fmi.printreads.sid_STDfilter.vcf')
    assert_equals(result['vcf']['class'], 'File')

    # assert_true(result['txt']['size'] > 0)
    assert_equals(result['txt']['basename'], 'DU874145-T.rg.md.abra.fmi.printreads.sid_STDfilter.txt')
    assert_equals(result['txt']['class'], 'File')


@nottest
def test_basic_filtering_vardict():
    "basic-filtering.vardict should generate the correct output"

    result = read_result('./outputs/basic-filtering.vardict.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true(result['vcf']['size'] > 0)
    assert_equals(result['vcf']['basename'], 'DU874145-T.rg.md.abra.fmi.printreads.vardict_STDfilter.vcf')
    assert_equals(result['vcf']['class'], 'File')

    assert_true(result['txt']['size'] > 0)
    assert_equals(result['txt']['basename'], 'DU874145-T.rg.md.abra.fmi.printreads.vardict_STDfilter.txt')
    assert_equals(result['txt']['class'], 'File')


def test_bcftools_norm_mutect():
    "bcftools.norm.mutect should generate the correct output"

    result = read_result('./outputs/cmo-bcftools.norm.mutect.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['vcf']['basename'], 'mutect-norm.vcf')
    assert_equals(result['vcf']['class'], 'File')


def test_bcftools_norm_pindel():
    "bcftools.norm.pindel should generate the correct output"

    result = read_result('./outputs/cmo-bcftools.norm.pindel.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['vcf']['basename'], 'pindel-norm.vcf')
    assert_equals(result['vcf']['class'], 'File')


def test_bcftools_norm_vardict():
    "bcftools.norm.vardict should generate the correct output"

    result = read_result('./outputs/cmo-bcftools.norm.vardict.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['vcf']['basename'], 'vardict-norm.vcf')
    assert_equals(result['vcf']['class'], 'File')


def test_bcftools_norm_sid():
    "bcftools.norm.somaticIndelDetector should generate the correct output"

    result = read_result('./outputs/cmo-bcftools.norm.somaticIndelDetector.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['vcf']['basename'], 'sid-norm.vcf')
    assert_equals(result['vcf']['class'], 'File')


def test_gatk_CombineVariants():
    "gatk.combineVariants should generate the correct output"

    result = read_result('./outputs/cmo-gatk.CombineVariants.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['out_vcf']['basename'], 'DU874145-T.combined-variants.vcf')
    assert_equals(result['out_vcf']['class'], 'File')


def test_env():
    "env should generate env.txt"

    result = read_result('./outputs/env.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['output']['basename'], 'env.txt')
    assert_equals(result['output']['class'], 'File')


def test_module_1():
    "module 1 should generate the correct output"

    result = read_result('./outputs/module-1.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('clstats1' in result)
    assert_true('clstats2' in result)
    assert_true('bam' in result)
    assert_true('bai' in result)
    assert_true('md_metrics' in result)


def test_module_2():
    "module 2 should generate the correct output"

    result = read_result('./outputs/module-2.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('covint_list' in result)
    assert_equals(result['covint_list']['basename'], 'intervals.list')

    assert_equals(len(result['bams']), 2)
    assert_equals(result['bams'][0]['basename'], 'P2_ADDRG_MD.abra.fmi.printreads.bam')
    assert_equals(result['bams'][1]['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.bam')
    assert_equals(result['bams'][0]['class'], 'File')
    assert_equals(result['bams'][1]['class'], 'File')
    assert_true(result['bams'][0]['size'] > 0)
    assert_true(result['bams'][1]['size'] > 0)
    assert_equals(result['bams'][0]['secondaryFiles'][0]['basename'], 'P2_ADDRG_MD.abra.fmi.printreads.bai')
    assert_equals(result['bams'][1]['secondaryFiles'][0]['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.bai')
    assert_true(result['bams'][0]['secondaryFiles'][0]['size'] > 0)
    assert_true(result['bams'][1]['secondaryFiles'][0]['size'] > 0)


def test_module_3():
    "module 3 should generate the correct output"

    result = read_result('./outputs/module-3.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_true('mutect_vcf' in result)
    assert_true('mutect_callstats' in result)
    assert_true('somaticindeldetector_vcf' in result)
    assert_true('somaticindeldetector_verbose_vcf' in result)
    assert_true('vardict_vcf' in result)

    assert_equals(result['pindel_vcf']['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.pindel.vcf')
    assert_true(result['pindel_vcf']['size'] > 0)
    assert_equals(result['mutect_vcf']['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.mutect.vcf')
    assert_true(result['mutect_vcf']['size'] > 0)
    assert_equals(result['mutect_callstats']['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.mutect.txt')
    assert_true(result['mutect_callstats']['size'] > 0)
    assert_equals(result['vardict_vcf']['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.vardict.vcf')
    assert_true(result['vardict_vcf']['size'] > 0)
    assert_equals(result['somaticindeldetector_vcf']['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.sid.vcf')
    assert_true(result['somaticindeldetector_vcf']['size'] > 0)
    assert_equals(result['somaticindeldetector_verbose_vcf']['basename'], 'P1_ADDRG_MD.abra.fmi.printreads.sid.txt')
    assert_true(result['somaticindeldetector_verbose_vcf']['size'] > 0)


def test_module_1_scatter():
    "module 1 scatter should generate the correct output"

    result = read_result('./outputs/module-1.scatter.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(len(result['clstats1']), 2)
    assert_equals(result['clstats1'][0]['basename'], 'P1_R1_cl.stats')
    assert_equals(result['clstats1'][1]['basename'], 'P2_R1_cl.stats')

    assert_equals(len(result['clstats2']), 2)
    assert_equals(result['clstats2'][0]['basename'], 'P1_R2_cl.stats')
    assert_equals(result['clstats2'][1]['basename'], 'P2_R2_cl.stats')

    assert_equals(len(result['bam']), 2)
    assert_equals(result['bam'][0]['basename'], 's_C_000269_T001_d.rg.md.bam')
    assert_equals(len(result['bam'][0]['secondaryFiles']), 1)
    assert_equals(result['bam'][0]['secondaryFiles'][0]['basename'], 's_C_000269_T001_d.rg.md.bai')
    assert_equals(result['bam'][1]['basename'], 's_C_000269_N001_d.rg.md.bam')
    assert_equals(len(result['bam'][1]['secondaryFiles']), 1)
    assert_equals(result['bam'][1]['secondaryFiles'][0]['basename'], 's_C_000269_N001_d.rg.md.bai')

    assert_equals(len(result['md_metrics']), 2)
    assert_equals(result['md_metrics'][0]['basename'], 's_C_000269_T001_d.rg.md_metrics')
    assert_equals(result['md_metrics'][1]['basename'], 's_C_000269_N001_d.rg.md_metrics')


def test_module_1_2_3():
    "module 1-2-3 should generate the correct output"

    result = read_result('./outputs/module-1-2-3.txt')

    assert_result_exists(result)

    tumor = 'DU874145-T'
    normal = 'DU874145-N'

    # absolute minimum test
    assert_equals(len(result['clstats1']), 2)
    assert_equals(result['clstats1'][0][0]['basename'], tumor + '_R1_cl.stats')
    assert_equals(result['clstats1'][1][0]['basename'], normal + '_R1_cl.stats')

    assert_equals(len(result['clstats2']), 2)
    assert_equals(result['clstats2'][0][0]['basename'], tumor + '_R2_cl.stats')
    assert_equals(result['clstats2'][1][0]['basename'], normal + '_R2_cl.stats')

    assert_equals(len(result['bams']), 2)
    assert_equals(result['bams'][0]['basename'], normal + '.rg.md.abra.fmi.printreads.bam')
    assert_equals(result['bams'][1]['basename'], tumor + '.rg.md.abra.fmi.printreads.bam')

    assert_equals(len(result['md_metrics']), 2)
    assert_equals(result['md_metrics'][0][0]['basename'], tumor + '.rg.md_metrics')
    assert_equals(result['md_metrics'][1][0]['basename'], normal + '.rg.md_metrics')

    assert_equals(result['somaticindeldetector_vcf'][0]['basename'], tumor + '.rg.md.abra.fmi.printreads.sid.vcf')
    assert_equals(result['somaticindeldetector_verbose_vcf'][0]['basename'], tumor + '.rg.md.abra.fmi.printreads.sid.txt')
    assert_equals(result['pindel_vcf'][0]['basename'], tumor + '.pindel.vcf')
    assert_equals(result['vardict_vcf'][0]['basename'], tumor + '.rg.md.abra.fmi.printreads.vardict.vcf')
    assert_equals(result['mutect_vcf'][0]['basename'], tumor + '.rg.md.abra.fmi.printreads.mutect.vcf')
    assert_equals(result['mutect_callstats'][0]['basename'], tumor + '.rg.md.abra.fmi.printreads.mutect.txt')


def test_sort_bams_by_pair():
    "sort-bams-by-pair should generate the correct output"

    result = read_result('./outputs/sort-bams-by-pair.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(len(result['tumor_bams']), 1)
    assert_equals(result['tumor_bams'][0]['basename'], 's_C_000269_T001_d.rg.md.bam')
    assert_equals(len(result['normal_bams']), 1)
    assert_equals(result['normal_bams'][0]['basename'], 's_C_000269_N001_d.rg.md.bam')
    assert_equals(len(result['tumor_sample_ids']), 1)
    assert_equals(result['tumor_sample_ids'][0], 's_C_000269_T001_d')
    assert_equals(len(result['normal_sample_ids']), 1)
    assert_equals(result['normal_sample_ids'][0], 's_C_000269_N001_d')


def test_cmo_index():
    "cmo_index should generate the correct output"

    result = read_result('./outputs/cmo-index.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['tumor_bam']['basename'], 's_C_000269_N001_d.rg.md.bam')
    assert_equals(result['normal_bam']['basename'], 's_C_000269_T001_d.rg.md.bam')

    # fixme: add secondaryFiles check


def test_flatten_array():
    "flatten-array should generate the correct output"

    result = read_result('./outputs/flatten-array.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(len(result['bams']), 2)
    assert_equals(result['bams'][0]['basename'], 's_C_000269_N001_d.rg.md.bam')
    assert_equals(result['bams'][0]['secondaryFiles'][0]['basename'], 's_C_000269_N001_d.rg.md.bai')
    assert_equals(result['bams'][1]['basename'], 's_C_000269_T001_d.rg.md.bam')
    assert_equals(result['bams'][1]['secondaryFiles'][0]['basename'], 's_C_000269_T001_d.rg.md.bai')


def test_vcf2maf():
    "vcf2maf should generate the correct output"

    result = read_result('./outputs/cmo-vcf2maf.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['output']['basename'], 'DU874145-T.combined-variants.vep.maf')
    assert_true(result['output']['size'] > 0)


def test_remove_variants():
    "remove-variants should generate the correct output"

    result = read_result('./outputs/remove-variants.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['maf']['basename'], 'DU874145-T.combined-variants.vep.rmv.maf')
    assert_true(result['maf']['size'] > 0)


def test_replace_allele_counts():
    "replace-allele-counts should generate the correct output"

    result = read_result('./outputs/remove-variants.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['maf']['basename'], 'DU874145-T.combined-variants.vep.rmv.maf')
    assert_true(result['maf']['size'] > 0)


def test_fillout_tumor_normal():
    "fillout_tumor_normal should generate the correct output"

    result = read_result('./outputs/cmo-fillout.tumor-normal.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['fillout']['basename'], 'DU874145-T.combined-variants.vep.rmv.maf.tumor-normal.fillout')
    assert_true(result['fillout']['size'] > 0)


def test_fillout_curated_bams():
    "fillout_curated_bams should generate the correct output"

    result = read_result('./outputs/cmo-fillout.curated-bams.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['fillout']['basename'], 'DU874145-T.combined-variants.vep.rmv.maf.curated.fillout')
    assert_true(result['fillout']['size'] > 0)


def test_ngs_filters():
    "ngs_filters should generate the correct output"

    result = read_result('./outputs/ngs-filters.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['output']['basename'], "DU874145-T.maf")
    assert_true(result['output']['size'] > 0)


def test_module_4():
    "module 4 should generate the correct output"

    result = read_result('./outputs/module-4.txt')

    assert_result_exists(result)

    # absolute minimum test
    assert_equals(result['maf']['basename'], "DU874145-T.maf")
    assert_true(result['maf']['size'] > 0)

    with open(result["maf"]["path"], "r") as maf_file:
        lines = [line.rstrip("\n") for line in maf_file.readlines()]
        git_commit_hash = "3c5a9ddc4068dad28a894275167978bae80a286d"
        assert_equals(lines[1], "#ngs-filters/applyFilter.sh VERSION=" + git_commit_hash + " FILTER=filter_blacklist_regions.R")
        assert_equals(lines[2], "#ngs-filters/applyFilter.sh VERSION=" + git_commit_hash + " FILTER=filter_low_conf.R")
        assert_equals(lines[3], "#ngs-filters/applyFilter.sh VERSION=" + git_commit_hash + " FILTER=filter_ffpe.R")
        assert_equals(lines[4], "#ngs-filters/applyFilter.sh VERSION=" + git_commit_hash + " FILTER=filter_dmp.R")
