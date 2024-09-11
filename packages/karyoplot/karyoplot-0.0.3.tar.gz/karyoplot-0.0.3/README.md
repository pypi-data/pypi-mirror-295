# karyoplot

## What is karyoplot ?

``karyoplot`` is a python package developed to draw simple karyoplot/ideogram with a simple configuration file like Circos [1], without any lines of code like karyoploteR [2]. 
``karyoplot`` deals with conventional bioinformatics formats (.bed, .fasta, .gff, .gtf, .vcf, ...) to avoid file manipulations before drawing. 

## How does it work ?

``karyoplot`` takes as an argument a configuration file with different sections which will have a sequence Fasta file as reference for ideograms. Every plot to draw on reference sequences is described in a track section with link to associated data and drawing options.
``karyoplot`` is mainly based on ``matplotlib`` for graph rendering and pysam for bioinformatics file format parsing.

``karyoplot`` is under developpement, currently supported format are:

* fasta
* bed

available soon:

* gff
* vcf
* bam
* wig/bigWig

## Install

**create your virtual env in a dedicated directory**
```
python3 -m venv $HOME/myvenvs/karyoplot
```
**set up the new env**
```
source $HOME/myvenvs/karyoplot/bin/activate
```
**install karyoplot**
``` 
pip install karyoplot 
```
**enjoy**
```
karyoplot -h
```
**to leave the env**
```
deactivate
```

## Usage

**Simple usage**

```
karyoplot config.ini -o genome_karyo.png -v 2
```

The `config.ini` file is a configuration file in Microsoft Windows INI style, readable by the [configparser](https://docs.python.org/3/library/configparser.html) Python module.
Some sections are expected with defined options to customize your plot. See the associated documentation [here](https://bioger.pages.mia.inra.fr/karyoplot/) for full options and required sections/options.

![karyoplot](https://forgemia.inra.fr/bioger/karyoplot/raw/dev/img/typical_karyoplot.png)

## Support
For any request please contact nicolas.lapalu[at]inrae.fr or adeline.simon[at]inrae.fr

## Authors and acknowledgment

* Rosanne Phebe
* Nicolas Lapalu
* Adeline Simon

## License
licensed under GNU General Public License v3.0 


## References

* [1] Krzywinski, M. et al. Circos: an Information Aesthetic for Comparative Genomics. Genome Res (2009) 19:1639-1645
* [2] Bernat Gel & Eduard Serra. (2017). karyoploteR: an R/Bioconductor package to plot customizable genomes displaying arbitrary data. Bioinformatics, 31–33. doi:10.1093/bioinformatics/btx346


