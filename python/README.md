# Mappluspy: mm2-plus Python Binding

Mappluspy provides a convenient interface to
[mm2-plus](https://github.com/at-cg/mm2-plus), an optimized
minimap2-compatible C/C++ program to align genomic and transcript nucleotide
sequences.

Mappluspy is built on the code base and public API design of
[mappy](https://pypi.org/project/mappy/), the official minimap2 Python binding
by Heng Li. We gratefully credit mappy and minimap2 for the original binding
interface and implementation. The key difference is that mappluspy uses
mm2-plus as the base aligner rather than upstream minimap2.

To maintain consistency with mappy for users moving between minimap2 and
mm2-plus, the API descriptions and examples below are adapted from the mappy
documentation and modified to use `mappluspy`.

## Installation

Mappluspy depends on [zlib](http://zlib.net). It can be installed with
[pip](https://en.wikipedia.org/wiki/Pip_(package_manager)):

```shell
pip install --user mappluspy
```

or from the mm2-plus GitHub repository ([Cython](http://cython.org) required):

```shell
git clone https://github.com/at-cg/mm2-plus
cd mm2-plus
python3 -m pip install .
```

## Usage

The following Python script demonstrates the key functionality of mappluspy:

```python
import mappluspy as mp

a = mp.Aligner("test/MT-human.fa")  # load or build index
if not a:
    raise Exception("ERROR: failed to load/build index")

s = a.seq("MT_human", 100, 200)     # retrieve a subsequence from the index
print(mp.revcomp(s))                # reverse complement

for name, seq, qual in mp.fastx_read("test/MT-orang.fa"):  # read a fasta/q sequence
    for hit in a.map(seq):  # traverse alignments
        print("{}\t{}\t{}\t{}".format(hit.ctg, hit.r_st, hit.r_en, hit.cigar_str))
```

## APIs

Mappluspy implements two classes and two global functions.

### Class `mappluspy.Aligner`

```python
mappluspy.Aligner(fn_idx_in=None, preset=None, ...)
```

This constructor accepts the following arguments:

- **fn_idx_in**: index or sequence file name. mm2-plus automatically tests the
  file type. If a sequence file is provided, mm2-plus builds an index. The
  sequence file can be optionally gzip'd. This option has no effect if **seq**
  is set.
- **seq**: a single sequence to index. The sequence name will be set to `N/A`.
- **preset**: minimap2/mm2-plus preset. Currently, mm2-plus supports the
  following presets: **sr** for single-end short reads; **map-pb** for PacBio
  read-to-reference mapping; **map-ont** for Oxford Nanopore read mapping;
  **splice** for long-read spliced alignment; **asm5** for
  assembly-to-assembly alignment; **asm10** for full genome alignment of
  closely related species. Note that the Python module does not support
  all-vs-all read overlapping.
- **k**: k-mer length, no larger than 28
- **w**: minimizer window size, no larger than 255
- **min_cnt**: minimum number of minimizers on a chain
- **min_chain_score**: minimum chaining score
- **bw**: chaining and alignment band width (initial chaining and extension)
- **bw_long**: chaining and alignment band width (RMQ-based rechaining and
  closing gaps)
- **best_n**: max number of alignments to return
- **n_threads**: number of indexing threads; 3 by default
- **extra_flags**: additional flags defined in minimap.h
- **fn_idx_out**: name of file to which the index is written. This parameter
  has no effect if **seq** is set.
- **scoring**: scoring system. It is a tuple/list consisting of 4, 6 or 7
  positive integers. The first 4 elements specify match scoring, mismatch
  penalty, gap open and gap extension penalty. The 5th and 6th elements, if
  present, set long-gap open and long-gap extension penalty. The 7th sets a
  mismatch penalty involving ambiguous bases.

```python
mappluspy.Aligner.map(seq, seq2=None, cs=False, MD=False)
```

This method aligns `seq` against the index. It is a generator, yielding a
series of `mappluspy.Alignment` objects. If `seq2` is present, mappluspy
performs paired-end alignment, assuming the two ends are in the FR orientation.
Alignments of the two ends can be distinguished by the `read_num` field (see
Class `mappluspy.Alignment` below). Argument `cs` asks mappluspy to generate the
`cs` tag; `MD` is similar. These two arguments might slightly degrade
performance and are not enabled by default.

```python
mappluspy.Aligner.seq(name, start=0, end=0x7fffffff)
```

This method retrieves a (sub)sequence from the index and returns it as a Python
string. `None` is returned if `name` is not present in the index or the
start/end coordinates are invalid.

```python
mappluspy.Aligner.seq_names
```

This property gives the array of sequence names in the index.

### Class `mappluspy.Alignment`

This class describes an alignment. An object of this class has the following
properties:

- **ctg**: name of the reference sequence the query is mapped to
- **ctg_len**: total length of the reference sequence
- **r_st** and **r_en**: start and end positions on the reference
- **q_st** and **q_en**: start and end positions on the query
- **strand**: +1 if on the forward strand; -1 if on the reverse strand
- **mapq**: mapping quality
- **blen**: length of the alignment, including both alignment matches and gaps
  but excluding ambiguous bases.
- **mlen**: length of the matching bases in the alignment, excluding ambiguous
  base matches.
- **NM**: number of mismatches, gaps and ambiguous positions in the alignment
- **trans_strand**: transcript strand. +1 if on the forward strand; -1 if on
  the reverse strand; 0 if unknown
- **is_primary**: if the alignment is primary (typically the best and the first
  to generate)
- **read_num**: read number that the alignment corresponds to; 1 for the first
  read and 2 for the second read
- **cigar_str**: CIGAR string
- **cigar**: CIGAR returned as an array of shape `(n_cigar,2)`. The two numbers
  give the length and the operator of each CIGAR operation.
- **MD**: the `MD` tag as in the SAM format. It is an empty string unless the
  `MD` argument is applied when calling `mappluspy.Aligner.map()`.
- **cs**: the `cs` tag.

An `Alignment` object can be converted to a string with `str()` in the
following format:

```text
q_st  q_en  strand  ctg  ctg_len  r_st  r_en  mlen  blen  mapq  cg:Z:cigar_str
```

It is effectively the PAF format without the QueryName and QueryLength columns
(the first two columns in PAF).

### Miscellaneous Functions

```python
mappluspy.fastx_read(fn, read_comment=False)
```

This generator function opens a FASTA/FASTQ file and yields a
`(name,seq,qual)` tuple for each sequence entry. The input file may be
optionally gzip'd. If `read_comment` is True, this generator yields a
`(name,seq,qual,comment)` tuple instead.

```python
mappluspy.revcomp(seq)
```

Return the reverse complement of DNA string `seq`. This function recognizes IUB
code and preserves the letter cases. Uracil `U` is complemented to `A`.
