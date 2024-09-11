CPPFLAGS=	-g -std=c++2a -march=native -O3 -w -DHAVE_KALLOC -fopenmp
INCLUDES=
OBJS=		src/kthread.o src/kalloc.o src/misc.o src/bseq.o src/sketch.o src/sdust.o src/options.o src/index.o \
			src/lchain.o src/align.o src/hit.o src/seed.o src/map.o src/format.o src/pe.o src/esterr.o src/splitidx.o \
			src/ksw2_ll_sse.o src/parallel_sort.o
PROG=		minimap2
PROG_EXTRA=	sdust minimap2-lite
LIBS=		-lm -lz -lpthread

ifeq ($(profile),1)
	CPPFLAGS+=-DPROFILE
endif

ifeq ($(par_dp_chain),1)
	CPPFLAGS+=-DPAR_DP_CHAIN
endif

ifeq ($(opt_olp),1)
	CPPFLAGS+=-DOPT_OLP
endif

ifeq ($(par_sort),1)
	CPPFLAGS+=-DPAR_SORT
endif

ifeq ($(par_btk),1)
	CPPFLAGS+=-DPAR_BTK
endif

ifeq ($(par_chain_1),1)
	CPPFLAGS+=-DPAR_CHAIN_1 -ljemalloc
endif

ifeq ($(par_chain_2),1)
	CPPFLAGS+=-DPAR_CHAIN_2 -ljemalloc
endif

ifeq ($(get_dist),1)
	CPPFLAGS+=-DGET_DIST -DPAR_CHAIN_1 -ljemalloc
endif

ifeq ($(all),1)
	CPPFLAGS+=-DPAR_BTK -DPAR_SORT -DPAR_CHAIN_1 -DPAR_DP_CHAIN -DOPT_OLP -ljemalloc
	avx=1
endif

ifneq ($(aarch64),)
	arm_neon=1
endif

ifeq ($(arm_neon),) # if arm_neon is not defined
ifeq ($(sse2only),) # if sse2only is not defined
	ifeq ($(avx),1)
		CPPFLAGS+=-DALIGN_AVX -DAPPLY_AVX2
	endif
	OBJS+=src/ksw2_extz2_sse41.o src/ksw2_extd2_sse41.o src/ksw2_exts2_sse41.o src/ksw2_extz2_sse2.o src/ksw2_extd2_sse2.o src/ksw2_exts2_sse2.o src/ksw2_dispatch.o src/ksw2_extd2_avx.o
else                # if sse2only is defined
	OBJS+=src/ksw2_extz2_sse.o src/ksw2_extd2_sse.o src/ksw2_exts2_sse.o
endif
else				# if arm_neon is defined
	OBJS+=src/ksw2_extz2_neon.o src/ksw2_extd2_neon.o src/ksw2_exts2_neon.o
    INCLUDES+=-Isse2neon
ifeq ($(aarch64),)	#if aarch64 is not defined
	CPPFLAGS+=-D_FILE_OFFSET_BITS=64 -mfpu=neon -fsigned-char
else				#if aarch64 is defined
	CPPFLAGS+=-D_FILE_OFFSET_BITS=64 -fsigned-char
endif
endif

ifneq ($(asan),)
	CPPFLAGS+=-fsanitize=address
	LIBS+=-fsanitize=address -ldl
endif

ifneq ($(tsan),)
	CPPFLAGS+=-fsanitize=thread
	LIBS+=-fsanitize=thread -ldl
endif

.PHONY:all extra clean depend
.SUFFIXES:.c .o

.c.o:
		$(CXX) -c $(CPPFLAGS) $(INCLUDES) $< -o $@

all:$(PROG)

extra:all $(PROG_EXTRA)

minimap2:src/main.o libminimap2.a
		$(CXX) $(CPPFLAGS) src/main.o -o $@ -L. -lminimap2 $(LIBS)

minimap2-lite:src/example.o libminimap2.a
		$(CXX) $(CPPFLAGS) $< -o $@ -L. -lminimap2 $(LIBS)

libminimap2.a:$(OBJS)
		$(AR) -csru $@ $(OBJS)

sdust:src/sdust.c src/kalloc.o src/kalloc.h src/kdq.h src/kvec.h src/kseq.h src/ketopt.h src/sdust.h
		$(CXX) -D_SDUST_MAIN $(CPPFLAGS) $< src/kalloc.o -o $@ -lz

# SSE-specific targets on x86/x86_64

ifeq ($(arm_neon),)   # if arm_neon is defined, compile this target with the default setting (i.e. no -msse2)
src/ksw2_ll_sse.o:src/ksw2_ll_sse.c src/ksw2.h src/kalloc.h
		$(CXX) -c $(CPPFLAGS) -msse2 $(INCLUDES) $< -o $@
endif

src/ksw2_extz2_sse41.o:src/ksw2_extz2_sse.c src/ksw2.h src/kalloc.h
		$(CXX) -c $(CPPFLAGS) -msse4.1 -DKSW_CPU_DISPATCH $(INCLUDES) $< -o $@

src/ksw2_extz2_sse2.o:src/ksw2_extz2_sse.c src/ksw2.h src/kalloc.h
		$(CXX) -c $(CPPFLAGS) -msse2 -mno-sse4.1 -DKSW_CPU_DISPATCH -DKSW_SSE2_ONLY $(INCLUDES) $< -o $@

src/ksw2_extd2_sse41.o:src/ksw2_extd2_sse.c src/ksw2.h src/kalloc.h
		$(CXX) -c $(CPPFLAGS) -msse4.1 -DKSW_CPU_DISPATCH $(INCLUDES) $< -o $@

src/ksw2_extd2_sse2.o:src/ksw2_extd2_sse.c src/ksw2.h src/kalloc.h
		$(CXX) -c $(CPPFLAGS) -msse2 -mno-sse4.1 -DKSW_CPU_DISPATCH -DKSW_SSE2_ONLY $(INCLUDES) $< -o $@

src/ksw2_exts2_sse41.o:src/ksw2_exts2_sse.c src/ksw2.h src/kalloc.h
		$(CXX) -c $(CPPFLAGS) -msse4.1 -DKSW_CPU_DISPATCH $(INCLUDES) $< -o $@

src/ksw2_exts2_sse2.o:src/ksw2_exts2_sse.c src/ksw2.h src/kalloc.h
		$(CXX) -c $(CPPFLAGS) -msse2 -mno-sse4.1 -DKSW_CPU_DISPATCH -DKSW_SSE2_ONLY $(INCLUDES) $< -o $@

src/ksw2_dispatch.o:src/ksw2_dispatch.c src/ksw2.h
		$(CXX) -c $(CPPFLAGS) -msse4.1 -DKSW_CPU_DISPATCH $(INCLUDES) $< -o $@

# NEON-specific targets on ARM

src/ksw2_extz2_neon.o:src/ksw2_extz2_sse.c src/ksw2.h src/kalloc.h
		$(CXX) -c $(CPPFLAGS) -DKSW_SSE2_ONLY -D__SSE2__ $(INCLUDES) $< -o $@

src/ksw2_extd2_neon.o:src/ksw2_extd2_sse.c src/ksw2.h src/kalloc.h
		$(CXX) -c $(CPPFLAGS) -DKSW_SSE2_ONLY -D__SSE2__ $(INCLUDES) $< -o $@

src/ksw2_exts2_neon.o:src/ksw2_exts2_sse.c src/ksw2.h src/kalloc.h
		$(CXX) -c $(CPPFLAGS) -DKSW_SSE2_ONLY -D__SSE2__ $(INCLUDES) $< -o $@

# other non-file targets

clean:
		rm -fr gmon.out src/*.o a.out $(PROG) $(PROG_EXTRA) *~ *.a *.dSYM build dist mappy*.so mappy.c python/mappy.c mappy.egg*

depend:
		(LC_ALL=C; export LC_ALL; makedepend -Y -- $(CPPFLAGS) -- src/*.c)

# DO NOT DELETE

src/align.o: src/minimap.h src/mmpriv.h src/bseq.h src/kseq.h src/ksw2.h src/kalloc.h src/ksw2_extd2_avx.h
src/bseq.o: src/bseq.h src/kvec.h src/kalloc.h src/kseq.h
src/esterr.o: src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h
src/example.o: src/minimap.h src/kseq.h
src/format.o: src/kalloc.h src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h
src/hit.o: src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h src/kalloc.h src/khash.h src/IntervalTree.h
src/index.o: src/kthread.h src/bseq.h src/minimap.h src/mmpriv.h src/kseq.h src/kvec.h src/kalloc.h src/khash.h
src/index.o: src/ksort.h
src/kalloc.o: src/kalloc.h
src/ksw2_extd2_sse.o: src/ksw2.h src/kalloc.h
src/ksw2_exts2_sse.o: src/ksw2.h src/kalloc.h
src/ksw2_extz2_sse.o: src/ksw2.h src/kalloc.h
src/ksw2_ll_sse.o: src/ksw2.h src/kalloc.h
src/kthread.o: src/kthread.h
src/lchain.o: src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h src/kalloc.h src/krmq.h
src/main.o: src/bseq.h src/minimap.h src/mmpriv.h src/kseq.h src/ketopt.h
src/map.o: src/kthread.h src/kvec.h src/kalloc.h src/sdust.h src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h
src/map.o: src/khash.h src/ksort.h
src/misc.o: src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h src/ksort.h
src/options.o: src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h
src/pe.o: src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h src/kvec.h src/kalloc.h src/ksort.h
src/sdust.o: src/kalloc.h src/kdq.h src/kvec.h src/sdust.h
src/seed.o: src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h src/kalloc.h src/ksort.h
src/sketch.o: src/kvec.h src/kalloc.h src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h
src/splitidx.o: src/mmpriv.h src/minimap.h src/bseq.h src/kseq.h