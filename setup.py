# Modified by Ghanshyam Chandra to use g++

try:
	from setuptools import setup, Extension
except ImportError:
	from distutils.core import setup
	from distutils.extension import Extension

import sys, platform
import os

os.environ["CC"] = "g++"

sys.path.append('python')

extra_compile_args = ['-DHAVE_KALLOC', '-std=c++2a']
include_dirs = ["src"]

if platform.machine() in ["aarch64", "arm64"]:
	include_dirs.append("sse2neon/")
	extra_compile_args.extend(['-ftree-vectorize', '-DKSW_SSE2_ONLY', '-D__SSE2__', '-DPAR_BTK -DPAR_SORT -DPAR_CHAIN_1 -DPAR_DP_CHAIN -DOPT_OLP -ljemalloc'])
else:
	extra_compile_args.append('-msse4.1')  # WARNING: ancient x86_64 CPUs don't have SSE4

def readme():
	with open('python/README.rst') as f:
		return f.read()

setup(
	name='mappy',
	version='2.28',
	url='https://github.com/lh3/minimap2',
	description='Minimap2 python binding',
	long_description=readme(),
	author='Heng Li',
	author_email='lh3@me.com',
	license='MIT',
	keywords='sequence-alignment',
	scripts=['python/minimap2.py'],
	ext_modules=[Extension('mappy',
		sources=['python/mappy.pyx', 'src/align.c', 'src/bseq.c', 'src/lchain.c', 'src/seed.c', 'src/format.c', 'src/hit.c', 'src/index.c',
				 'src/pe.c', 'src/options.c', 'src/ksw2_extd2_sse.c', 'src/ksw2_exts2_sse.c', 'src/ksw2_extz2_sse.c', 'src/ksw2_ll_sse.c',
				 'src/kalloc.c', 'src/kthread.c', 'src/map.c', 'src/misc.c', 'src/sdust.c', 'src/sketch.c', 'src/esterr.c', 'src/splitidx.c'],
		depends=['src/minimap.h', 'src/bseq.h', 'src/kalloc.h', 'src/kdq.h', 'src/khash.h', 'src/kseq.h', 'src/ksort.h',
				 'src/ksw2.h', 'src/kthread.h', 'src/kvec.h', 'src/mmpriv.h', 'src/sdust.h',
				 'python/cmappy.h', 'python/cmappy.pxd'],
		extra_compile_args=extra_compile_args,
		include_dirs=include_dirs,
		libraries=['z', 'm', 'pthread'],
		language='c++',
		# Specify 'g++' for compilation
		compiler_directives={'language': 'c++'})],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX',
		'Programming Language :: C++',
		'Programming Language :: Cython',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering :: Bio-Informatics'],
	setup_requires=["cython"])
