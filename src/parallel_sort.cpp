#define _GLIBCXX_PARALLEL
#include <parallel/algorithm>
#include "mmpriv.h"

void parallel_sort(mm128_t* z, size_t n_u) {
    __gnu_parallel::stable_sort(z, z + n_u, [](const mm128_t &a, const mm128_t &b) { return a.x < b.x; });
}

#undef _GLIBCXX_PARALLEL  // This ensures parallel features are only enabled within this file