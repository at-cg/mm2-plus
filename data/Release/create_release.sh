#!/bin/bash

set -euo pipefail

VERSION="${1:-v1.3}"

# --- locate paths ------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"      # .../data/Release
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"                    # repo root
OUT_DIR="$SCRIPT_DIR/$VERSION"
RUN_SIMD="$SCRIPT_DIR/run_simd.cpp"

# --- toolchain ---------------------------------------------------------------
CXX_BIN="${CXX:-}"
CC_BIN="${CC:-}"
if [[ -z "$CXX_BIN" ]]; then
    if command -v x86_64-conda-linux-gnu-c++ >/dev/null 2>&1; then
        CXX_BIN="$(command -v x86_64-conda-linux-gnu-c++)"
        CC_BIN="$(command -v x86_64-conda-linux-gnu-cc)"
    else
        CXX_BIN="g++"; CC_BIN="gcc"
    fi
fi
[[ -z "$CC_BIN" ]] && CC_BIN="gcc"

# --- static link flags -------------------------------------------------------
# -static                         : fully static executable
# --allow-multiple-definition     : jemalloc overrides glibc malloc/free/realloc
STATIC_LDFLAGS="-static -Wl,--allow-multiple-definition"

# --- ISA variants: name -> SIMD feature flag ---------------------------------
# The conda toolchain has a plain x86-64/SSE2 default baseline, so these -m
# feature flags restrict each binary to exactly that ISA (no higher SIMD leaks in).
VARIANTS=(avx512 avx2 avx sse4.2 sse4.1)
declare -A ARCH=(
    [avx512]="-mavx512bw"
    [avx2]="-mavx2"
    [avx]="-mavx"
    [sse4.2]="-msse4.2"
    [sse4.1]="-msse4.1"
)

echo "=============================================================="
echo " mm2-plus release builder"
echo " version : $VERSION"
echo " repo    : $REPO_ROOT"
echo " output  : $OUT_DIR"
echo " CXX     : $CXX_BIN"
echo "=============================================================="

mkdir -p "$OUT_DIR"
cd "$REPO_ROOT"

# --- ensure dependencies (jemalloc + zlib) are built -------------------------
if [[ ! -f external/jemalloc/lib/libjemalloc.a || ! -f external/zlib/lib/libz.a ]]; then
    echo "[deps] building jemalloc + zlib ..."
    make deps
fi

# --- helper: count instrs/registers only inside mm2-plus's OWN functions ------
# (mm_*, mg_*, ksw_*, SoA/anchor helpers) so static libc/libstdc++/libgomp/
# jemalloc/zlib code does not pollute the ISA verification.
own_count() { # $1=binary  $2=regex of instruction/register
    objdump -d "$1" 2>/dev/null | awk -v pat="$2" '
        /^[0-9a-f]+ <.*>:/ { f=$2 }
        $0 ~ pat && f ~ /ksw_|mm_|mg_|SoA|anchor|lchain|chain_backtrack/ { c++ }
        END { print c+0 }'
}

verify_static() {
    if file "$1" | grep -q "statically linked" && ! ldd "$1" >/dev/null 2>&1; then
        echo "    [static ] OK (not a dynamic executable)"
        return 0
    fi
    echo "    [static ] FAIL — binary is not fully static"; return 1
}

verify_isa() { # $1=binary  $2=variant
    local bin="$1" v="$2"
    local zmm ymm avx2int sse42
    zmm=$(own_count "$bin" "%zmm")
    ymm=$(own_count "$bin" "%ymm")
    avx2int=$(own_count "$bin" "vp[a-z0-9]+[^,]*%ymm")
    sse42=$(own_count "$bin" "crc32|pcmpgtq|pcmpistr|pcmpestr")
    case "$v" in
        avx512)
            if [[ "$zmm" -gt 0 ]]; then echo "    [isa    ] OK — AVX-512 (zmm=$zmm)"; else echo "    [isa    ] FAIL — no zmm found"; return 1; fi ;;
        avx2)
            if [[ "$zmm" -eq 0 && "$avx2int" -gt 0 ]]; then echo "    [isa    ] OK — AVX2 (own ymm=$ymm, avx2-int=$avx2int, zmm=0)"; else echo "    [isa    ] FAIL — zmm=$zmm avx2int=$avx2int"; return 1; fi ;;
        avx)
            if [[ "$zmm" -eq 0 && "$avx2int" -eq 0 && "$ymm" -gt 0 ]]; then echo "    [isa    ] OK — AVX (own ymm=$ymm, no avx2-int, zmm=0)"; else echo "    [isa    ] FAIL — zmm=$zmm avx2int=$avx2int own_ymm=$ymm"; return 1; fi ;;
        sse4.2)
            if [[ "$zmm" -eq 0 && "$ymm" -eq 0 && "$sse42" -gt 0 ]]; then echo "    [isa    ] OK — SSE4.2 (own ymm=0, sse42 ops=$sse42, zmm=0)"; else echo "    [isa    ] FAIL — zmm=$zmm own_ymm=$ymm sse42=$sse42"; return 1; fi ;;
        sse4.1)
            if [[ "$zmm" -eq 0 && "$ymm" -eq 0 && "$sse42" -eq 0 ]]; then echo "    [isa    ] OK — SSE4.1 (own ymm=0, no sse4.2 ops, zmm=0)"; else echo "    [isa    ] FAIL — zmm=$zmm own_ymm=$ymm sse42=$sse42"; return 1; fi ;;
    esac
}

# --- build each variant ------------------------------------------------------
for v in "${VARIANTS[@]}"; do
    echo
    echo "-------- building mm2plus.$v (${ARCH[$v]}) --------"
    make clean >/dev/null 2>&1 || true
    make -j SIMD_FLAGS="${ARCH[$v]}" CXX="$CXX_BIN" CC="$CC_BIN" \
         BDYNAMIC= RELEASE_LDFLAGS="$STATIC_LDFLAGS"
    cp -f mm2plus "$OUT_DIR/mm2plus.$v"
    verify_static "$OUT_DIR/mm2plus.$v"
    verify_isa    "$OUT_DIR/mm2plus.$v" "$v"
done

# --- build the CPU-dispatching launcher (static, plain C) --------------------
echo
echo "-------- building dispatcher mm2plus --------"
"$CC_BIN" -O2 -static -x c "$RUN_SIMD" -o "$OUT_DIR/mm2plus"
verify_static "$OUT_DIR/mm2plus"

# --- pack the release tarball (flat layout, matching upstream releases) -------
# Version tag v1.3 -> tarball mm2-plus-1.3_x64-linux.tar.bz2
VER_NUM="${VERSION#v}"
TARBALL="$SCRIPT_DIR/mm2-plus-${VER_NUM}_x64-linux.tar.bz2"
echo
echo "-------- packing $TARBALL --------"
tar cjf "$TARBALL" -C "$OUT_DIR" mm2plus mm2plus.avx512 mm2plus.avx2 mm2plus.avx mm2plus.sse4.2 mm2plus.sse4.1
echo "    packed: $TARBALL"
tar tjf "$TARBALL" | sed 's/^/      /'

# --- summary -----------------------------------------------------------------
echo
echo "=============================================================="
echo " Release $VERSION built in: $OUT_DIR"
echo "=============================================================="
ls -la "$OUT_DIR"
make clean >/dev/null 2>&1 || true
