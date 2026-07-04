try:
	from setuptools import setup, Extension
except ImportError:
	from distutils.core import setup
	from distutils.extension import Extension

import platform
import sys
from pathlib import Path

from setuptools.command.build_ext import build_ext

sys.path.append('python')

extra_compile_args = ['-DHAVE_KALLOC', '-DMM2_FAST', '-std=c++2a', '-w']
include_dirs = ['src', 'python']
libraries = ['z', 'm', 'pthread']
library_dirs = []

if Path('external/zlib/include').exists():
	include_dirs.append('external/zlib/include')
if Path('external/zlib/lib').exists():
	library_dirs.append('external/zlib/lib')

if platform.machine() in ['aarch64', 'arm64']:
	include_dirs.append('sse2neon')
	extra_compile_args.extend(['-ftree-vectorize', '-DKSW_SSE2_ONLY', '-D__SSE2__'])
else:
	extra_compile_args.append('-msse4.1')


def readme():
	with open('python/README.md') as f:
		return f.read()


sources = [
	'python/mappluspy.pyx',
	'python/mappluspy_globals.cpp',
	'src/align.c',
	'src/bseq.c',
	'src/lchain.c',
	'src/seed.c',
	'src/format.c',
	'src/hit.c',
	'src/index.c',
	'src/pe.c',
	'src/jump.c',
	'src/options.c',
	'src/ksw2_extd2_avx.c',
	'src/ksw2_extd2_sse.c',
	'src/ksw2_exts2_sse.c',
	'src/ksw2_extz2_sse.c',
	'src/ksw2_ll_sse.c',
	'src/kalloc.c',
	'src/kthread.c',
	'src/map.c',
	'src/misc.c',
	'src/sdust.c',
	'src/sketch.c',
	'src/esterr.c',
	'src/splitidx.c',
]


class build_ext_cxx(build_ext):
	def build_extensions(self):
		if hasattr(self.compiler, 'compiler_cxx'):
			cxx = self.compiler.compiler_cxx[0]
			self.compiler.compiler_so[0] = cxx
		if hasattr(self.compiler, 'linker_so') and hasattr(self.compiler, 'compiler_cxx'):
			cxx = self.compiler.compiler_cxx[0]
			self.compiler.linker_so[0] = cxx
		super().build_extensions()

depends = [
	'src/minimap.h',
	'src/bseq.h',
	'src/kalloc.h',
	'src/kdq.h',
	'src/khash.h',
	'src/kseq.h',
	'src/ksort.h',
	'src/ksw2.h',
	'src/kthread.h',
	'src/kvec.h',
	'src/mmpriv.h',
	'src/sdust.h',
	'src/IntervalTree.h',
	'src/parallel_chaining_v2_22.h',
	'python/cmappluspy.h',
	'python/cmappluspy.pxd',
]

setup(
	name='mappluspy',
	version='1.30.1',
	url='https://github.com/at-cg/mm2-plus',
	description='mm2-plus python binding',
	long_description=readme(),
	long_description_content_type='text/markdown',
	author='Ghanshyam Chandra',
	author_email='ghanshyam.chandra@intel.com',
	license='MIT',
	keywords='sequence-alignment',
	python_requires='>=3.8',
	scripts=['python/mm2plus.py'],
	ext_modules=[Extension(
		'mappluspy',
		sources=sources,
		depends=depends,
		extra_compile_args=extra_compile_args,
		include_dirs=include_dirs,
		library_dirs=library_dirs,
		libraries=libraries,
		language='c++',
	)],
	cmdclass={'build_ext': build_ext_cxx},
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX',
		'Programming Language :: C',
		'Programming Language :: Cython',
		'Programming Language :: Python :: 3',
		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering :: Bio-Informatics',
	],
	project_urls={
		'Source': 'https://github.com/at-cg/mm2-plus',
		'Issues': 'https://github.com/at-cg/mm2-plus/issues',
	},
	zip_safe=False,
)
