#!/usr/bin/env python3

import re
import sys
import argparse
import logging
import os.path

import matplotlib.pyplot as plt
from pysam import FastaFile

from karyoplot.confparser import Confparser
from karyoplot.entities import Chromosome


def __add_arguments(parser):
    parser.add_argument(
        "config",
        help="Config File",
        type=str
    )

    parser.add_argument(
        "-v", "--verbosity",
        type=int, choices=[1, 2, 3],
        help="increase output verbosity 1=error, 2=info, 3=debug"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output Image",
        default="karyoplot.png"
    )


def main():
    """script entry point"""
    parser = argparse.ArgumentParser()
    __add_arguments(parser)
    args = parser.parse_args()

    log_level = 'ERROR'
    if args.verbosity == 1:
        log_level = 'ERROR'
    if args.verbosity == 2:
        log_level = 'INFO'
    if args.verbosity == 3:
        log_level = 'DEBUG'
    logging.getLogger().setLevel(log_level)

    # Parse arguments

    # Checking if file exists
    if not os.path.exists(args.config):
        logging.error('CONFIG FILE DOES NOT EXISTS')
        exit(0)
    else:
        logging.info('Creating canvas and track objects')
    cp = Confparser()
    cp.read(args.config)
    canvas = cp.get_canvas()
    tracks = cp.get_tracks()
    sequence = cp.get_sequence()

    ##Plot

    # Reading fasta file
    logging.info('Checking if fasta is valid')
    chromosomes = []
    chrom_idx_name = {}
    if sequence.validate():
        fasta_file = FastaFile(sequence.reference)
        # chr_lengths = {}
        logging.info('Getting sequence lengths')
        for chrom_name in fasta_file.references:
            chrom = Chromosome(chrom_name,
                               fasta_file.get_reference_length(chrom_name))
            chromosomes.append(chrom)
            try:
                chrom_idx_name[chrom.name] = chrom
            except:
                raise Exception("Probably duplicate sequence {}, check your reference file".format(chrom.name))

    # f = open(canvas.reference,'r')
    # print(f.readline())

    nb_chr_to_draw = []
    if not sequence.zoom:
        # Verify if the limitesize is bigger than atleast one sequence
        logging.info('Checking if limitesize is valid')
        # max_length = max(chr_lengths.values())
        max_length = max([chrom.length for chrom in chromosomes])
        if max_length <= sequence.limitesize:
            raise ValueError("The limitesize is too BIG, no Chromosome to draw")

        # List of plots that need to be drawn
        for chrom in chromosomes:
            if chrom.length >= sequence.limitesize:
                nb_chr_to_draw.append(chrom)
    else:
        for zoom in cp.get_zooms():
            if zoom[0] not in [chrom.name for chrom in chromosomes]:
                raise Exception("Error in zoom option, {} is not available in reference file".format(zoom[0]))
            else:
                chrom = Chromosome(zoom[0], fasta_file.get_reference_length(zoom[0]))
                # chrom = chrom_idx_name[zoom[0]]
                if zoom[1]:
                    chrom.zoom_min = min(max(chrom.zoom_min, zoom[1]), chrom.zoom_max)

                if zoom[2]:
                    chrom.zoom_max = max(min(chrom.zoom_max, zoom[2]), chrom.zoom_min)
                nb_chr_to_draw.append(chrom)

    # Blank Canvas
    plt.rcParams["figure.figsize"] = (canvas.width, canvas.height)

    # compute size ratios for each plot (using size option)
    size_ratios = []
    for chrom in nb_chr_to_draw:
        size_ratios.append(sequence.size)
        for track in tracks:
            size_ratios.append(track.size)

    # constrained_layout=True, required to avoid overlap of x-axis
    logging.info("Initializing subplots - quite long")
    fig, ax = plt.subplots(len(nb_chr_to_draw) * (len(tracks) + 1), 1, sharex=sequence.sharex,
                           gridspec_kw={'height_ratios': size_ratios}, constrained_layout=canvas.constrained_layout)

    logging.info('Building Sequences')
    for n, chrom in enumerate(nb_chr_to_draw):
        idx = n * (len(tracks) + 1)
        ax[idx].plot([chrom.zoom_min, chrom.zoom_max], [1, 1], linewidth=5, color=sequence.color)
        ax[idx].get_xaxis().set_visible(True)
        ax[idx].margins(0, 0)

        if not sequence.sharex:
            ax[idx].spines['top'].set_visible(False)
            ax[idx].spines['right'].set_visible(False)
            ax[idx].spines['bottom'].set_visible(False)
            ax[idx].ticklabel_format(axis="x", style="sci", scilimits=(0, 6))
            ax[idx].get_xaxis().set_visible(False)
            if sequence.scale:
                ax[idx].spines['bottom'].set_visible(True)
                ax[idx].get_xaxis().set_visible(True)
            ax[idx].spines['left'].set_visible(False)
            ax[idx].get_yaxis().set_visible(False)
            ax[idx].tick_params(axis='x', labelsize=sequence.x_label_fontsize)



        else:
            ax[idx].axis('off')

        ax[idx].text(0, 0, chrom.name, fontsize=sequence.seq_fontsize, transform=ax[idx].transAxes, ha="right",
                     va="baseline")

        #legend_line = []
        #legend_title = []
        for ix, track in enumerate(tracks):
            #legend_title.append(track.title)
            #legend_line.append(Line2D([0, 1], [0, 1], color=track.color))
            idx_track = idx + (ix + 1)
            track.draw_track(sequence, ax[idx_track], chrom, canvas)
    if sequence.scale and sequence.sharex:
        ax[-1].ticklabel_format(axis="x", style="sci", scilimits=(0, 6))
        ax[-1].spines['bottom'].set_visible(True)
        ax[-1].get_xaxis().set_visible(True)
        ax[-1].tick_params(axis='x', labelsize=sequence.x_label_fontsize)


    logging.info("Exporting figure / layout rearrangments")

    plt.rcParams['savefig.facecolor'] = canvas.background_color
    fig.suptitle(canvas.title,fontsize=canvas.title_fontsize)
    #plt.legend(legend_line, legend_title,bbox_to_anchor=(1,1), fontsize=15)
    fig.savefig(args.output)


if __name__ == "__main__":
    sys.exit(main())
