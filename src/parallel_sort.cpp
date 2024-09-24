#include <parallel/algorithm>
#include "mmpriv.h"
#include <omp.h>

void parallel_sort(mm128_t* z, size_t n_u, int32_t n_thds) {
    omp_set_num_threads(n_thds);
    __gnu_parallel::stable_sort(z, z + n_u, [](const mm128_t &a, const mm128_t &b) { return a.x < b.x;});
}