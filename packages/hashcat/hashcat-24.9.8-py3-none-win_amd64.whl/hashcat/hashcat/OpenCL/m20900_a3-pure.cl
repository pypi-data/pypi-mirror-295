/**
 * Author......: See docs/credits.txt
 * License.....: MIT
 */

#define NEW_SIMD_CODE

#ifdef KERNEL_STATIC
#include M2S(INCLUDE_PATH/inc_vendor.h)
#include M2S(INCLUDE_PATH/inc_types.h)
#include M2S(INCLUDE_PATH/inc_platform.cl)
#include M2S(INCLUDE_PATH/inc_common.cl)
#include M2S(INCLUDE_PATH/inc_simd.cl)
#include M2S(INCLUDE_PATH/inc_hash_md5.cl)
#include M2S(INCLUDE_PATH/inc_hash_sha1.cl)
#endif

#if   VECT_SIZE == 1
#define uint_to_hex_lower8(i) make_u32x (l_bin2asc[(i)])
#elif VECT_SIZE == 2
#define uint_to_hex_lower8(i) make_u32x (l_bin2asc[(i).s0], l_bin2asc[(i).s1])
#elif VECT_SIZE == 4
#define uint_to_hex_lower8(i) make_u32x (l_bin2asc[(i).s0], l_bin2asc[(i).s1], l_bin2asc[(i).s2], l_bin2asc[(i).s3])
#elif VECT_SIZE == 8
#define uint_to_hex_lower8(i) make_u32x (l_bin2asc[(i).s0], l_bin2asc[(i).s1], l_bin2asc[(i).s2], l_bin2asc[(i).s3], l_bin2asc[(i).s4], l_bin2asc[(i).s5], l_bin2asc[(i).s6], l_bin2asc[(i).s7])
#elif VECT_SIZE == 16
#define uint_to_hex_lower8(i) make_u32x (l_bin2asc[(i).s0], l_bin2asc[(i).s1], l_bin2asc[(i).s2], l_bin2asc[(i).s3], l_bin2asc[(i).s4], l_bin2asc[(i).s5], l_bin2asc[(i).s6], l_bin2asc[(i).s7], l_bin2asc[(i).s8], l_bin2asc[(i).s9], l_bin2asc[(i).sa], l_bin2asc[(i).sb], l_bin2asc[(i).sc], l_bin2asc[(i).sd], l_bin2asc[(i).se], l_bin2asc[(i).sf])
#endif

KERNEL_FQ void m20900_mxx (KERN_ATTR_VECTOR ())
{
  /**
   * modifier
   */

  const u64 gid = get_global_id (0);
  const u64 lid = get_local_id (0);
  const u64 lsz = get_local_size (0);

  /**
   * bin2asc table
   */

  LOCAL_VK u32 l_bin2asc[256];

  for (u32 i = lid; i < 256; i += lsz)
  {
    const u32 i0 = (i >> 0) & 15;
    const u32 i1 = (i >> 4) & 15;

    l_bin2asc[i] = ((i0 < 10) ? '0' + i0 : 'a' - 10 + i0) << 8
                 | ((i1 < 10) ? '0' + i1 : 'a' - 10 + i1) << 0;
  }

  SYNC_THREADS ();

  if (gid >= GID_CNT) return;

  /**
   * base
   */

  const u32 pw_len = pws[gid].pw_len;

  u32x w[64] = { 0 };

  for (u32 i = 0, idx = 0; i < pw_len; i += 4, idx += 1)
  {
    w[idx] = pws[gid].i[idx];
  }

  /**
   * loop
   */

  u32x _w0[4];
  u32x _w1[4];
  u32x _w2[4];
  u32x _w3[4];

  u32x w0l = w[0];

  for (u32 il_pos = 0; il_pos < IL_CNT; il_pos += VECT_SIZE)
  {
    const u32x w0r = words_buf_r[il_pos / VECT_SIZE];

    const u32x w0 = w0l | w0r;

    w[0] = w0;

    sha1_ctx_vector_t ctx0;

    sha1_init_vector (&ctx0);

    sha1_update_vector_swap (&ctx0, w, pw_len);

    sha1_final_vector (&ctx0);

    const u32x a0 = ctx0.h[0];
    const u32x b0 = ctx0.h[1];
    const u32x c0 = ctx0.h[2];
    const u32x d0 = ctx0.h[3];
    const u32x e0 = ctx0.h[4];

    md5_ctx_vector_t ctx1;

    md5_init_vector (&ctx1);

    md5_update_vector (&ctx1, w, pw_len);

    md5_final_vector (&ctx1);

    const u32x a1 = hc_swap32 (ctx1.h[0]);
    const u32x b1 = hc_swap32 (ctx1.h[1]);
    const u32x c1 = hc_swap32 (ctx1.h[2]);
    const u32x d1 = hc_swap32 (ctx1.h[3]);

    md5_ctx_vector_t ctx;

    md5_init_vector (&ctx);

    _w0[0] = uint_to_hex_lower8 ((a0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((a0 >> 16) & 255) << 16;
    _w0[1] = uint_to_hex_lower8 ((a0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((a0 >>  0) & 255) << 16;
    _w0[2] = uint_to_hex_lower8 ((b0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((b0 >> 16) & 255) << 16;
    _w0[3] = uint_to_hex_lower8 ((b0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((b0 >>  0) & 255) << 16;
    _w1[0] = uint_to_hex_lower8 ((c0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((c0 >> 16) & 255) << 16;
    _w1[1] = uint_to_hex_lower8 ((c0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((c0 >>  0) & 255) << 16;
    _w1[2] = uint_to_hex_lower8 ((d0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((d0 >> 16) & 255) << 16;
    _w1[3] = uint_to_hex_lower8 ((d0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((d0 >>  0) & 255) << 16;
    _w2[0] = uint_to_hex_lower8 ((e0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((e0 >> 16) & 255) << 16;
    _w2[1] = uint_to_hex_lower8 ((e0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((e0 >>  0) & 255) << 16;

    _w2[2] = 0;
    _w2[3] = 0;
    _w3[0] = 0;
    _w3[1] = 0;
    _w3[2] = 0;
    _w3[3] = 0;

    md5_update_vector_64 (&ctx, _w0, _w1, _w2, _w3, 40);

    _w0[0] = uint_to_hex_lower8 ((a1 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((a1 >> 16) & 255) << 16;
    _w0[1] = uint_to_hex_lower8 ((a1 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((a1 >>  0) & 255) << 16;
    _w0[2] = uint_to_hex_lower8 ((b1 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((b1 >> 16) & 255) << 16;
    _w0[3] = uint_to_hex_lower8 ((b1 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((b1 >>  0) & 255) << 16;
    _w1[0] = uint_to_hex_lower8 ((c1 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((c1 >> 16) & 255) << 16;
    _w1[1] = uint_to_hex_lower8 ((c1 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((c1 >>  0) & 255) << 16;
    _w1[2] = uint_to_hex_lower8 ((d1 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((d1 >> 16) & 255) << 16;
    _w1[3] = uint_to_hex_lower8 ((d1 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((d1 >>  0) & 255) << 16;

    _w2[0] = 0;
    _w2[1] = 0;
    _w2[2] = 0;
    _w2[3] = 0;
    _w3[0] = 0;
    _w3[1] = 0;
    _w3[2] = 0;
    _w3[3] = 0;

    md5_update_vector_64 (&ctx, _w0, _w1, _w2, _w3, 32);

    _w0[0] = uint_to_hex_lower8 ((a0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((a0 >> 16) & 255) << 16;
    _w0[1] = uint_to_hex_lower8 ((a0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((a0 >>  0) & 255) << 16;
    _w0[2] = uint_to_hex_lower8 ((b0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((b0 >> 16) & 255) << 16;
    _w0[3] = uint_to_hex_lower8 ((b0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((b0 >>  0) & 255) << 16;
    _w1[0] = uint_to_hex_lower8 ((c0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((c0 >> 16) & 255) << 16;
    _w1[1] = uint_to_hex_lower8 ((c0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((c0 >>  0) & 255) << 16;
    _w1[2] = uint_to_hex_lower8 ((d0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((d0 >> 16) & 255) << 16;
    _w1[3] = uint_to_hex_lower8 ((d0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((d0 >>  0) & 255) << 16;
    _w2[0] = uint_to_hex_lower8 ((e0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((e0 >> 16) & 255) << 16;
    _w2[1] = uint_to_hex_lower8 ((e0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((e0 >>  0) & 255) << 16;

    _w2[2] = 0;
    _w2[3] = 0;
    _w3[0] = 0;
    _w3[1] = 0;
    _w3[2] = 0;
    _w3[3] = 0;

    md5_update_vector_64 (&ctx, _w0, _w1, _w2, _w3, 40);

    md5_final_vector (&ctx);

    const u32x r0 = ctx.h[DGST_R0];
    const u32x r1 = ctx.h[DGST_R1];
    const u32x r2 = ctx.h[DGST_R2];
    const u32x r3 = ctx.h[DGST_R3];

    COMPARE_M_SIMD (r0, r1, r2, r3);
  }
}

KERNEL_FQ void m20900_sxx (KERN_ATTR_VECTOR ())
{
  /**
   * modifier
   */

  const u64 gid = get_global_id (0);
  const u64 lid = get_local_id (0);
  const u64 lsz = get_local_size (0);

  /**
   * bin2asc table
   */

  LOCAL_VK u32 l_bin2asc[256];

  for (u32 i = lid; i < 256; i += lsz)
  {
    const u32 i0 = (i >> 0) & 15;
    const u32 i1 = (i >> 4) & 15;

    l_bin2asc[i] = ((i0 < 10) ? '0' + i0 : 'a' - 10 + i0) << 8
                 | ((i1 < 10) ? '0' + i1 : 'a' - 10 + i1) << 0;
  }

  SYNC_THREADS ();

  if (gid >= GID_CNT) return;

  /**
   * digest
   */

  const u32 search[4] =
  {
    digests_buf[DIGESTS_OFFSET_HOST].digest_buf[DGST_R0],
    digests_buf[DIGESTS_OFFSET_HOST].digest_buf[DGST_R1],
    digests_buf[DIGESTS_OFFSET_HOST].digest_buf[DGST_R2],
    digests_buf[DIGESTS_OFFSET_HOST].digest_buf[DGST_R3]
  };

  /**
   * base
   */

  const u32 pw_len = pws[gid].pw_len;

  u32x w[64] = { 0 };

  for (u32 i = 0, idx = 0; i < pw_len; i += 4, idx += 1)
  {
    w[idx] = pws[gid].i[idx];
  }

  /**
   * loop
   */

  u32x _w0[4];
  u32x _w1[4];
  u32x _w2[4];
  u32x _w3[4];

  u32x w0l = w[0];

  for (u32 il_pos = 0; il_pos < IL_CNT; il_pos += VECT_SIZE)
  {
    const u32x w0r = words_buf_r[il_pos / VECT_SIZE];

    const u32x w0 = w0l | w0r;

    w[0] = w0;

    sha1_ctx_vector_t ctx0;

    sha1_init_vector (&ctx0);

    sha1_update_vector_swap (&ctx0, w, pw_len);

    sha1_final_vector (&ctx0);

    const u32x a0 = ctx0.h[0];
    const u32x b0 = ctx0.h[1];
    const u32x c0 = ctx0.h[2];
    const u32x d0 = ctx0.h[3];
    const u32x e0 = ctx0.h[4];

    md5_ctx_vector_t ctx1;

    md5_init_vector (&ctx1);

    md5_update_vector (&ctx1, w, pw_len);

    md5_final_vector (&ctx1);

    const u32x a1 = hc_swap32 (ctx1.h[0]);
    const u32x b1 = hc_swap32 (ctx1.h[1]);
    const u32x c1 = hc_swap32 (ctx1.h[2]);
    const u32x d1 = hc_swap32 (ctx1.h[3]);

    md5_ctx_vector_t ctx;

    md5_init_vector (&ctx);

    _w0[0] = uint_to_hex_lower8 ((a0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((a0 >> 16) & 255) << 16;
    _w0[1] = uint_to_hex_lower8 ((a0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((a0 >>  0) & 255) << 16;
    _w0[2] = uint_to_hex_lower8 ((b0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((b0 >> 16) & 255) << 16;
    _w0[3] = uint_to_hex_lower8 ((b0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((b0 >>  0) & 255) << 16;
    _w1[0] = uint_to_hex_lower8 ((c0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((c0 >> 16) & 255) << 16;
    _w1[1] = uint_to_hex_lower8 ((c0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((c0 >>  0) & 255) << 16;
    _w1[2] = uint_to_hex_lower8 ((d0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((d0 >> 16) & 255) << 16;
    _w1[3] = uint_to_hex_lower8 ((d0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((d0 >>  0) & 255) << 16;
    _w2[0] = uint_to_hex_lower8 ((e0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((e0 >> 16) & 255) << 16;
    _w2[1] = uint_to_hex_lower8 ((e0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((e0 >>  0) & 255) << 16;

    _w2[2] = 0;
    _w2[3] = 0;
    _w3[0] = 0;
    _w3[1] = 0;
    _w3[2] = 0;
    _w3[3] = 0;

    md5_update_vector_64 (&ctx, _w0, _w1, _w2, _w3, 40);

    _w0[0] = uint_to_hex_lower8 ((a1 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((a1 >> 16) & 255) << 16;
    _w0[1] = uint_to_hex_lower8 ((a1 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((a1 >>  0) & 255) << 16;
    _w0[2] = uint_to_hex_lower8 ((b1 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((b1 >> 16) & 255) << 16;
    _w0[3] = uint_to_hex_lower8 ((b1 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((b1 >>  0) & 255) << 16;
    _w1[0] = uint_to_hex_lower8 ((c1 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((c1 >> 16) & 255) << 16;
    _w1[1] = uint_to_hex_lower8 ((c1 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((c1 >>  0) & 255) << 16;
    _w1[2] = uint_to_hex_lower8 ((d1 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((d1 >> 16) & 255) << 16;
    _w1[3] = uint_to_hex_lower8 ((d1 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((d1 >>  0) & 255) << 16;

    _w2[0] = 0;
    _w2[1] = 0;
    _w2[2] = 0;
    _w2[3] = 0;
    _w3[0] = 0;
    _w3[1] = 0;
    _w3[2] = 0;
    _w3[3] = 0;

    md5_update_vector_64 (&ctx, _w0, _w1, _w2, _w3, 32);

    _w0[0] = uint_to_hex_lower8 ((a0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((a0 >> 16) & 255) << 16;
    _w0[1] = uint_to_hex_lower8 ((a0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((a0 >>  0) & 255) << 16;
    _w0[2] = uint_to_hex_lower8 ((b0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((b0 >> 16) & 255) << 16;
    _w0[3] = uint_to_hex_lower8 ((b0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((b0 >>  0) & 255) << 16;
    _w1[0] = uint_to_hex_lower8 ((c0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((c0 >> 16) & 255) << 16;
    _w1[1] = uint_to_hex_lower8 ((c0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((c0 >>  0) & 255) << 16;
    _w1[2] = uint_to_hex_lower8 ((d0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((d0 >> 16) & 255) << 16;
    _w1[3] = uint_to_hex_lower8 ((d0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((d0 >>  0) & 255) << 16;
    _w2[0] = uint_to_hex_lower8 ((e0 >> 24) & 255) <<  0
           | uint_to_hex_lower8 ((e0 >> 16) & 255) << 16;
    _w2[1] = uint_to_hex_lower8 ((e0 >>  8) & 255) <<  0
           | uint_to_hex_lower8 ((e0 >>  0) & 255) << 16;

    _w2[2] = 0;
    _w2[3] = 0;
    _w3[0] = 0;
    _w3[1] = 0;
    _w3[2] = 0;
    _w3[3] = 0;

    md5_update_vector_64 (&ctx, _w0, _w1, _w2, _w3, 40);

    md5_final_vector (&ctx);

    const u32x r0 = ctx.h[DGST_R0];
    const u32x r1 = ctx.h[DGST_R1];
    const u32x r2 = ctx.h[DGST_R2];
    const u32x r3 = ctx.h[DGST_R3];

    COMPARE_S_SIMD (r0, r1, r2, r3);
  }
}
