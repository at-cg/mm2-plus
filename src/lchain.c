#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include "mmpriv.h"
#include "kalloc.h"
#include "krmq.h"
#include <stdbool.h>
#include <omp.h>
// CPP
#include <chrono>	// for timing	
#include <iostream>
#include <vector>
#include <algorithm>
#include <cassert>
#include <future>
#include <map>
#include <cstring>

#if defined(__x86_64__) || defined(_M_X64) || defined(__i386) || defined(_M_IX86)
    #include <immintrin.h>  // Include this header only for x86 architectures
	#include "parallel_chaining_v2_22.h"
#endif

extern float mean_itr_1_, mean_itr_2_;
extern int32_t max_itr_1, max_itr_2;
extern int32_t num_threads_b2b;
extern float rmq_1_time_, rmq_2_time_, btk_1_time_, btk_2_time_;
extern int32_t count_stages, is_g2g_aln;
extern std::fstream anchor_dist_file;

static int64_t mg_chain_bk_end_par(const int32_t max_drop, const std::vector<mm128_t> &z, const int32_t *f, std::pair<int64_t, int32_t> *p_t_vec, const int64_t k_, const int64_t k)
{
	int64_t i = k_, end_i = -1, max_i = i;
	int32_t max_s = 0;
	if (i < 0 || p_t_vec[i].second != 0) return i;
	do {
		int32_t s = 0;
		p_t_vec[i].second = 2;
		end_i = i = p_t_vec[i].first;
		s = i < 0? z[k].x : (int32_t)z[k].x - f[i];
		if (__builtin_expect(s > max_s, 1)) {  // This is the most time-consuming part of the code
            max_s = s;
            max_i = i;
        } else if (__builtin_expect(max_s - s > max_drop, 0)) {
            break;
        }
	} while (i >= 0 && p_t_vec[i].second == 0);
	for (i = k_; i >= 0 && i != end_i; i = p_t_vec[i].first) // reset modified t[]
		p_t_vec[i].second = 0;
	return max_i;
}

static int64_t mg_chain_bk_end(int32_t max_drop, const mm128_t *z, const int32_t *f, const int64_t *p, int32_t *t, int64_t k)
{
	int64_t i = z[k].y, end_i = -1, max_i = i;
	int32_t max_s = 0;
	if (i < 0 || t[i] != 0) return i;
	do {
		int32_t s;
		t[i] = 2;
		end_i = i = p[i];
		s = i < 0? z[k].x : (int32_t)z[k].x - f[i];
		if (s > max_s) max_s = s, max_i = i;
		else if (max_s - s > max_drop) break;
	} while (i >= 0 && t[i] == 0);
	for (i = z[k].y; i >= 0 && i != end_i; i = p[i]) // reset modified t[]
		t[i] = 0;
	return max_i;
}

uint64_t *mg_chain_backtrack(void *km, int64_t n, int32_t *f, int64_t *p, int32_t *v, int32_t *t, int32_t min_cnt, int32_t min_sc, int32_t max_drop, int32_t *n_u_, int32_t *n_v_)
{
	mm128_t *z;
	uint64_t *u;
	int64_t i, k, n_z, n_v;
	int32_t n_u;

	*n_u_ = *n_v_ = 0;
	for (i = 0, n_z = 0; i < n; ++i) // precompute n_z
		if (f[i] >= min_sc) ++n_z;
	if (n_z == 0) return 0;
	z = Kmalloc(km, mm128_t, n_z);
	for (i = 0, k = 0; i < n; ++i) // populate z[]
		if (f[i] >= min_sc) z[k].x = f[i], z[k++].y = i;
	radix_sort_128x(z, z + n_z);

	memset(t, 0, n * 4);
	for (k = n_z - 1, n_v = n_u = 0; k >= 0; --k) { // precompute n_u
		if (t[z[k].y] == 0) {
			int64_t n_v0 = n_v, end_i;
			int32_t sc;
			end_i = mg_chain_bk_end(max_drop, z, f, p, t, k);
			for (i = z[k].y; i != end_i; i = p[i])
				++n_v, t[i] = 1;
			sc = i < 0? z[k].x : (int32_t)z[k].x - f[i];
			if (sc >= min_sc && n_v > n_v0 && n_v - n_v0 >= min_cnt)
				++n_u;
			else n_v = n_v0;
		}
	}
	u = Kmalloc(km, uint64_t, n_u);
	memset(t, 0, n * 4);
	for (k = n_z - 1, n_v = n_u = 0; k >= 0; --k) { // populate u[]
		if (t[z[k].y] == 0) {
			int64_t n_v0 = n_v, end_i;
			int32_t sc;
			end_i = mg_chain_bk_end(max_drop, z, f, p, t, k);
			for (i = z[k].y; i != end_i; i = p[i])
				v[n_v++] = i, t[i] = 1;
			sc = i < 0? z[k].x : (int32_t)z[k].x - f[i];
			if (sc >= min_sc && n_v > n_v0 && n_v - n_v0 >= min_cnt)
				u[n_u++] = (uint64_t)sc << 32 | (n_v - n_v0);
			else n_v = n_v0;
		}
	}
	kfree(km, z);
	// free f p t in case of parallel chaining
	if (is_g2g_aln)
	{
		#if defined(PAR_CHAIN_1) || defined(PAR_CHAIN_2)
			free(f); free(p); free(t);
		#endif
	}

	assert(n_v < INT32_MAX);
	*n_u_ = n_u, *n_v_ = n_v;
	return u;
}

// Parallel backtracking
uint64_t *mg_chain_backtrack_par(void *km, int64_t n, int32_t *f, int64_t *p, int32_t *v, int32_t *t, int32_t min_cnt, int32_t min_sc, int32_t max_drop, int32_t *n_u_, int32_t *n_v_, const mm128_t *a)
{
	mm128_t *z;
	uint64_t *u;
	int64_t i, k, n_z, n_v;
	int32_t n_u;
	if (is_g2g_aln)
	{
		#if defined(PAR_CHAIN_1) || defined(PAR_CHAIN_2)
			free(t);
		#endif
	}

	auto future = std::async(std::launch::async, [&](){
		std::pair<int64_t, int32_t> *p_t_vec = (std::pair<int64_t, int32_t>*)malloc(n * sizeof(std::pair<int64_t, int32_t>));
		#pragma omp parallel for num_threads(num_threads_b2b) // no need to schedule dynamic
		for (int64_t i = 0; i < n; i++)
		{
			p_t_vec[i] = std::make_pair(p[i], 0);
		}
		return p_t_vec;
	});
	
	*n_u_ = *n_v_ = 0;

	int32_t num_chr = 1; // number of chromosomes
	for (i = 1; i < n; i++)
	{
		if (a[i-1].x>>32 != a[i].x>>32) num_chr++;
	}
	std::vector<int64_t> st_vec(num_chr, 0);
	std::vector<int64_t> end_vec(num_chr, 0);
	int32_t chrom_id = 0;
	if (n > 0) {
		st_vec[0] = 0; // Initialize the start of the first chromosome
		for (i = 1; i < n; i++)
		{
			if (a[i-1].x >> 32 != a[i].x >> 32) // Check for a new chromosome
			{
				end_vec[chrom_id] = i - 1; // Set end for the current chromosome
				chrom_id++; // Move to the next chromosome
				st_vec[chrom_id] = i; // Start index for the new chromosome
			}
		}
		end_vec[chrom_id] = n - 1; // Set end for the last chromosome
	}

	// Handle the case where num_chr is 1
	if (num_chr == 1) {st_vec[0] = 0; end_vec[0] = n - 1;}

	int32_t n_u_global = 0;
	int64_t n_v_global = 0;
	// backtracking
	std::vector<int32_t> v_vec_global;
	std::vector<uint64_t> u_vec_global;

	std::pair<int64_t, int32_t> *p_t_vec = future.get();
	if (is_g2g_aln)
	{
		#if defined(PAR_CHAIN_1) || defined(PAR_CHAIN_2)
			free(p);
		#endif
	}


	#pragma omp parallel for num_threads(num_threads_b2b) reduction(+:n_u_global, n_v_global) ordered schedule(static,1)
	for (int32_t thd = 0; thd < num_chr; thd++)
	{
		int64_t n_z = 0;
		int64_t i = 0;
		int64_t k;
		std::vector<mm128_t> z;

		for (i = st_vec[thd]; i <= end_vec[thd]; ++i)
		{
			if (f[i] >= min_sc)
			{
				mm128_t temp;
				temp.x = f[i];
				temp.y = i;
				z.push_back(temp);
			}
		}
		n_z = z.size();

		if (is_g2g_aln)
		{
			#if defined(PAR_SORT) 
				parallel_sort(z.data(), n_z, num_threads_b2b);
			#else
				radix_sort_128x(z.data(), z.data() + n_z);
			#endif
		}else
		{
			radix_sort_128x(z.data(), z.data() + n_z);
		}
		
		// backtracking
		std::vector<int32_t> v_vec;
		std::vector<uint64_t> u_vec;
		int64_t n_v = 0;
		int32_t n_u = 0;
		#if defined(__x86_64__) || defined(_M_X64) || defined(__i386) || defined(_M_IX86)
			int64_t prefetch_dist = 16; // Larger prefetch distance causes cache pollution due to parallelism
		#endif
		for (k = n_z - 1; k >= 0; --k) 
		{ // precompute n_u
			#if defined(__x86_64__) || defined(_M_X64) || defined(__i386) || defined(_M_IX86)
				if (k - prefetch_dist >=0 ) _mm_prefetch(reinterpret_cast<const char*>(&p_t_vec[z[k - prefetch_dist].y].second), _MM_HINT_T0); // Asynchronous prefetching
			#endif
			if (p_t_vec[z[k].y].second == 0) {
				int64_t n_v0 = n_v, end_i;
				int32_t sc;
				end_i = mg_chain_bk_end_par(max_drop, z, f, p_t_vec, z[k].y, k);
				for (i = z[k].y; i != end_i; i = p_t_vec[i].first)
				{
					++n_v; v_vec.push_back(i); p_t_vec[i].second = 1;
				}
				sc = i < 0? z[k].x : (int32_t)z[k].x - f[i];
				if (sc >= min_sc && n_v > n_v0 && n_v - n_v0 >= min_cnt)
				{
					++n_u; u_vec.push_back((uint64_t)sc << 32 | (n_v - n_v0));
				}
				else {
					for (int64_t j = 0; j < (n_v - n_v0); j++) v_vec.pop_back(); n_v = n_v0;
				}
			}
		}

		// sum n_u and n_v to global variables
		#pragma omp atomic
		n_u_global += n_u;
		#pragma omp atomic
		n_v_global += n_v;

		// push u_vec to u and v_vec to v
		#pragma omp ordered // maintains thd order
		{
			v_vec_global.insert(v_vec_global.end(), v_vec.begin(), v_vec.end()); v_vec.clear();
			u_vec_global.insert(u_vec_global.end(), u_vec.begin(), u_vec.end()); u_vec.clear();
		}
	}

	n_u = n_u_global; n_v = n_v_global;
	assert(v_vec_global.size() == n_v);
	assert(u_vec_global.size() == n_u);

	free(p_t_vec);
	if (is_g2g_aln)
	{
		#if defined(PAR_CHAIN_1) || defined(PAR_CHAIN_2)
			free(f);
		#endif
	}
	// push u_vec to u and v_vec to v
	memcpy(v, v_vec_global.data(), n_v * sizeof(int32_t)); v_vec_global.clear();
	u = Kmalloc(km, uint64_t, n_u);
	memcpy(u, u_vec_global.data(), n_u * sizeof(uint64_t)); u_vec_global.clear();
	st_vec.clear(); end_vec.clear();

	assert(n_v < INT32_MAX);
	*n_u_ = n_u, *n_v_ = n_v;
	return u;
}

static mm128_t *compact_a(void *km, int32_t n_u, uint64_t *u, int32_t n_v, int32_t *v, mm128_t *a)
{
	mm128_t *b, *w;
	uint64_t *u2;
	int64_t i, j, k;

	// write the results to b[]
	if (is_g2g_aln)
	{
		b = Kmalloc(km, mm128_t, n_v);
		#if defined(__x86_64__) || defined(_M_X64) || defined(__i386) || defined(_M_IX86)
			const int64_t PREF_DIST = 64;
		#endif
		for (i = 0, k = 0; i < n_u; ++i) {
			int32_t k0 = k, ni = (int32_t)u[i];
			for (j = 0; j < ni; ++j)
			{
				int64_t idx = k0 + (ni - j - 1);
				#if defined(__x86_64__) || defined(_M_X64) || defined(__i386) || defined(_M_IX86)
					int64_t PREF_idx = idx - PREF_DIST;
					if (PREF_idx >= 0 && PREF_idx >= (k0 + ni - 1)) _mm_prefetch(reinterpret_cast<const char*>(&a[v[idx - PREF_DIST]]), _MM_HINT_T0); // Asynchronous prefetching
				#endif
				b[k++] = a[v[idx]];
			}
		}
		#if defined(PAR_CHAIN_1) || defined(PAR_CHAIN_2)
			free(v);
		#else
			kfree(km, v);
		#endif
	}else
	{
		// write the result to b[]
		b = Kmalloc(km, mm128_t, n_v);
		for (i = 0, k = 0; i < n_u; ++i) {
			int32_t k0 = k, ni = (int32_t)u[i];
			for (j = 0; j < ni; ++j)
				b[k++] = a[v[k0 + (ni - j - 1)]];
		}
		kfree(km, v);
	}

	// sort u[] and a[] by the target position, such that adjacent chains may be joined
	w = Kmalloc(km, mm128_t, n_u);
	for (i = k = 0; i < n_u; ++i) { // This is linear time
		w[i].x = b[k].x, w[i].y = (uint64_t)k<<32|i;
		k += (int32_t)u[i];
	}

	if (is_g2g_aln)
	{
		#if defined(PAR_SORT) 
			parallel_sort(w, n_u, num_threads_b2b);
		#else
			radix_sort_128x(w, w + n_u);
		#endif
	}else
	{
		radix_sort_128x(w, w + n_u);
	}

	u2 = Kmalloc(km, uint64_t, n_u);
	for (i = k = 0; i < n_u; ++i) {
		int32_t j = (int32_t)w[i].y, n = (int32_t)u[j];
		u2[i] = u[j];
		memcpy(&a[k], &b[w[i].y>>32], n * sizeof(mm128_t));
		k += n;
	}
	memcpy(u, u2, n_u * 8);
	memcpy(b, a, k * sizeof(mm128_t)); // write _a_ to _b_ and deallocate _a_ because _a_ is oversized, sometimes a lot
	kfree(km, a); kfree(km, w); kfree(km, u2);
	return b;
}

static inline int32_t comput_sc(const mm128_t *ai, const mm128_t *aj, int32_t max_dist_x, int32_t max_dist_y, int32_t bw, float chn_pen_gap, float chn_pen_skip, int is_cdna, int n_seg)
{
	int32_t dq = (int32_t)ai->y - (int32_t)aj->y, dr, dd, dg, q_span, sc;
	int32_t sidi = (ai->y & MM_SEED_SEG_MASK) >> MM_SEED_SEG_SHIFT;
	int32_t sidj = (aj->y & MM_SEED_SEG_MASK) >> MM_SEED_SEG_SHIFT;
	if (dq <= 0 || dq > max_dist_x) return INT32_MIN;
	dr = (int32_t)(ai->x - aj->x);
	if (sidi == sidj && (dr == 0 || dq > max_dist_y)) return INT32_MIN;
	dd = dr > dq? dr - dq : dq - dr;
	if (sidi == sidj && dd > bw) return INT32_MIN;
	if (n_seg > 1 && !is_cdna && sidi == sidj && dr > max_dist_y) return INT32_MIN;
	dg = dr < dq? dr : dq;
	q_span = aj->y>>32&0xff;
	sc = q_span < dg? q_span : dg;
	if (dd || dg > q_span) {
		float lin_pen, log_pen;
		lin_pen = chn_pen_gap * (float)dd + chn_pen_skip * (float)dg;
		log_pen = dd >= 1? mg_log2(dd + 1) : 0.0f; // mg_log2() only works for dd>=2
		if (is_cdna || sidi != sidj) {
			if (sidi != sidj && dr == 0) ++sc; // possibly due to overlapping paired ends; give a minor bonus
			else if (dr > dq || sidi != sidj) sc -= (int)(lin_pen < log_pen? lin_pen : log_pen); // deletion or jump between paired ends
			else sc -= (int)(lin_pen + .5f * log_pen);
		} else sc -= (int)(lin_pen + .5f * log_pen);
	}
	return sc;
}

/* Input:
 *   a[].x: rev<<63 | tid<<32 | tpos
 *   a[].y: flags<<40 | q_span<<32 | q_pos
 * Output:
 *   n_u: #chains
 *   u[]: score<<32 | #anchors (sum of lower 32 bits of u[] is the returned length of a[])
 * input a[] is deallocated on return
 */


mm128_t *mg_lchain_dp(int max_dist_x, int max_dist_y, int bw, int max_skip, int max_iter, int min_cnt, int min_sc, float chn_pen_gap, float chn_pen_skip,
					  int is_cdna, int n_seg, int64_t n, mm128_t *a, int *n_u_, uint64_t **_u, void *km)
{ // TODO: make sure this works when n has more than 32 bits
	int32_t *f, *t, *v, n_u, n_v, mmax_f = 0, max_drop = bw;
	int64_t *p, i, j, max_ii, st = 0;
	uint64_t *u;

	if (_u) *_u = 0, *n_u_ = 0;
	if (n == 0 || a == 0) {
		kfree(km, a);
		return 0;
	}
	if (max_dist_x < bw) max_dist_x = bw;
	if (max_dist_y < bw && !is_cdna) max_dist_y = bw;
	if (is_cdna) max_drop = INT32_MAX;
	p = Kmalloc(km, int64_t, n);
	f = Kmalloc(km, int32_t, n);
	v = Kmalloc(km, int32_t, n);
	t = Kcalloc(km, int32_t, n);

	#if defined(PAR_DP_CHAIN) && (defined(__AVX512BW__) || defined(__AVX2__))
			int32_t *v_1, *p_1;
			uint32_t *f_1;
			v_1 = Kmalloc(km, int32_t, n);
			p_1 = Kmalloc(km, int32_t, n);
			f_1 = Kmalloc(km, uint32_t, n);
			// Parallel chaining data-structures
			anchor_t* anchors = (anchor_t*)malloc(n* sizeof(anchor_t));
			for (i = 0; i < n; ++i) {
				uint64_t ri = a[i].x;
				int32_t qi = (int32_t)a[i].y, q_span = a[i].y>>32&0xff; // NB: only 8 bits of span is used!!!
				anchors[i].r = ri;
				anchors[i].q = qi;
				anchors[i].l = q_span;
			}
			num_bits_t *anchor_r, *anchor_q, *anchor_l;
			create_SoA_Anchors_32_bit(anchors, n, anchor_r, anchor_q, anchor_l);
			dp_chain obj(max_dist_x, max_dist_y, bw, max_skip, max_iter, min_cnt, min_sc, chn_pen_gap, chn_pen_skip, is_cdna, n_seg);
			obj.mm_dp_vectorized(n, &anchors[0], anchor_r, anchor_q, anchor_l, f_1, p_1, v_1, max_dist_x, max_dist_y, NULL, NULL);
			// -16 is due to extra padding at the start of arrays
			anchor_r -= 16; anchor_q -= 16; anchor_l -= 16;
			free(anchor_r); 
			free(anchor_q); 
			free(anchor_l);
			free(anchors);

			// copy the results
			for(i = 0; i < n; i++)
			{
				f[i] = f_1[i];
				p[i] = p_1[i];
				v[i] = v_1[i];
			}
			kfree(km, p_1); kfree(km, f_1); kfree(km, v_1);
	#else
		// fill the score and backtrack arrays
		for (i = 0, max_ii = -1; i < n; ++i) {
			int64_t max_j = -1, end_j;
			int32_t max_f = a[i].y>>32&0xff, n_skip = 0;
			while (st < i && (a[i].x>>32 != a[st].x>>32 || a[i].x > a[st].x + max_dist_x)) ++st;
			if (i - st > max_iter) st = i - max_iter;
			for (j = i - 1; j >= st; --j) {
				int32_t sc;
				sc = comput_sc(&a[i], &a[j], max_dist_x, max_dist_y, bw, chn_pen_gap, chn_pen_skip, is_cdna, n_seg);
				if (sc == INT32_MIN) continue;
				sc += f[j];
				if (sc > max_f) {
					max_f = sc, max_j = j;
					if (n_skip > 0) --n_skip;
				} else if (t[j] == (int32_t)i) {
					if (++n_skip > max_skip)
						break;
				}
				if (p[j] >= 0) t[p[j]] = i;
			}
			end_j = j;
			if (max_ii < 0 || a[i].x - a[max_ii].x > (int64_t)max_dist_x) {
				int32_t max = INT32_MIN;
				max_ii = -1;
				for (j = i - 1; j >= st; --j)
					if (max < f[j]) max = f[j], max_ii = j;
			}
			if (max_ii >= 0 && max_ii < end_j) {
				int32_t tmp;
				tmp = comput_sc(&a[i], &a[max_ii], max_dist_x, max_dist_y, bw, chn_pen_gap, chn_pen_skip, is_cdna, n_seg);
				if (tmp != INT32_MIN && max_f < tmp + f[max_ii])
					max_f = tmp + f[max_ii], max_j = max_ii;
			}
			f[i] = max_f, p[i] = max_j;
			v[i] = max_j >= 0 && v[max_j] > max_f? v[max_j] : max_f; // v[] keeps the peak score up to i; f[] is the score ending at i, not always the peak
			if (max_ii < 0 || (a[i].x - a[max_ii].x <= (int64_t)max_dist_x && f[max_ii] < f[i]))
				max_ii = i;
			if (mmax_f < max_f) mmax_f = max_f;
			//fprintf(stderr, "X1\t%ld\t%ld:%d\t%ld\t%ld:%d\t%ld\t%ld\n", (long)i, (long)(a[i].x>>32), (int32_t)a[i].x, (long)max_j, max_j<0?-1L:(long)(a[max_j].x>>32), max_j<0?-1:(int32_t)a[max_j].x, (long)max_f, (long)v[i]);
		}
	#endif

	u = mg_chain_backtrack(km, n, f, p, v, t, min_cnt, min_sc, max_drop, &n_u, &n_v);
	*n_u_ = n_u, *_u = u; // NB: note that u[] may not be sorted by score here
	kfree(km, p); kfree(km, f); kfree(km, t);
	if (n_u == 0) {
		kfree(km, a); kfree(km, v);
		return 0;
	}
	return compact_a(km, n_u, u, n_v, v, a);
}

typedef struct lc_elem_s {
	int32_t y;
	int64_t i;
	double pri;
	KRMQ_HEAD(struct lc_elem_s) head;
} lc_elem_t;

#define lc_elem_cmp(a, b) ((a)->y < (b)->y? -1 : (a)->y > (b)->y? 1 : ((a)->i > (b)->i) - ((a)->i < (b)->i))
#define lc_elem_lt2(a, b) ((a)->pri < (b)->pri)
KRMQ_INIT(lc_elem, lc_elem_t, head, lc_elem_cmp, lc_elem_lt2)

KALLOC_POOL_INIT(rmq, lc_elem_t)

static inline int32_t comput_sc_simple(const mm128_t *ai, const mm128_t *aj, float chn_pen_gap, float chn_pen_skip, int32_t *exact, int32_t *width)
{
	int32_t dq = (int32_t)ai->y - (int32_t)aj->y, dr, dd, dg, q_span, sc;
	dr = (int32_t)(ai->x - aj->x);
	*width = dd = dr > dq? dr - dq : dq - dr;
	dg = dr < dq? dr : dq;
	q_span = aj->y>>32&0xff;
	sc = q_span < dg? q_span : dg;
	if (exact) *exact = (dd == 0 && dg <= q_span);
	if (dd || dq > q_span) {
		float lin_pen, log_pen;
		lin_pen = chn_pen_gap * (float)dd + chn_pen_skip * (float)dg;
		log_pen = dd >= 1? mg_log2(dd + 1) : 0.0f; // mg_log2() only works for dd>=2
		sc -= (int)(lin_pen + .5f * log_pen);
	}
	return sc;
}

mm128_t *mg_lchain_rmq_opt(int max_dist, int max_dist_inner, int bw, int max_chn_skip, int cap_rmq_size, int min_cnt, int min_sc, float chn_pen_gap, float chn_pen_skip,
					   int64_t n, mm128_t *a, int *n_u_, uint64_t **_u, void *km, int32_t num_threads)
{
	struct timeval start_chain, end_chain;
	if (is_g2g_aln)
	{
		#ifdef PROFILE
			gettimeofday(&start_chain, NULL);
		#endif
	}
	#if defined(PAR_CHAIN_2) 
		int32_t *f, *t, *v, n_u, n_v, mmax_f = 0, max_rmq_size = 0, max_drop = bw;
		int64_t *p;
		uint64_t *u;
		int64_t i, k, n_z, j;

		if (_u) *_u = 0, *n_u_ = 0;
		if (n == 0 || a == 0) {
			kfree(km, a);
			return 0;
		}

		if (max_dist < bw) max_dist = bw;
		if (max_dist_inner <= 0 || max_dist_inner >= max_dist) max_dist_inner = 0;
		p = (int64_t*)malloc(n * sizeof(int64_t));
		f = (int32_t*)malloc(n * sizeof(int32_t));
		v = (int32_t*)malloc(n * sizeof(int32_t));
		t = (int32_t*)malloc(n * sizeof(int32_t));

		// parallel initialisation
		#pragma omp parallel for num_threads(num_threads) private(i) // No need to schedule dynamic
		for (i = 0; i < n; i++)
		{
			p[i] = -1; f[i] = 0; v[i] = 0; t[i] = 0;
		}

		// chunk size for each thread
		int64_t chunk_size = n/num_threads;
		/* Note: Handle the case when chunk_size = 0 */

		int64_t* st_idx = (int64_t*)malloc(num_threads * sizeof(int64_t));
		
		// Fill st_idx[] with start index of each chunk
		for (int32_t thd = 0; thd < num_threads; thd++)
		{
			if (thd == 0) {st_idx[thd] = 0; continue;};
			int64_t start_id = thd * chunk_size;
			int64_t i0 = start_id - (int64_t)1;
			int64_t extra_olp = 0;
			while (i0 >= 0 && ((int32_t)a[start_id].x <= ((int32_t)a[i0].x + max_dist + extra_olp)) && (a[start_id].x>>32 == a[i0].x>>32))
			{
				st_idx[thd] = i0;
				i0--;
			}
		}

		int32_t itr = 0;
		for (itr = 0; itr < num_threads; itr++) // For irregular chunks
		{
			// Parallel RMQ Chaining
			int32_t sum = 0;
			#pragma omp parallel num_threads(num_threads)
			{
				int32_t thd = omp_get_thread_num(); // thread id
				// Initialise RMQ Tree pointers
				lc_elem_t *root = 0, *root_inner = 0;
				int64_t start = thd * chunk_size;
				int64_t end = (thd + 1) * chunk_size;
				if (thd == num_threads - 1) end = n;
				int64_t st = st_idx[thd];
				int64_t st_inner = st_idx[thd];
				int64_t i0 = st_idx[thd];
				int64_t count = 0;
				int32_t mmax_f_loc = 0;
				int32_t max_rmq_size_loc = 0;

				for (int64_t i = start; i < end; i++) // Process chunks in parallel
				{
					if (itr > thd) break; // Theoritical guarantee skip for now

					int64_t max_j = -1;
					int32_t max_f = a[i].y>>32&0xff;
					lc_elem_t s, *q, *r, lo, hi;
					// Fill RMQ Tree for a chunk
					if ( i0 < i && a[i0].x != a[i].x){
						int64_t j;
						for (j = i0; j < i; ++j) {
							if ((int32_t)a[j].x == (int32_t)a[i].x) break; // This needs clear inspection
							q = (lc_elem_t*)malloc(sizeof *q);
							q->y = (int32_t)a[j].y, q->i = j, q->pri = -(f[j] + 0.5 * chn_pen_gap * ((int32_t)a[j].x + (int32_t)a[j].y));
							krmq_insert(lc_elem, &root, q, 0);
							if (max_dist_inner > 0) {
								r = (lc_elem_t*)malloc(sizeof *r);
								*r = *q;
								krmq_insert(lc_elem, &root_inner, r, 0);
							}
						}
						i0 = j;
					}
					
					// get rid of active chains out of range
					while (st < i && (a[i].x>>32 != a[st].x>>32 || a[i].x > a[st].x + max_dist || krmq_size(head, root) > cap_rmq_size)) {
						s.y = (int32_t)a[st].y, s.i = st;
						if ((q = krmq_find(lc_elem, root, &s, 0)) != 0) {
								q = krmq_erase(lc_elem, &root, q, 0);
								free(q);
						}
						++st;
					}

					if (max_dist_inner > 0)  { // similar to the block above, but applied to the inner tree
						while (st_inner < i && (a[i].x>>32 != a[st_inner].x>>32 || a[i].x > a[st_inner].x + max_dist_inner || krmq_size(head, root_inner) > cap_rmq_size)) {
							s.y = (int32_t)a[st_inner].y, s.i = st_inner;
							if ((q = krmq_find(lc_elem, root_inner, &s, 0)) != 0) {
									q = krmq_erase(lc_elem, &root_inner, q, 0);
									free(q);
							}
							++st_inner;
						}
					}

					// RMQ
					lo.i = INT32_MAX, lo.y = (int32_t)a[i].y - max_dist;
					hi.i = 0, hi.y = (int32_t)a[i].y;
					if ((q = krmq_rmq(lc_elem, root, &lo, &hi)) != 0) {
						int32_t sc, exact, width, n_skip = 0;
						int64_t j = q->i;
						assert(q->y >= lo.y && q->y <= hi.y);
						sc = f[j] + comput_sc_simple(&a[i], &a[j], chn_pen_gap, chn_pen_skip, &exact, &width);
						if (width <= bw && sc > max_f) max_f = sc, max_j = j;
						if (!exact && root_inner && (int32_t)a[i].y > 0) {
							lc_elem_t *lo, *hi;
							s.y = (int32_t)a[i].y - 1, s.i = n;
							krmq_interval(lc_elem, root_inner, &s, &lo, &hi);
							if (lo) {
								const lc_elem_t *q;
								int32_t width, n_rmq_iter = 0;
								krmq_itr_t(lc_elem) itr;
								krmq_itr_find(lc_elem, root_inner, lo, &itr);
								while ((q = krmq_at(&itr)) != 0) {
									if (q->y < (int32_t)a[i].y - max_dist_inner) break;
									++n_rmq_iter;
									j = q->i;
									sc = f[j] + comput_sc_simple(&a[i], &a[j], chn_pen_gap, chn_pen_skip, 0, &width);
									if (width <= bw) {
										if (sc > max_f) {
											max_f = sc, max_j = j;
											if (n_skip > 0) --n_skip;
										} else if (t[j] == (int32_t)i) {
											if (++n_skip > max_chn_skip)
												break;
										}
										if (p[j] >= 0) t[p[j]] = i;
									}
									if (!krmq_itr_prev(lc_elem, &itr)) break;
								}
							}
						}
					}
					
					// set max_f and max_j
					assert(max_j < 0 || (a[max_j].x < a[i].x && (int32_t)a[max_j].y < (int32_t)a[i].y)); // always true
					if (max_f !=  f[i] || max_j != p[i]) 
					{
						count++;
						f[i] = max_f;
						p[i] = max_j;
						v[i] = max_j >= 0 && v[max_j] > max_f? v[max_j] : max_f; // v[] keeps the peak score up to i; f[] is the score ending at i, not always the peak
						mmax_f_loc = mmax_f_loc > max_f ? mmax_f_loc : max_f;
						int32_t rmq_size = krmq_size(head, root);
						max_rmq_size_loc = max_rmq_size_loc > rmq_size ? max_rmq_size_loc : rmq_size;
					}
				}
				// clean up RMQ Tree for current iteration
				krmq_clear(lc_elem, &root, free);
				krmq_clear(lc_elem, &root_inner, free);

				// sum count from all threads to sum
				#pragma omp atomic
				sum += count;

				// update mmax_f and max_rmq_size across all threads
				#pragma omp critical
				{
					if (mmax_f < mmax_f_loc) mmax_f = mmax_f_loc;
					if (max_rmq_size < max_rmq_size_loc) max_rmq_size = max_rmq_size_loc;
				}
			}
			if (sum == 0) break; // break if all f[i] are equal
		}

		itr += 1; // Iterations starts from 0
		if (bw != 100000)
		{
			mean_itr_1_ += (float)itr;
		}else
		{
			mean_itr_2_ += (float)itr;
		}
		
		if (bw != 100000)
		{
			max_itr_1 = max_itr_1 > itr ? max_itr_1 : itr;
		}else
		{
			max_itr_2 = max_itr_2 > itr ? max_itr_2 : itr;
		}
		
		count_stages += 1;
		// free memory
		free(st_idx);

	#elif defined(PAR_CHAIN_1)
		int32_t *f, *t, *v, n_u, n_v, mmax_f = 0, max_rmq_size = 0, max_drop = bw;
        int64_t *p;
        uint64_t *u;
        int64_t i, k, n_z, j;
        
        if (_u) *_u = 0, *n_u_ = 0;
        if (n == 0 || a == 0) {
            kfree(km, a);
            return 0;
        }

        int32_t num_chr = 1; // number of chromosomes
        for (i = 1; i < n; i++)
        {
            if (a[i-1].x>>32 != a[i].x>>32) num_chr++;
        }
		int64_t *st_vec = (int64_t*)malloc(num_chr * sizeof(int64_t));
		int64_t *end_vec = (int64_t*)malloc(num_chr * sizeof(int64_t));
		memset(st_vec, 0, num_chr * sizeof(int64_t));
		memset(end_vec, 0, num_chr * sizeof(int64_t));
        int32_t chrom_id = 0;
        if (n > 0) {
			st_vec[0] = 0; // Initialize the start of the first chromosome
			for (i = 1; i < n; i++)
			{
				if (a[i-1].x >> 32 != a[i].x >> 32) // Check for a new chromosome
				{
					end_vec[chrom_id] = i - 1; // Set end for the current chromosome
					chrom_id++; // Move to the next chromosome
					st_vec[chrom_id] = i; // Start index for the new chromosome
				}
			}
			end_vec[chrom_id] = n - 1; // Set end for the last chromosome
		}

		// Handle the case where num_chr is 1
		if (num_chr == 1) {st_vec[0] = 0; end_vec[0] = n - 1;}

		#ifdef GET_DIST
			int64_t max_anchor_chrom = -1;
			for (i = 0; i < num_chr; i++) if (end_vec[i] - st_vec[i] + 1 >= max_anchor_chrom) max_anchor_chrom = end_vec[i] - st_vec[i] + 1;
			double max_anchor_chrom_f = (double)max_anchor_chrom/(double)n;
			// write to anchor_dist_file line by line
			anchor_dist_file << max_anchor_chrom_f << "\n";
		#endif

        if (max_dist < bw) max_dist = bw;
        if (max_dist_inner <= 0 || max_dist_inner >= max_dist) max_dist_inner = 0;
		p = (int64_t*)malloc(n * sizeof(int64_t));
		f = (int32_t*)malloc(n * sizeof(int32_t));
		v = (int32_t*)malloc(n * sizeof(int32_t));
		t = (int32_t*)malloc(n * sizeof(int32_t));

        // parallel initialisation
        #pragma omp parallel for num_threads(num_threads) private(i) // No need to schedule dynamic
        for (i = 0; i < n; i++)
        {
            p[i] = -1; f[i] = 0; v[i] = 0; t[i] = 0;
        }

        #pragma omp parallel for num_threads(num_threads) schedule(dynamic, 1) // No need to schedule dynamic
        for (int32_t thd = 0; thd < num_chr; thd++) // For irregular chunks
        {
            // Initialise RMQ Tree pointers
            lc_elem_t *root = 0, *root_inner = 0;
            int64_t start = st_vec[thd];
            int64_t end = end_vec[thd];
            int64_t st = start;
            int64_t st_inner = start;
            int64_t i0 = start;
            int32_t mmax_f_loc = 0;
            int32_t max_rmq_size_loc = 0;

            for (int64_t i = start; i <= end; i++) // Process chunks in parallel
            {
                int64_t max_j = -1;
                int32_t max_f = a[i].y>>32&0xff;
                lc_elem_t s, *q, *r, lo, hi;
                // Fill RMQ Tree for a chunk
                if ( i0 < i && a[i0].x != a[i].x){
                    int64_t j;
                    for (j = i0; j < i; ++j) {
                        if ((int32_t)a[j].x == (int32_t)a[i].x) break; // This needs clear inspection
                        q = (lc_elem_t*)malloc(sizeof *q);
                        q->y = (int32_t)a[j].y, q->i = j, q->pri = -(f[j] + 0.5 * chn_pen_gap * ((int32_t)a[j].x + (int32_t)a[j].y));
                        krmq_insert(lc_elem, &root, q, 0);
                        if (max_dist_inner > 0) {
                            r = (lc_elem_t*)malloc(sizeof *r);
                            *r = *q;
                            krmq_insert(lc_elem, &root_inner, r, 0);
                        }
                    }
                    i0 = j;
                }
                
                // get rid of active chains out of range
                while (st < i && (a[i].x>>32 != a[st].x>>32 || a[i].x > a[st].x + max_dist || krmq_size(head, root) > cap_rmq_size)) {
                    s.y = (int32_t)a[st].y, s.i = st;
                    if ((q = krmq_find(lc_elem, root, &s, 0)) != 0) {
                            q = krmq_erase(lc_elem, &root, q, 0);
                            free(q);
                    }
                    ++st;
                }

                if (max_dist_inner > 0)  { // similar to the block above, but applied to the inner tree
                    while (st_inner < i && (a[i].x>>32 != a[st_inner].x>>32 || a[i].x > a[st_inner].x + max_dist_inner || krmq_size(head, root_inner) > cap_rmq_size)) {
                        s.y = (int32_t)a[st_inner].y, s.i = st_inner;
                        if ((q = krmq_find(lc_elem, root_inner, &s, 0)) != 0) {
                                q = krmq_erase(lc_elem, &root_inner, q, 0);
                                free(q);
                        }
                        ++st_inner;
                    }
                }

                // RMQ
                lo.i = INT32_MAX, lo.y = (int32_t)a[i].y - max_dist;
                hi.i = 0, hi.y = (int32_t)a[i].y;
                if ((q = krmq_rmq(lc_elem, root, &lo, &hi)) != 0) {
                    int32_t sc, exact, width, n_skip = 0;
                    int64_t j = q->i;
                    assert(q->y >= lo.y && q->y <= hi.y);
                    sc = f[j] + comput_sc_simple(&a[i], &a[j], chn_pen_gap, chn_pen_skip, &exact, &width);
                    if (width <= bw && sc > max_f) max_f = sc, max_j = j;
                    if (!exact && root_inner && (int32_t)a[i].y > 0) {
                        lc_elem_t *lo, *hi;
                        s.y = (int32_t)a[i].y - 1, s.i = n;
                        krmq_interval(lc_elem, root_inner, &s, &lo, &hi);
                        if (lo) {
                            const lc_elem_t *q;
                            int32_t width, n_rmq_iter = 0;
                            krmq_itr_t(lc_elem) itr;
                            krmq_itr_find(lc_elem, root_inner, lo, &itr);
                            while ((q = krmq_at(&itr)) != 0) {
                                if (q->y < (int32_t)a[i].y - max_dist_inner) break;
                                ++n_rmq_iter;
                                j = q->i;
                                sc = f[j] + comput_sc_simple(&a[i], &a[j], chn_pen_gap, chn_pen_skip, 0, &width);
                                if (width <= bw) {
                                    if (sc > max_f) {
                                        max_f = sc, max_j = j;
                                        if (n_skip > 0) --n_skip;
                                    } else if (t[j] == (int32_t)i) {
                                        if (++n_skip > max_chn_skip)
                                            break;
                                    }
                                    if (p[j] >= 0) t[p[j]] = i;
                                }
                                if (!krmq_itr_prev(lc_elem, &itr)) break;
                            }
                        }
                    }
                }
                
                // set max_f and max_j
                assert(max_j < 0 || (a[max_j].x < a[i].x && (int32_t)a[max_j].y < (int32_t)a[i].y)); // always true
                if (max_f !=  f[i] || max_j != p[i]) 
                {
                    f[i] = max_f;
                    p[i] = max_j;
                    v[i] = max_j >= 0 && v[max_j] > max_f? v[max_j] : max_f; // v[] keeps the peak score up to i; f[] is the score ending at i, not always the peak
                    mmax_f_loc = mmax_f_loc > max_f ? mmax_f_loc : max_f;
                    int32_t rmq_size = krmq_size(head, root);
                    max_rmq_size_loc = max_rmq_size_loc > rmq_size ? max_rmq_size_loc : rmq_size;
                }
            }
            // clean up RMQ Tree for current iteration
            krmq_clear(lc_elem, &root, free);
            krmq_clear(lc_elem, &root_inner, free);

            // update mmax_f and max_rmq_size across all threads
            #pragma omp critical
            {
                if (mmax_f < mmax_f_loc) mmax_f = mmax_f_loc;
                if (max_rmq_size < max_rmq_size_loc) max_rmq_size = max_rmq_size_loc;
            }
        }
		// free memory
		free(st_vec); free(end_vec);

	#else
		int32_t *f,*t, *v, n_u, n_v, mmax_f = 0, max_rmq_size = 0, max_drop = bw;
		int64_t *p, i, i0, st = 0, st_inner = 0;
		uint64_t *u;
		lc_elem_t *root = 0, *root_inner = 0;
		void *mem_mp = 0;
		kmp_rmq_t *mp;

		if (_u) *_u = 0, *n_u_ = 0;
		if (n == 0 || a == 0) {
			kfree(km, a);
			return 0;
		}
		if (max_dist < bw) max_dist = bw;
		if (max_dist_inner < 0) max_dist_inner = 0;
		if (max_dist_inner > max_dist) max_dist_inner = max_dist;
		p = Kmalloc(km, int64_t, n);
		f = Kmalloc(km, int32_t, n);
		t = Kcalloc(km, int32_t, n);
		v = Kmalloc(km, int32_t, n);
		mem_mp = km_init2(km, 0x10000);
		mp = kmp_init_rmq(mem_mp);

		// fill the score and backtrack arrays
		for (i = i0 = 0; i < n; ++i) {
			int64_t max_j = -1;
			int32_t q_span = a[i].y>>32&0xff, max_f = q_span;
			lc_elem_t s, *q, *r, lo, hi;
			// add in-range anchors
			if (i0 < i && a[i0].x != a[i].x) {
				int64_t j;
				for (j = i0; j < i; ++j) {
					q = kmp_alloc_rmq(mp);
					q->y = (int32_t)a[j].y, q->i = j, q->pri = -(f[j] + 0.5 * chn_pen_gap * ((int32_t)a[j].x + (int32_t)a[j].y));
					krmq_insert(lc_elem, &root, q, 0);
					if (max_dist_inner > 0) {
						r = kmp_alloc_rmq(mp);
						*r = *q;
						krmq_insert(lc_elem, &root_inner, r, 0);
					}
				}
				i0 = i;
			}
			// get rid of active chains out of range
			while (st < i && (a[i].x>>32 != a[st].x>>32 || a[i].x > a[st].x + max_dist || krmq_size(head, root) > cap_rmq_size)) {
				s.y = (int32_t)a[st].y, s.i = st;
				if ((q = krmq_find(lc_elem, root, &s, 0)) != 0) {
					q = krmq_erase(lc_elem, &root, q, 0);
					kmp_free_rmq(mp, q);
				}
				++st;
			}
			if (max_dist_inner > 0)  { // similar to the block above, but applied to the inner tree
				while (st_inner < i && (a[i].x>>32 != a[st_inner].x>>32 || a[i].x > a[st_inner].x + max_dist_inner || krmq_size(head, root_inner) > cap_rmq_size)) {
					s.y = (int32_t)a[st_inner].y, s.i = st_inner;
					if ((q = krmq_find(lc_elem, root_inner, &s, 0)) != 0) {
						q = krmq_erase(lc_elem, &root_inner, q, 0);
						kmp_free_rmq(mp, q);
					}
					++st_inner;
				}
			}
			// RMQ
			lo.i = INT32_MAX, lo.y = (int32_t)a[i].y - max_dist;
			hi.i = 0, hi.y = (int32_t)a[i].y;
			if ((q = krmq_rmq(lc_elem, root, &lo, &hi)) != 0) {
				int32_t sc, exact, width, n_skip = 0;
				int64_t j = q->i;
				assert(q->y >= lo.y && q->y <= hi.y);
				sc = f[j] + comput_sc_simple(&a[i], &a[j], chn_pen_gap, chn_pen_skip, &exact, &width);
				if (width <= bw && sc > max_f) max_f = sc, max_j = j;
				if (!exact && root_inner && (int32_t)a[i].y > 0) {
					lc_elem_t *lo, *hi;
					s.y = (int32_t)a[i].y - 1, s.i = n;
					krmq_interval(lc_elem, root_inner, &s, &lo, &hi);
					if (lo) {
						const lc_elem_t *q;
						int32_t width;
						krmq_itr_t(lc_elem) itr;
						krmq_itr_find(lc_elem, root_inner, lo, &itr);
						while ((q = krmq_at(&itr)) != 0) {
							if (q->y < (int32_t)a[i].y - max_dist_inner) break;
							j = q->i;
							sc = f[j] + comput_sc_simple(&a[i], &a[j], chn_pen_gap, chn_pen_skip, 0, &width);
							if (width <= bw) {
								if (sc > max_f) {
									max_f = sc, max_j = j;
									if (n_skip > 0) --n_skip;
								} else if (t[j] == (int32_t)i) {
									if (++n_skip > max_chn_skip)
										break;
								}
								if (p[j] >= 0) t[p[j]] = i;
							}
							if (!krmq_itr_prev(lc_elem, &itr)) break;
						}
					}
				}
			}
			// set max
			assert(max_j < 0 || (a[max_j].x < a[i].x && (int32_t)a[max_j].y < (int32_t)a[i].y));
			f[i] = max_f, p[i] = max_j;
			v[i] = max_j >= 0 && v[max_j] > max_f? v[max_j] : max_f; // v[] keeps the peak score up to i; f[] is the score ending at i, not always the peak
			if (mmax_f < max_f) mmax_f = max_f;
			if (max_rmq_size < krmq_size(head, root)) max_rmq_size = krmq_size(head, root);
		}
		km_destroy(mem_mp);
	#endif

	if (max_dist == 100000)
	{
		double time  = 0.0f;
		struct timeval start_btk, end_btk;
		if (is_g2g_aln)
		{
			#ifdef PROFILE
				gettimeofday(&end_chain, NULL);
				time = (end_chain.tv_sec - start_chain.tv_sec) + (end_chain.tv_usec - start_chain.tv_usec) / 1000000.0;
				rmq_2_time_ = rmq_2_time_ > time ? rmq_2_time_ : time;
			#endif

			#ifdef PROFILE
				gettimeofday(&start_btk, NULL);
			#endif
		}

		#if defined(PAR_BTK) 
			u = mg_chain_backtrack_par(km, n, f, p, v, t, min_cnt, min_sc, max_drop, &n_u, &n_v, a);
		#else
			u = mg_chain_backtrack(km, n, f, p, v, t, min_cnt, min_sc, max_drop, &n_u, &n_v);
		#endif

		if (is_g2g_aln)
		{
			#ifdef PROFILE
				gettimeofday(&end_btk, NULL);
				time = (end_btk.tv_sec - start_btk.tv_sec) + (end_btk.tv_usec - start_btk.tv_usec) / 1000000.0;
				btk_2_time_ = btk_2_time_ > time ? btk_2_time_ : time;
			#endif
		}

	} else {
		double time = 0.0f;
		if (is_g2g_aln)
		{
			#ifdef PROFILE
				gettimeofday(&end_chain, NULL);
				time = (end_chain.tv_sec - start_chain.tv_sec) + (end_chain.tv_usec - start_chain.tv_usec) / 1000000.0;
				rmq_1_time_ = rmq_1_time_ > time ? rmq_1_time_ : time;
			#endif
		}

		struct timeval start_btk, end_btk;
		if (is_g2g_aln)
		{
			#ifdef PROFILE
				gettimeofday(&start_btk, NULL);
			#endif
		}
		#if defined(PAR_BTK) 
			u = mg_chain_backtrack_par(km, n, f, p, v, t, min_cnt, min_sc, max_drop, &n_u, &n_v, a);
		#else
			u = mg_chain_backtrack(km, n, f, p, v, t, min_cnt, min_sc, max_drop, &n_u, &n_v);
		#endif

		if (is_g2g_aln)
		{
			#ifdef PROFILE
				gettimeofday(&end_btk, NULL);
				time = (end_btk.tv_sec - start_btk.tv_sec) + (end_btk.tv_usec - start_btk.tv_usec) / 1000000.0;
				btk_1_time_ = btk_1_time_ > time ? btk_1_time_ : time;
			#endif
		}
	}

	#if defined(PAR_CHAIN_1) || defined(PAR_CHAIN_2)
		// do nothing
	#else
		kfree(km, p); kfree(km, f); kfree(km, t);
	#endif

	*n_u_ = n_u, *_u = u;
	if (n_u == 0) {
		kfree(km, a); 
		#if defined(PAR_CHAIN_1) || defined(PAR_CHAIN_2)
			free(v);
		#else
			kfree(km, v);
		#endif
		return 0;
	}

	return compact_a(km, n_u, u, n_v, v, a);
}
mm128_t *mg_lchain_rmq_mm2(int max_dist, int max_dist_inner, int bw, int max_chn_skip, int cap_rmq_size, int min_cnt, int min_sc, float chn_pen_gap, float chn_pen_skip,
					   int64_t n, mm128_t *a, int *n_u_, uint64_t **_u, void *km, int32_t temp)
{
	int32_t *f,*t, *v, n_u, n_v, mmax_f = 0, max_rmq_size = 0, max_drop = bw;
	int64_t *p, i, i0, st = 0, st_inner = 0;
	uint64_t *u;
	lc_elem_t *root = 0, *root_inner = 0;
	void *mem_mp = 0;
	kmp_rmq_t *mp;

	if (_u) *_u = 0, *n_u_ = 0;
	if (n == 0 || a == 0) {
		kfree(km, a);
		return 0;
	}
	if (max_dist < bw) max_dist = bw;
	if (max_dist_inner < 0) max_dist_inner = 0;
	if (max_dist_inner > max_dist) max_dist_inner = max_dist;
	p = Kmalloc(km, int64_t, n);
	f = Kmalloc(km, int32_t, n);
	t = Kcalloc(km, int32_t, n);
	v = Kmalloc(km, int32_t, n);
	mem_mp = km_init2(km, 0x10000);
	mp = kmp_init_rmq(mem_mp);

	// fill the score and backtrack arrays
	for (i = i0 = 0; i < n; ++i) {
		int64_t max_j = -1;
		int32_t q_span = a[i].y>>32&0xff, max_f = q_span;
		lc_elem_t s, *q, *r, lo, hi;
		// add in-range anchors
		if (i0 < i && a[i0].x != a[i].x) {
			int64_t j;
			for (j = i0; j < i; ++j) {
				q = kmp_alloc_rmq(mp);
				q->y = (int32_t)a[j].y, q->i = j, q->pri = -(f[j] + 0.5 * chn_pen_gap * ((int32_t)a[j].x + (int32_t)a[j].y));
				krmq_insert(lc_elem, &root, q, 0);
				if (max_dist_inner > 0) {
					r = kmp_alloc_rmq(mp);
					*r = *q;
					krmq_insert(lc_elem, &root_inner, r, 0);
				}
			}
			i0 = i;
		}
		// get rid of active chains out of range
		while (st < i && (a[i].x>>32 != a[st].x>>32 || a[i].x > a[st].x + max_dist || krmq_size(head, root) > cap_rmq_size)) {
			s.y = (int32_t)a[st].y, s.i = st;
			if ((q = krmq_find(lc_elem, root, &s, 0)) != 0) {
				q = krmq_erase(lc_elem, &root, q, 0);
				kmp_free_rmq(mp, q);
			}
			++st;
		}
		if (max_dist_inner > 0)  { // similar to the block above, but applied to the inner tree
			while (st_inner < i && (a[i].x>>32 != a[st_inner].x>>32 || a[i].x > a[st_inner].x + max_dist_inner || krmq_size(head, root_inner) > cap_rmq_size)) {
				s.y = (int32_t)a[st_inner].y, s.i = st_inner;
				if ((q = krmq_find(lc_elem, root_inner, &s, 0)) != 0) {
					q = krmq_erase(lc_elem, &root_inner, q, 0);
					kmp_free_rmq(mp, q);
				}
				++st_inner;
			}
		}
		// RMQ
		lo.i = INT32_MAX, lo.y = (int32_t)a[i].y - max_dist;
		hi.i = 0, hi.y = (int32_t)a[i].y;
		if ((q = krmq_rmq(lc_elem, root, &lo, &hi)) != 0) {
			int32_t sc, exact, width, n_skip = 0;
			int64_t j = q->i;
			assert(q->y >= lo.y && q->y <= hi.y);
			sc = f[j] + comput_sc_simple(&a[i], &a[j], chn_pen_gap, chn_pen_skip, &exact, &width);
			if (width <= bw && sc > max_f) max_f = sc, max_j = j;
			if (!exact && root_inner && (int32_t)a[i].y > 0) {
				lc_elem_t *lo, *hi;
				s.y = (int32_t)a[i].y - 1, s.i = n;
				krmq_interval(lc_elem, root_inner, &s, &lo, &hi);
				if (lo) {
					const lc_elem_t *q;
					int32_t width;
					krmq_itr_t(lc_elem) itr;
					krmq_itr_find(lc_elem, root_inner, lo, &itr);
					while ((q = krmq_at(&itr)) != 0) {
						if (q->y < (int32_t)a[i].y - max_dist_inner) break;
						j = q->i;
						sc = f[j] + comput_sc_simple(&a[i], &a[j], chn_pen_gap, chn_pen_skip, 0, &width);
						if (width <= bw) {
							if (sc > max_f) {
								max_f = sc, max_j = j;
								if (n_skip > 0) --n_skip;
							} else if (t[j] == (int32_t)i) {
								if (++n_skip > max_chn_skip)
									break;
							}
							if (p[j] >= 0) t[p[j]] = i;
						}
						if (!krmq_itr_prev(lc_elem, &itr)) break;
					}
				}
			}
		}
		// set max
		assert(max_j < 0 || (a[max_j].x < a[i].x && (int32_t)a[max_j].y < (int32_t)a[i].y));
		f[i] = max_f, p[i] = max_j;
		v[i] = max_j >= 0 && v[max_j] > max_f? v[max_j] : max_f; // v[] keeps the peak score up to i; f[] is the score ending at i, not always the peak
		if (mmax_f < max_f) mmax_f = max_f;
		if (max_rmq_size < krmq_size(head, root)) max_rmq_size = krmq_size(head, root);
	}
	km_destroy(mem_mp);

	u = mg_chain_backtrack(km, n, f, p, v, t, min_cnt, min_sc, max_drop, &n_u, &n_v);
	*n_u_ = n_u, *_u = u; // NB: note that u[] may not be sorted by score here
	kfree(km, p); kfree(km, f); kfree(km, t);
	if (n_u == 0) {
		kfree(km, a); kfree(km, v);
		return 0;
	}
	return compact_a(km, n_u, u, n_v, v, a);
}


mm128_t *mg_lchain_rmq(int max_dist, int max_dist_inner, int bw, int max_chn_skip, int cap_rmq_size, int min_cnt, int min_sc, float chn_pen_gap, float chn_pen_skip,
					   int64_t n, mm128_t *a, int *n_u_, uint64_t **_u, void *km, int32_t num_threads)

{
	if (is_g2g_aln)
	{
		return mg_lchain_rmq_opt(max_dist, max_dist_inner, bw, max_chn_skip, cap_rmq_size, min_cnt, min_sc, chn_pen_gap, chn_pen_skip, n, a, n_u_, _u, km, num_threads);
	}else
	{
		return mg_lchain_rmq_mm2(max_dist, max_dist_inner, bw, max_chn_skip, cap_rmq_size, min_cnt, min_sc, chn_pen_gap, chn_pen_skip, n, a, n_u_, _u, km, num_threads);
	}
}