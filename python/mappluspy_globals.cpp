#include <stdint.h>
#include <fstream>
#include <sys/time.h>

void *km1;
uint64_t km_size = 500000000;
int km_top;
int32_t num_threads_b2b = 1;
std::fstream anchor_dist_file;
std::fstream count_chains_file;

int32_t n_seqs_ = 0;
float align_time_ = 0.0f;
float seed_time_ = 0.0f;
float rmq_1_time_ = 0.0f;
float rmq_2_time_ = 0.0f;
float btk_1_time_ = 0.0f;
float btk_2_time_ = 0.0f;
float mm_set_time_ = 0.0f;
float mm_set_time = 0.0f;
float mean_itr_1_ = 0.0f;
float mean_itr_2_ = 0.0f;
float mean_itr_1 = 0.0f;
float mean_itr_2 = 0.0f;
float total_time_ = 0.0f;
float total_time = 0.0f;
int32_t max_itr_1 = 0;
int32_t max_itr_2 = 0;
int32_t count_stages = 0;
int32_t max_thds = 1;
int32_t is_g2g_aln = 0;
int32_t is_splice_sr = 0;

float seed_time = 0.0f;
float alignment_time = 0.0f;
float rmq_1_time = 0.0f;
float rmq_2_time = 0.0f;
float other_time = 0.0f;
float btk_1_time = 0.0f;
float btk_2_time = 0.0f;
struct timeval start;
struct timeval end;
