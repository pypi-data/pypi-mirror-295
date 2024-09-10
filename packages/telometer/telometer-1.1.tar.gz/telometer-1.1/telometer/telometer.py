#!/usr/bin/env python3
# Telometer v1.0
# Created by: Santiago E Sanchez
# Artandi Lab, Stanford University, 2024
# Measures telomeres from ONT or PacBio long reads aligned to a T2T genome assembly
# Simple Usage: telometer -b sorted_t2t.bam -o output.tsv

import pysam
import regex as re
import pandas as pd
import time
import argparse
import sys
from multiprocessing import Pool, cpu_count
import numpy as np
from scipy.signal import savgol_filter

def reverse_complement(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    return "".join(complement[base] for base in reversed(seq))

def get_telomere_repeats():
    telomere_repeats = ['CCCTAA', 'TTAGGG']
    telomere_repeats_rc = [reverse_complement(repeat) for repeat in telomere_repeats]
    return telomere_repeats + telomere_repeats_rc

def identify_telomere_regions(seq, base_qualities, telomere_motifs, window_size=120, step_size=12,
                              density_threshold=0.1, max_gap_length=20, quality_threshold=15):
    telomere_regions = []
    current_start = None
    gap_length = 0
    has_large_gap = False
    densities = []

    combined_motif_pattern = '|'.join(f'({motif})' for motif in telomere_motifs)

    for i in range(0, len(seq) - window_size + 1, step_size):
        window_seq = seq[i:i + window_size]
        motif_count = len(re.findall(combined_motif_pattern, window_seq))
        density = motif_count / (window_size / len(telomere_motifs[0]))
        densities.append(density)

        if density >= density_threshold:
            if current_start is None:
                current_start = i
            gap_length = 0
        else:
            if current_start is not None:
                gap_length += step_size

                gap_start = i - gap_length
                gap_end = i
                gap_quality = base_qualities[gap_start:gap_end]

                if len(gap_quality) > 0:
                    avg_gap_quality = sum(gap_quality) / len(gap_quality)
                else:
                    avg_gap_quality = 0

                if avg_gap_quality < quality_threshold:
                    gap_length = 0
                    continue

                if gap_length > max_gap_length:
                    mismatch_motif_count = len(re.findall(f"({combined_motif_pattern}){{e<=1}}", window_seq))
                    mismatch_density = mismatch_motif_count / (window_size / len(telomere_motifs[0]))

                    if mismatch_density >= density_threshold:
                        gap_length = 0
                    else:
                        has_large_gap = True
                        telomere_regions.append((current_start, i - gap_length + step_size))
                        current_start = None
                        gap_length = 0

    if current_start is not None:
        telomere_regions.append((current_start, len(seq)))

    return telomere_regions, densities, has_large_gap, combined_motif_pattern

def detect_discontinuities(base_qualities, window_length=11, polyorder=2, gradient_threshold=-1):
    if len(base_qualities) < window_length:
        window_length = len(base_qualities) if len(base_qualities) % 2 == 1 else len(base_qualities) - 1

    if len(base_qualities) > polyorder:
        smoothed_qualities = savgol_filter(base_qualities, window_length=window_length, polyorder=polyorder)
    else:
        smoothed_qualities = base_qualities

    gradient = np.diff(smoothed_qualities)
    discontinuities = np.where(gradient < gradient_threshold)[0]

    return discontinuities, smoothed_qualities

def check_gap(seq, base_qualities, telomere_regions, gradient_threshold=-1, quality_threshold=15):
    merged_regions = []
    prev_end = None
    current_start = None

    for i, (start, end) in enumerate(telomere_regions):
        if current_start is None:
            current_start = start

        if prev_end is not None:
            gap_start = prev_end
            gap_end = start
            gap_quality = base_qualities[gap_start:gap_end]
            discontinuities, smoothed_qualities = detect_discontinuities(gap_quality, gradient_threshold=gradient_threshold)
            avg_gap_quality = sum(gap_quality) / len(gap_quality) if len(gap_quality) > 0 else 0
            if avg_gap_quality < quality_threshold or len(discontinuities) == 0:
                continue
        merged_regions.append((current_start, end))
        current_start = None
        prev_end = end

    return merged_regions

def measure_telomere_length(seq, telomere_motifs, base_qualities, window_size=120, step_size=12,
                                         density_threshold=0.1, max_gap_length=20, quality_threshold=15):

    telomere_regions, densities, has_large_gap, combined_motif_pattern = identify_telomere_regions(
        seq, base_qualities, telomere_motifs, window_size, step_size, density_threshold, max_gap_length, quality_threshold)

    if not telomere_regions:
        return 0, 0, 0, densities, has_large_gap, combined_motif_pattern


    if not any(density >= 0.75 for density in densities):
        return 0, 0, 0, densities, has_large_gap, combined_motif_pattern


    merged_telomere_regions = check_gap(seq, base_qualities, telomere_regions, gradient_threshold=-1, quality_threshold=quality_threshold)

    terminus_regions = []
    for start, end in merged_telomere_regions:
        if start < 100 or end > len(seq) - 100:
            terminus_regions.append((start, end))

    if not terminus_regions:
        return 0, 0, 0, densities, has_large_gap, combined_motif_pattern


    telomere_start, telomere_end = terminus_regions[0]
    telomere_length = telomere_end - telomere_start

    return telomere_start, telomere_end, telomere_length, densities, has_large_gap, combined_motif_pattern


def process_read(read_data, telomere_motifs, max_gap_length, min_read_len):
    if read_data['is_unmapped'] or read_data['reference_name'] == 'chrM':
        return None

    if read_data['reference_start'] > 30000 and read_data['reference_end'] < read_data['reference_length'] - 30000:
        return None

    seq = read_data['query_sequence']
    base_qualities = read_data['query_qualities']
    if seq is None or len(seq) < min_read_len:
        return None

    alignment_start = read_data['reference_start']
    alignment_end = read_data['reference_end']
    reference_genome_length = read_data['reference_length']

    if alignment_start < 15000 and alignment_end <= reference_genome_length - 30000:
        arm = "p"
    else:
        arm = "q"

    direction = "rev" if read_data['is_reverse'] else "fwd"

    telomere_start, telomere_end, telomere_length, densities, has_large_gap, combined_motif_pattern = measure_telomere_length(
        seq, telomere_motifs, base_qualities, max_gap_length=max_gap_length)

    if telomere_length < 1:
        return None

    if (telomere_length + 50) > len(seq):
        return None

    return {
        'chromosome': read_data['reference_name'],
        'reference_start': alignment_start,
        'reference_end': alignment_end,
        'telomere_length': telomere_length,
        'read_id': read_data['query_name'],
        'mapping_quality': read_data['mapping_quality'],
        'read_length': len(seq),
        'arm': arm,
        'direction': direction
    }

def process_read_wrapper(args):
    return process_read(*args)

def estimate_memory_usage(reads_list):
    """
    Estimate the memory usage of the reads in bytes.
    Approximate size based on the size of sequences, base qualities, and metadata.
    """
    memory_usage = 0
    for read in reads_list:
        seq_len = len(read['query_sequence']) if read['query_sequence'] else 0
        quality_len = len(read['query_qualities']) if read['query_qualities'] else 0
        memory_usage += sys.getsizeof(read['query_name']) + seq_len + quality_len + sys.getsizeof(read)
    return memory_usage

def process_bam_file(bam_file_path, output_file_path, max_gap_length=20, min_read_len=1000, num_processes=8, memory_limit_gb=8):
    start_time = time.time()
    bam_file = pysam.AlignmentFile(bam_file_path, "rb")
    telomere_motifs = get_telomere_repeats()

    results = []
    read_results = {}
    total_reads = 0
    memory_limit_bytes = memory_limit_gb * (1024 ** 3)

    batch = []
    batch_memory = 0

    def process_batch(batch_data):
        nonlocal total_reads, read_results

        with Pool(processes=num_processes) as pool:
            for result in pool.imap_unordered(process_read_wrapper, [(rd, telomere_motifs, max_gap_length, min_read_len) for rd in batch_data]):
                if result:
                    total_reads += 1
                    existing_result = read_results.get(result['read_id'])
                    if existing_result:
                        if (result['mapping_quality'] > existing_result['mapping_quality'] or
                            (result['mapping_quality'] == existing_result['mapping_quality'] and
                            result['telomere_length'] > existing_result['telomere_length'])):
                            read_results[result['read_id']] = result
                    else:
                        read_results[result['read_id']] = result

        batch_data.clear()

    for read in bam_file:
        if read.reference_name is not None and read.reference_name != 'chrM':
            base_qualities = read.query_qualities

            if base_qualities is not None and len(base_qualities) > 0:
                avg_phred_score = sum(base_qualities) / len(base_qualities)
            else:
                avg_phred_score = 0
                #print("no phred score")

            if avg_phred_score > 9:
                read_data = {
                    'query_name': read.query_name,
                    'is_unmapped': read.is_unmapped,
                    'is_reverse': read.is_reverse,
                    'reference_start': read.reference_start,
                    'reference_end': read.reference_end,
                    'reference_name': read.reference_name,
                    'mapping_quality': read.mapping_quality,
                    'query_sequence': read.query_sequence,
                    'query_qualities': base_qualities,
                    'reference_length': bam_file.get_reference_length(read.reference_name) if read.reference_name is not None else None
                }

                read_memory = estimate_memory_usage([read_data])
                batch_memory += read_memory
                batch.append(read_data)

                if batch_memory >= memory_limit_bytes:
                    print(f"Processing batch of {len(batch)} reads, approx memory used: {batch_memory / (1024 ** 3):.2f} GB")
                    process_batch(batch)
                    batch_memory = 0
                    batch = []
            #else:
                #print("low phred")

    if batch:
        print(f"Processing final batch of {len(batch)} reads")
        process_batch(batch)

    bam_file.close()

    results_df = pd.DataFrame(list(read_results.values()))
    results_df.to_csv(output_file_path, sep='\t', index=False)

    print(f"Telometer completed successfully. Total telomeres measured: {len(read_results)}")
    print(f"Total processing time: {time.time() - start_time:.2f} seconds")
    # After the final print statements
    if len(read_results) > 0:
        # Convert read results to a DataFrame for easy statistical computation
        results_df = pd.DataFrame(list(read_results.values()))

        # Calculate summary statistics for the 'telomere_length' column
        telomere_lengths = results_df['telomere_length']

        min_length = telomere_lengths.min()
        percentile_25 = telomere_lengths.quantile(0.25)
        median_length = telomere_lengths.median()
        mean_length = telomere_lengths.mean()
        percentile_75 = telomere_lengths.quantile(0.75)
        max_length = telomere_lengths.max()

        # Print summary statistics
        print("\nTelomere Length Summary Statistics:")
        print(f"Min: {min_length:.2f}")
        print(f"25th Percentile: {percentile_25:.2f}")
        print(f"Median: {median_length:.2f}")
        print(f"Mean: {mean_length:.2f}")
        print(f"75th Percentile: {percentile_75:.2f}")
        print(f"Max: {max_length:.2f}")
    else:
        print("No telomere measurements to summarize.")


def run_telometer():
    parser = argparse.ArgumentParser(description='Calculate telomere length from a BAM file.')
    parser.add_argument('-b', '--bam', help='The path to the sorted BAM file.', required=True)
    parser.add_argument('-o', '--output', help='The path to the output file.', required=True)
    parser.add_argument('-m', '--minreadlen', default=1000, type=int, help='Minimum read length to consider (Default: 1000 for telomere capture, use 4000 for WGS). Optional', required=False)
    parser.add_argument('-g', '--maxgaplen', default=20, type=int, help='Maximum allowed gap length between telomere regions. Optional', required=False)
    parser.add_argument('-t', '--threads', default=cpu_count(), type=int, help='Number of processing threads to use. Optional', required=False)
    parser.add_argument('-l', '--memlimit', default=8, type=int, help="Maximum amount of memory to commit per batch of reads while processing. Optional, default = 8 Gb", required=False)
    args = parser.parse_args()
    process_bam_file(args.bam, args.output, max_gap_length=args.maxgaplen, min_read_len=args.minreadlen, num_processes=args.threads, memory_limit_gb=args.memlimit)

if __name__ == "__main__":
    run_telometer()
