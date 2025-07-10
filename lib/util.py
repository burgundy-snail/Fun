import subprocess
import bioframe
import pandas as pd

def align_track_with_chromsize(track, chromsizes):
    """
    Aligns a signal track with chromosome sizes, ensuring that 'end' coordinates do not exceed chromosome sizes.

    Args:
        track (DataFrame): Signal track of SoN.
        chromsizes (DataFrame): DataFrame containing information of chromosome sizes.

    Returns:
        DataFrame: Refined SoN with adjusted 'end' coordinates.
    """
    track = track.copy()

    # Get chromosome information from the track
    chrom = track['chr'].unique().item()
    print(f"[DEBUG] Requested chrom: '{chrom}'")
    print(f"[DEBUG] Available chromsizes keys: {list(chromsizes.index)}")


    # Get chromosome size

    # redone to catch errors
    # add smth to normalize chrom names?
    try:
        size = chromsizes.at[chrom]
    except KeyError:
        alt_chrom = chrom.removeprefix("chr") if chrom.startswith("chr") else "chr" + chrom
        print(f"[DEBUG] Trying alternate chrom: '{alt_chrom}'")
        """
        # Try stripping 'chr' if not found
        alt_chrom = chrom.removeprefix("chr") if chrom.startswith("chr") else "chr" + chrom
        size = chromsizes.at[alt_chrom]
        """
        try:
            size = chromsizes.at[alt_chrom]
        except KeyError as e:
            print(f"[ERROR] Neither '{chrom}' nor '{alt_chrom}' found in chromsizes index.")
            raise


    # Update 'end' coordinates exceeding chromosome size
    track.loc[track['end'] > size, 'end'] = size

    return track


def bedgraph_to_bigwig(bedGraphToBigWig, track_path, chromsizes_path, bigwig_output_path):
    """

    Args:
        bedGraphToBigWig (str): Path to bedGraphToBigWig from UCSC
        bedgraph_path (str): Path to the input bedGraph file.
        chromsize_path (str): Path to the chromosome size file.
        bigwig_output_path (str): Path to save the output BigWig file.

    Returns:
        None
    """
    cmd = [bedGraphToBigWig, track_path, chromsizes_path, bigwig_output_path]
    subprocess.run(cmd)