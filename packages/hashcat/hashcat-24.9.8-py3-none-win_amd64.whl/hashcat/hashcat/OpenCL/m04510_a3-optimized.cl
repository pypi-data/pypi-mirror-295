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
#include M2S(INCLUDE_PATH/inc_hash_sha1.cl)
#endif

#if   VECT_SIZE == 1
#define uint_to_hex_lower8_le(i) make_u32x (l_bin2asc[(i)])
#elif VECT_SIZE == 2
#define uint_to_hex_lower8_le(i) make_u32x (l_bin2asc[(i).s0], l_bin2asc[(i).s1])
#elif VECT_SIZE == 4
#define uint_to_hex_lower8_le(i) make_u32x (l_bin2asc[(i).s0], l_bin2asc[(i).s1], l_bin2asc[(i).s2], l_bin2asc[(i).s3])
#elif VECT_SIZE == 8
#define uint_to_hex_lower8_le(i) make_u32x (l_bin2asc[(i).s0], l_bin2asc[(i).s1], l_bin2asc[(i).s2], l_bin2asc[(i).s3], l_bin2asc[(i).s4], l_bin2asc[(i).s5], l_bin2asc[(i).s6], l_bin2asc[(i).s7])
#elif VECT_SIZE == 16
#define uint_to_hex_lower8_le(i) make_u32x (l_bin2asc[(i).s0], l_bin2asc[(i).s1], l_bin2asc[(i).s2], l_bin2asc[(i).s3], l_bin2asc[(i).s4], l_bin2asc[(i).s5], l_bin2asc[(i).s6], l_bin2asc[(i).s7], l_bin2asc[(i).s8], l_bin2asc[(i).s9], l_bin2asc[(i).sa], l_bin2asc[(i).sb], l_bin2asc[(i).sc], l_bin2asc[(i).sd], l_bin2asc[(i).se], l_bin2asc[(i).sf])
#endif

DECLSPEC void m04510m (PRIVATE_AS u32 *w0, PRIVATE_AS u32 *w1, PRIVATE_AS u32 *w2, PRIVATE_AS u32 *w3, const u32 pw_len, KERN_ATTR_FUNC_BASIC (), LOCAL_AS u32 * l_bin2asc)
{
  /**
   * modifiers are taken from args
   */

  /**
   * salt
   */

  u32 salt_buf0[4];
  u32 salt_buf1[4];
  u32 salt_buf2[4];
  u32 salt_buf3[4];

  salt_buf0[0] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[0]);
  salt_buf0[1] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[1]);
  salt_buf0[2] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[2]);
  salt_buf0[3] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[3]);
  salt_buf1[0] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[4]);
  salt_buf1[1] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[5]);
  salt_buf1[2] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[6]);
  salt_buf1[3] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[7]);
  salt_buf2[0] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[8]);
  salt_buf2[1] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[9]);
  salt_buf2[2] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[10]);
  salt_buf2[3] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[11]);
  salt_buf3[0] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[12]);
  salt_buf3[1] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[13]);
  salt_buf3[2] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[14]);
  salt_buf3[3] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[15]);

  const u32 salt_len = salt_bufs[SALT_POS_HOST].salt_len;

  /**
   * loop
   */

  u32 w0l = w0[0];

  for (u32 il_pos = 0; il_pos < IL_CNT; il_pos += VECT_SIZE)
  {
    const u32x w0r = ix_create_bft (bfs_buf, il_pos);

    const u32x w0lr = w0l | w0r;


    /**
    * sha1
    */

    // Contains the password

    u32x w0_t = w0lr;
    u32x w1_t = w0[1];
    u32x w2_t = w0[2];
    u32x w3_t = w0[3];
    u32x w4_t = w1[0];
    u32x w5_t = w1[1];
    u32x w6_t = w1[2];
    u32x w7_t = w1[3];
    u32x w8_t = w2[0];
    u32x w9_t = w2[1];
    u32x wa_t = w2[2];
    u32x wb_t = w2[3];
    u32x wc_t = w3[0];
    u32x wd_t = w3[1];
    u32x we_t = w3[2];
    u32x wf_t = w3[3];

    // original hash state
    u32x a = SHA1M_A;
    u32x b = SHA1M_B;
    u32x c = SHA1M_C;
    u32x d = SHA1M_D;
    u32x e = SHA1M_E;

    // Compute SHA1

#undef K
#define K SHA1C00

    SHA1_STEP (SHA1_F0o, a, b, c, d, e, w0_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w1_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w2_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w3_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w4_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, w5_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w6_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w7_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w8_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w9_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, wa_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, wb_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, wc_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, wd_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, we_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w3_t);

#undef K
#define K SHA1C01

    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w7_t);

#undef K
#define K SHA1C02

    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, wb_t);

#undef K
#define K SHA1C03

    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wf_t);

    // Update sha1 state
    a += make_u32x (SHA1M_A);
    b += make_u32x (SHA1M_B);
    c += make_u32x (SHA1M_C);
    d += make_u32x (SHA1M_D);
    e += make_u32x (SHA1M_E);

    /**
    * 2nd SHA1
    */

    // Convert to ascii
    w0_t = uint_to_hex_lower8_le ((a >> 16) & 255) << 0 | uint_to_hex_lower8_le ((a >> 24) & 255) << 16;
    w1_t = uint_to_hex_lower8_le ((a >> 0) & 255) << 0 | uint_to_hex_lower8_le ((a >> 8) & 255) << 16;
    w2_t = uint_to_hex_lower8_le ((b >> 16) & 255) << 0 | uint_to_hex_lower8_le ((b >> 24) & 255) << 16;
    w3_t = uint_to_hex_lower8_le ((b >> 0) & 255) << 0 | uint_to_hex_lower8_le ((b >> 8) & 255) << 16;
    w4_t = uint_to_hex_lower8_le ((c >> 16) & 255) << 0 | uint_to_hex_lower8_le ((c >> 24) & 255) << 16;
    w5_t = uint_to_hex_lower8_le ((c >> 0) & 255) << 0 | uint_to_hex_lower8_le ((c >> 8) & 255) << 16;
    w6_t = uint_to_hex_lower8_le ((d >> 16) & 255) << 0 | uint_to_hex_lower8_le ((d >> 24) & 255) << 16;
    w7_t = uint_to_hex_lower8_le ((d >> 0) & 255) << 0 | uint_to_hex_lower8_le ((d >> 8) & 255) << 16;
    w8_t = uint_to_hex_lower8_le ((e >> 16) & 255) << 0 | uint_to_hex_lower8_le ((e >> 24) & 255) << 16;
    w9_t = uint_to_hex_lower8_le ((e >> 0) & 255) << 0 | uint_to_hex_lower8_le ((e >> 8) & 255) << 16;
    wa_t = 0;
    wb_t = 0;
    wc_t = 0;
    wd_t = 0;
    we_t = 0;
    wf_t = 0;


    u32x digest[8];

    // Reset hash state for the second computation
    a = SHA1M_A;
    b = SHA1M_B;
    c = SHA1M_C;
    d = SHA1M_D;
    e = SHA1M_E;

    digest[0] = a;
    digest[1] = b;
    digest[2] = c;
    digest[3] = d;
    digest[4] = e;

    // append salt

    // ctx_len 40, pos 40

    int pos = 40;

    u32x s0[4];
    u32x s1[4];
    u32x s2[4];
    u32x s3[4];

    s0[0] = salt_buf0[0];
    s0[1] = salt_buf0[1];
    s0[2] = salt_buf0[2];
    s0[3] = salt_buf0[3];
    s1[0] = salt_buf1[0];
    s1[1] = salt_buf1[1];
    s1[2] = salt_buf1[2];
    s1[3] = salt_buf1[3];
    s2[0] = salt_buf2[0];
    s2[1] = salt_buf2[1];
    s2[2] = salt_buf2[2];
    s2[3] = salt_buf2[3];
    s3[0] = salt_buf3[0];
    s3[1] = salt_buf3[1];
    s3[2] = salt_buf3[2];
    s3[3] = salt_buf3[3];

    if ((pos + salt_len) < 64)
    {
      switch_buffer_by_offset_be (s0, s1, s2, s3, pos);

      w0_t |= s0[0];
      w1_t |= s0[1];
      w2_t |= s0[2];
      w3_t |= s0[3];
      w4_t |= s1[0];
      w5_t |= s1[1];
      w6_t |= s1[2];
      w7_t |= s1[3];
      w8_t |= s2[0];
      w9_t |= s2[1];
      wa_t |= s2[2];
      wb_t |= s2[3];
      wc_t |= s3[0];
      wd_t |= s3[1];
      we_t |= s3[2];
      wf_t |= s3[3];
    }
    else
    {
      u32x _w0[4] = { 0 };
      u32x _w1[4] = { 0 };
      u32x _w2[4] = { 0 };
      u32x _w3[4] = { 0 };

      switch_buffer_by_offset_carry_be (s0, s1, s2, s3, _w0, _w1, _w2, _w3, pos);

      w0_t |= s0[0];
      w1_t |= s0[1];
      w2_t |= s0[2];
      w3_t |= s0[3];
      w4_t |= s1[0];
      w5_t |= s1[1];
      w6_t |= s1[2];
      w7_t |= s1[3];
      w8_t |= s2[0];
      w9_t |= s2[1];
      wa_t |= s2[2];
      wb_t |= s2[3];
      wc_t |= s3[0];
      wd_t |= s3[1];
      we_t |= s3[2];
      wf_t |= s3[3];

      // sha1 transform

#undef K
#define K SHA1C00

      SHA1_STEP (SHA1_F0o, a, b, c, d, e, w0_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w1_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w2_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w3_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w4_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, w5_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w6_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w7_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w8_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w9_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, wa_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, wb_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, wc_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, wd_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, we_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w3_t);

#undef K
#define K SHA1C01

      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w7_t);

#undef K
#define K SHA1C02

      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, wb_t);

#undef K
#define K SHA1C03

      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wf_t);

      digest[0] += a;
      digest[1] += b;
      digest[2] += c;
      digest[3] += d;
      digest[4] += e;

      w0_t = _w0[0];
      w1_t = _w0[1];
      w2_t = _w0[2];
      w3_t = _w0[3];
      w4_t = _w1[0];
      w5_t = _w1[1];
      w6_t = _w1[2];
      w7_t = _w1[3];
      w8_t = _w2[0];
      w9_t = _w2[1];
      wa_t = _w2[2];
      wb_t = _w2[3];
      wc_t = _w3[0];
      wd_t = _w3[1];
      we_t = _w3[2];
      wf_t = _w3[3];
    }

    const int ctx_len = 40 + salt_len;

    pos = ctx_len & 63;

    // append_0x80_4x4

    const u32 off = pos ^ 3;

    const u32 c0 = (off & 15) / 4;

    const u32 r0 = 0xff << ((off & 3) * 8);

    const u32 m0[4] = { ((c0 == 0) ? r0 : 0), ((c0 == 1) ? r0 : 0), ((c0 == 2) ? r0 : 0), ((c0 == 3) ? r0 : 0) };

    const u32 off16 = off / 16;

    const u32 v0[4] = { ((off16 == 0) ? 0x80808080 : 0), ((off16 == 1) ? 0x80808080 : 0), ((off16 == 2) ? 0x80808080 : 0), ((off16 == 3) ? 0x80808080 : 0) };

    w0_t |= v0[0] & m0[0];
    w1_t |= v0[0] & m0[1];
    w2_t |= v0[0] & m0[2];
    w3_t |= v0[0] & m0[3];
    w4_t |= v0[1] & m0[0];
    w5_t |= v0[1] & m0[1];
    w6_t |= v0[1] & m0[2];
    w7_t |= v0[1] & m0[3];
    w8_t |= v0[2] & m0[0];
    w9_t |= v0[2] & m0[1];
    wa_t |= v0[2] & m0[2];
    wb_t |= v0[2] & m0[3];
    wc_t |= v0[3] & m0[0];
    wd_t |= v0[3] & m0[1];
    we_t |= v0[3] & m0[2];
    wf_t |= v0[3] & m0[3];

    if (pos >= 56)
    {
      a = digest[0];
      b = digest[1];
      c = digest[2];
      d = digest[3];
      e = digest[4];

#undef K
#define K SHA1C00

      SHA1_STEP (SHA1_F0o, a, b, c, d, e, w0_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w1_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w2_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w3_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w4_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, w5_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w6_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w7_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w8_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w9_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, wa_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, wb_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, wc_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, wd_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, we_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w3_t);

#undef K
#define K SHA1C01

      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w7_t);

#undef K
#define K SHA1C02

      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, wb_t);

#undef K
#define K SHA1C03

      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wf_t);

      digest[0] += a;
      digest[1] += b;
      digest[2] += c;
      digest[3] += d;
      digest[4] += e;

      w0_t = 0;
      w1_t = 0;
      w2_t = 0;
      w3_t = 0;
      w4_t = 0;
      w5_t = 0;
      w6_t = 0;
      w7_t = 0;
      w8_t = 0;
      w9_t = 0;
      wa_t = 0;
      wb_t = 0;
      wc_t = 0;
      wd_t = 0;
      we_t = 0;
      wf_t = 0;
    }

    // last sha1 transform

    we_t = 0;
    wf_t = ctx_len * 8;

    a = digest[0];
    b = digest[1];
    c = digest[2];
    d = digest[3];
    e = digest[4];

#undef K
#define K SHA1C00

    SHA1_STEP (SHA1_F0o, a, b, c, d, e, w0_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w1_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w2_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w3_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w4_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, w5_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w6_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w7_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w8_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w9_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, wa_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, wb_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, wc_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, wd_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, we_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w3_t);

#undef K
#define K SHA1C01

    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w7_t);

#undef K
#define K SHA1C02

    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, wb_t);

#undef K
#define K SHA1C03

    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wf_t);

    b += digest[1] - make_u32x (SHA1M_B);
    c += digest[2] - make_u32x (SHA1M_C);
    d += digest[3] - make_u32x (SHA1M_D);
    e += digest[4] - make_u32x (SHA1M_E);

    COMPARE_M_SIMD (d, e, c, b);
  }
}

DECLSPEC void m04510s (PRIVATE_AS u32 *w0, PRIVATE_AS u32 *w1, PRIVATE_AS u32 *w2, PRIVATE_AS u32 *w3, const u32 pw_len, KERN_ATTR_FUNC_BASIC (), LOCAL_AS u32 * l_bin2asc)
{
  /**
   * modifiers are taken from args
   */

  /**
   * salt
   */

  u32 salt_buf0[4];
  u32 salt_buf1[4];
  u32 salt_buf2[4];
  u32 salt_buf3[4];

  salt_buf0[0] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[0]);
  salt_buf0[1] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[1]);
  salt_buf0[2] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[2]);
  salt_buf0[3] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[3]);
  salt_buf1[0] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[4]);
  salt_buf1[1] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[5]);
  salt_buf1[2] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[6]);
  salt_buf1[3] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[7]);
  salt_buf2[0] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[8]);
  salt_buf2[1] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[9]);
  salt_buf2[2] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[10]);
  salt_buf2[3] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[11]);
  salt_buf3[0] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[12]);
  salt_buf3[1] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[13]);
  salt_buf3[2] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[14]);
  salt_buf3[3] = hc_swap32_S (salt_bufs[SALT_POS_HOST].salt_buf[15]);

  const u32 salt_len = salt_bufs[SALT_POS_HOST].salt_len;

  /**
   * digest
   */

  const u32 search[4] = {
    digests_buf[DIGESTS_OFFSET_HOST].digest_buf[DGST_R0],
    digests_buf[DIGESTS_OFFSET_HOST].digest_buf[DGST_R1],
    digests_buf[DIGESTS_OFFSET_HOST].digest_buf[DGST_R2],
    digests_buf[DIGESTS_OFFSET_HOST].digest_buf[DGST_R3]
  };

  /**
   * loop
   */

  u32 w0l = w0[0];

  for (u32 il_pos = 0; il_pos < IL_CNT; il_pos += VECT_SIZE)
  {
    const u32x w0r = ix_create_bft (bfs_buf, il_pos);

    const u32x w0lr = w0l | w0r;

    /**
    * sha1
    */

    // Contains the password

    u32x w0_t = w0lr;
    u32x w1_t = w0[1];
    u32x w2_t = w0[2];
    u32x w3_t = w0[3];
    u32x w4_t = w1[0];
    u32x w5_t = w1[1];
    u32x w6_t = w1[2];
    u32x w7_t = w1[3];
    u32x w8_t = w2[0];
    u32x w9_t = w2[1];
    u32x wa_t = w2[2];
    u32x wb_t = w2[3];
    u32x wc_t = w3[0];
    u32x wd_t = w3[1];
    u32x we_t = w3[2];
    u32x wf_t = w3[3];

    // original hash state
    u32x a = SHA1M_A;
    u32x b = SHA1M_B;
    u32x c = SHA1M_C;
    u32x d = SHA1M_D;
    u32x e = SHA1M_E;

    // Compute SHA1

#undef K
#define K SHA1C00

    SHA1_STEP (SHA1_F0o, a, b, c, d, e, w0_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w1_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w2_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w3_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w4_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, w5_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w6_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w7_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w8_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w9_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, wa_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, wb_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, wc_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, wd_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, we_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w3_t);

#undef K
#define K SHA1C01

    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w7_t);

#undef K
#define K SHA1C02

    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, wb_t);

#undef K
#define K SHA1C03

    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wf_t);

    // Update sha1 state
    a += make_u32x (SHA1M_A);
    b += make_u32x (SHA1M_B);
    c += make_u32x (SHA1M_C);
    d += make_u32x (SHA1M_D);
    e += make_u32x (SHA1M_E);

    /**
    * 2nd SHA1
    */

    // Convert to ascii
    w0_t = uint_to_hex_lower8_le ((a >> 16) & 255) << 0 | uint_to_hex_lower8_le ((a >> 24) & 255) << 16;
    w1_t = uint_to_hex_lower8_le ((a >> 0) & 255) << 0 | uint_to_hex_lower8_le ((a >> 8) & 255) << 16;
    w2_t = uint_to_hex_lower8_le ((b >> 16) & 255) << 0 | uint_to_hex_lower8_le ((b >> 24) & 255) << 16;
    w3_t = uint_to_hex_lower8_le ((b >> 0) & 255) << 0 | uint_to_hex_lower8_le ((b >> 8) & 255) << 16;
    w4_t = uint_to_hex_lower8_le ((c >> 16) & 255) << 0 | uint_to_hex_lower8_le ((c >> 24) & 255) << 16;
    w5_t = uint_to_hex_lower8_le ((c >> 0) & 255) << 0 | uint_to_hex_lower8_le ((c >> 8) & 255) << 16;
    w6_t = uint_to_hex_lower8_le ((d >> 16) & 255) << 0 | uint_to_hex_lower8_le ((d >> 24) & 255) << 16;
    w7_t = uint_to_hex_lower8_le ((d >> 0) & 255) << 0 | uint_to_hex_lower8_le ((d >> 8) & 255) << 16;
    w8_t = uint_to_hex_lower8_le ((e >> 16) & 255) << 0 | uint_to_hex_lower8_le ((e >> 24) & 255) << 16;
    w9_t = uint_to_hex_lower8_le ((e >> 0) & 255) << 0 | uint_to_hex_lower8_le ((e >> 8) & 255) << 16;
    wa_t = 0;
    wb_t = 0;
    wc_t = 0;
    wd_t = 0;
    we_t = 0;
    wf_t = 0;


    u32x digest[8];

    // Reset hash state for the second computation
    a = SHA1M_A;
    b = SHA1M_B;
    c = SHA1M_C;
    d = SHA1M_D;
    e = SHA1M_E;

    digest[0] = a;
    digest[1] = b;
    digest[2] = c;
    digest[3] = d;
    digest[4] = e;

    // append salt

    // ctx_len 40, pos 40

    int pos = 40;

    u32x s0[4];
    u32x s1[4];
    u32x s2[4];
    u32x s3[4];

    s0[0] = salt_buf0[0];
    s0[1] = salt_buf0[1];
    s0[2] = salt_buf0[2];
    s0[3] = salt_buf0[3];
    s1[0] = salt_buf1[0];
    s1[1] = salt_buf1[1];
    s1[2] = salt_buf1[2];
    s1[3] = salt_buf1[3];
    s2[0] = salt_buf2[0];
    s2[1] = salt_buf2[1];
    s2[2] = salt_buf2[2];
    s2[3] = salt_buf2[3];
    s3[0] = salt_buf3[0];
    s3[1] = salt_buf3[1];
    s3[2] = salt_buf3[2];
    s3[3] = salt_buf3[3];

    // Does the whole string fit in one block (512 bits) ?
    // 512 bits block size: 64 * 8
    if ((pos + salt_len) < 64)
    {
      // Put every char of the salt after the computed ascii sha1
      switch_buffer_by_offset_be (s0, s1, s2, s3, pos);

      w0_t |= s0[0];
      w1_t |= s0[1];
      w2_t |= s0[2];
      w3_t |= s0[3];
      w4_t |= s1[0];
      w5_t |= s1[1];
      w6_t |= s1[2];
      w7_t |= s1[3];
      w8_t |= s2[0];
      w9_t |= s2[1];
      wa_t |= s2[2];
      wb_t |= s2[3];
      wc_t |= s3[0];
      wd_t |= s3[1];
      we_t |= s3[2];
      wf_t |= s3[3];
    }
    else
    {
      u32x _w0[4] = { 0 };
      u32x _w1[4] = { 0 };
      u32x _w2[4] = { 0 };
      u32x _w3[4] = { 0 };

      switch_buffer_by_offset_carry_be (s0, s1, s2, s3, _w0, _w1, _w2, _w3, pos);

      w0_t |= s0[0];
      w1_t |= s0[1];
      w2_t |= s0[2];
      w3_t |= s0[3];
      w4_t |= s1[0];
      w5_t |= s1[1];
      w6_t |= s1[2];
      w7_t |= s1[3];
      w8_t |= s2[0];
      w9_t |= s2[1];
      wa_t |= s2[2];
      wb_t |= s2[3];
      wc_t |= s3[0];
      wd_t |= s3[1];
      we_t |= s3[2];
      wf_t |= s3[3];

      // sha1 transform

#undef K
#define K SHA1C00

      SHA1_STEP (SHA1_F0o, a, b, c, d, e, w0_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w1_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w2_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w3_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w4_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, w5_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w6_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w7_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w8_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w9_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, wa_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, wb_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, wc_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, wd_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, we_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w3_t);

#undef K
#define K SHA1C01

      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w7_t);

#undef K
#define K SHA1C02

      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, wb_t);

#undef K
#define K SHA1C03

      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wf_t);

      digest[0] += a;
      digest[1] += b;
      digest[2] += c;
      digest[3] += d;
      digest[4] += e;

      w0_t = _w0[0];
      w1_t = _w0[1];
      w2_t = _w0[2];
      w3_t = _w0[3];
      w4_t = _w1[0];
      w5_t = _w1[1];
      w6_t = _w1[2];
      w7_t = _w1[3];
      w8_t = _w2[0];
      w9_t = _w2[1];
      wa_t = _w2[2];
      wb_t = _w2[3];
      wc_t = _w3[0];
      wd_t = _w3[1];
      we_t = _w3[2];
      wf_t = _w3[3];
    }

    const int ctx_len = 40 + salt_len;

    pos = ctx_len & 63;

    // append_0x80_4x4

    const u32 off = pos ^ 3;

    const u32 c0 = (off & 15) / 4;

    const u32 r0 = 0xff << ((off & 3) * 8);

    const u32 m0[4] = { ((c0 == 0) ? r0 : 0), ((c0 == 1) ? r0 : 0), ((c0 == 2) ? r0 : 0), ((c0 == 3) ? r0 : 0) };

    const u32 off16 = off / 16;

    const u32 v0[4] = { ((off16 == 0) ? 0x80808080 : 0), ((off16 == 1) ? 0x80808080 : 0), ((off16 == 2) ? 0x80808080 : 0), ((off16 == 3) ? 0x80808080 : 0) };

    w0_t |= v0[0] & m0[0];
    w1_t |= v0[0] & m0[1];
    w2_t |= v0[0] & m0[2];
    w3_t |= v0[0] & m0[3];
    w4_t |= v0[1] & m0[0];
    w5_t |= v0[1] & m0[1];
    w6_t |= v0[1] & m0[2];
    w7_t |= v0[1] & m0[3];
    w8_t |= v0[2] & m0[0];
    w9_t |= v0[2] & m0[1];
    wa_t |= v0[2] & m0[2];
    wb_t |= v0[2] & m0[3];
    wc_t |= v0[3] & m0[0];
    wd_t |= v0[3] & m0[1];
    we_t |= v0[3] & m0[2];
    wf_t |= v0[3] & m0[3];

    if (pos >= 56)
    {
      a = digest[0];
      b = digest[1];
      c = digest[2];
      d = digest[3];
      e = digest[4];

#undef K
#define K SHA1C00

      SHA1_STEP (SHA1_F0o, a, b, c, d, e, w0_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w1_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w2_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w3_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w4_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, w5_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w6_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w7_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w8_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w9_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, wa_t);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, wb_t);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, wc_t);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, wd_t);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, we_t);
      SHA1_STEP (SHA1_F0o, a, b, c, d, e, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F0o, e, a, b, c, d, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F0o, d, e, a, b, c, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F0o, c, d, e, a, b, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F0o, b, c, d, e, a, w3_t);

#undef K
#define K SHA1C01

      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w7_t);

#undef K
#define K SHA1C02

      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F2o, a, b, c, d, e, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F2o, e, a, b, c, d, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F2o, d, e, a, b, c, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F2o, c, d, e, a, b, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F2o, b, c, d, e, a, wb_t);

#undef K
#define K SHA1C03

      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, wf_t);
      w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w0_t);
      w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w1_t);
      w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w2_t);
      w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w3_t);
      w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w4_t);
      w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, w5_t);
      w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, w6_t);
      w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, w7_t);
      w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, w8_t);
      w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, w9_t);
      wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wa_t);
      wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
      SHA1_STEP (SHA1_F1, a, b, c, d, e, wb_t);
      wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
      SHA1_STEP (SHA1_F1, e, a, b, c, d, wc_t);
      wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
      SHA1_STEP (SHA1_F1, d, e, a, b, c, wd_t);
      we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
      SHA1_STEP (SHA1_F1, c, d, e, a, b, we_t);
      wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
      SHA1_STEP (SHA1_F1, b, c, d, e, a, wf_t);

      digest[0] += a;
      digest[1] += b;
      digest[2] += c;
      digest[3] += d;
      digest[4] += e;

      w0_t = 0;
      w1_t = 0;
      w2_t = 0;
      w3_t = 0;
      w4_t = 0;
      w5_t = 0;
      w6_t = 0;
      w7_t = 0;
      w8_t = 0;
      w9_t = 0;
      wa_t = 0;
      wb_t = 0;
      wc_t = 0;
      wd_t = 0;
      we_t = 0;
      wf_t = 0;
    }

    // last sha1 transform

    we_t = 0;
    wf_t = ctx_len * 8;

    a = digest[0];
    b = digest[1];
    c = digest[2];
    d = digest[3];
    e = digest[4];

#undef K
#define K SHA1C00

    SHA1_STEP (SHA1_F0o, a, b, c, d, e, w0_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w1_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w2_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w3_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w4_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, w5_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w6_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w7_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w8_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w9_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, wa_t);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, wb_t);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, wc_t);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, wd_t);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, we_t);
    SHA1_STEP (SHA1_F0o, a, b, c, d, e, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F0o, e, a, b, c, d, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F0o, d, e, a, b, c, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F0o, c, d, e, a, b, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F0o, b, c, d, e, a, w3_t);

#undef K
#define K SHA1C01

    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w7_t);

#undef K
#define K SHA1C02

    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F2o, a, b, c, d, e, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F2o, e, a, b, c, d, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F2o, d, e, a, b, c, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F2o, c, d, e, a, b, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F2o, b, c, d, e, a, wb_t);

#undef K
#define K SHA1C03

    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wd_t);
    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, wf_t);
    w0_t = hc_rotl32 ((wd_t ^ w8_t ^ w2_t ^ w0_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w0_t);
    w1_t = hc_rotl32 ((we_t ^ w9_t ^ w3_t ^ w1_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w1_t);
    w2_t = hc_rotl32 ((wf_t ^ wa_t ^ w4_t ^ w2_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w2_t);
    w3_t = hc_rotl32 ((w0_t ^ wb_t ^ w5_t ^ w3_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w3_t);
    w4_t = hc_rotl32 ((w1_t ^ wc_t ^ w6_t ^ w4_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w4_t);
    w5_t = hc_rotl32 ((w2_t ^ wd_t ^ w7_t ^ w5_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, w5_t);
    w6_t = hc_rotl32 ((w3_t ^ we_t ^ w8_t ^ w6_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, w6_t);
    w7_t = hc_rotl32 ((w4_t ^ wf_t ^ w9_t ^ w7_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, w7_t);
    w8_t = hc_rotl32 ((w5_t ^ w0_t ^ wa_t ^ w8_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, w8_t);
    w9_t = hc_rotl32 ((w6_t ^ w1_t ^ wb_t ^ w9_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, w9_t);
    wa_t = hc_rotl32 ((w7_t ^ w2_t ^ wc_t ^ wa_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wa_t);
    wb_t = hc_rotl32 ((w8_t ^ w3_t ^ wd_t ^ wb_t), 1u);
    SHA1_STEP (SHA1_F1, a, b, c, d, e, wb_t);
    wc_t = hc_rotl32 ((w9_t ^ w4_t ^ we_t ^ wc_t), 1u);
    SHA1_STEP (SHA1_F1, e, a, b, c, d, wc_t);
    wd_t = hc_rotl32 ((wa_t ^ w5_t ^ wf_t ^ wd_t), 1u);
    SHA1_STEP (SHA1_F1, d, e, a, b, c, wd_t);

    if (MATCHES_NONE_VS ((e + digest[4] - make_u32x (SHA1M_E)), search[1]))
      continue;

    we_t = hc_rotl32 ((wb_t ^ w6_t ^ w0_t ^ we_t), 1u);
    SHA1_STEP (SHA1_F1, c, d, e, a, b, we_t);
    wf_t = hc_rotl32 ((wc_t ^ w7_t ^ w1_t ^ wf_t), 1u);
    SHA1_STEP (SHA1_F1, b, c, d, e, a, wf_t);

    b += digest[1] - make_u32x (SHA1M_B);
    c += digest[2] - make_u32x (SHA1M_C);
    d += digest[3] - make_u32x (SHA1M_D);
    e += digest[4] - make_u32x (SHA1M_E);

    COMPARE_S_SIMD (d, e, c, b);
  }
}

KERNEL_FQ void m04510_m04 (KERN_ATTR_BASIC ())
{
  /**
   * base
   */

  const u64 lid = get_local_id (0);
  const u64 gid = get_global_id (0);
  const u64 lsz = get_local_size (0);

  /**
   * bin2asc table
   */

  LOCAL_VK u32 l_bin2asc[256];

  for (u32 i = lid; i < 256; i += lsz)
  {
    const u32 i0 = (i >> 0) & 15;
    const u32 i1 = (i >> 4) & 15;

    l_bin2asc[i] = ((i0 < 10) ? '0' + i0 : 'a' - 10 + i0) << 0 | ((i1 < 10) ? '0' + i1 : 'a' - 10 + i1) << 8;
  }

  SYNC_THREADS ();

  if (gid >= GID_CNT)
    return;

  /**
   * modifier
   */

  u32 w0[4];

  w0[0] = pws[gid].i[0];
  w0[1] = pws[gid].i[1];
  w0[2] = pws[gid].i[2];
  w0[3] = pws[gid].i[3];

  u32 w1[4];

  w1[0] = 0;
  w1[1] = 0;
  w1[2] = 0;
  w1[3] = 0;

  u32 w2[4];

  w2[0] = 0;
  w2[1] = 0;
  w2[2] = 0;
  w2[3] = 0;

  u32 w3[4];

  w3[0] = 0;
  w3[1] = 0;
  w3[2] = 0;
  w3[3] = pws[gid].i[15];

  const u32 pw_len = pws[gid].pw_len & 63;

  /**
   * main
   */

  m04510m (w0, w1, w2, w3, pw_len, pws, rules_buf, combs_buf, bfs_buf, tmps, hooks, bitmaps_buf_s1_a, bitmaps_buf_s1_b, bitmaps_buf_s1_c, bitmaps_buf_s1_d, bitmaps_buf_s2_a, bitmaps_buf_s2_b, bitmaps_buf_s2_c, bitmaps_buf_s2_d, plains_buf, digests_buf, hashes_shown, salt_bufs, esalt_bufs, d_return_buf, d_extra0_buf, d_extra1_buf, d_extra2_buf, d_extra3_buf, kernel_param, gid, lid, lsz, l_bin2asc);
}

KERNEL_FQ void m04510_m08 (KERN_ATTR_BASIC ())
{
  /**
   * base
   */

  const u64 lid = get_local_id (0);
  const u64 gid = get_global_id (0);
  const u64 lsz = get_local_size (0);

  /**
   * bin2asc table
   */

  LOCAL_VK u32 l_bin2asc[256];

  for (u32 i = lid; i < 256; i += lsz)
  {
    const u32 i0 = (i >> 0) & 15;
    const u32 i1 = (i >> 4) & 15;

    l_bin2asc[i] = ((i0 < 10) ? '0' + i0 : 'a' - 10 + i0) << 0 | ((i1 < 10) ? '0' + i1 : 'a' - 10 + i1) << 8;
  }

  SYNC_THREADS ();

  if (gid >= GID_CNT)
    return;

  /**
   * modifier
   */

  u32 w0[4];

  w0[0] = pws[gid].i[0];
  w0[1] = pws[gid].i[1];
  w0[2] = pws[gid].i[2];
  w0[3] = pws[gid].i[3];

  u32 w1[4];

  w1[0] = pws[gid].i[4];
  w1[1] = pws[gid].i[5];
  w1[2] = pws[gid].i[6];
  w1[3] = pws[gid].i[7];

  u32 w2[4];

  w2[0] = 0;
  w2[1] = 0;
  w2[2] = 0;
  w2[3] = 0;

  u32 w3[4];

  w3[0] = 0;
  w3[1] = 0;
  w3[2] = 0;
  w3[3] = pws[gid].i[15];

  const u32 pw_len = pws[gid].pw_len & 63;

  /**
   * main
   */

  m04510m (w0, w1, w2, w3, pw_len, pws, rules_buf, combs_buf, bfs_buf, tmps, hooks, bitmaps_buf_s1_a, bitmaps_buf_s1_b, bitmaps_buf_s1_c, bitmaps_buf_s1_d, bitmaps_buf_s2_a, bitmaps_buf_s2_b, bitmaps_buf_s2_c, bitmaps_buf_s2_d, plains_buf, digests_buf, hashes_shown, salt_bufs, esalt_bufs, d_return_buf, d_extra0_buf, d_extra1_buf, d_extra2_buf, d_extra3_buf, kernel_param, gid, lid, lsz, l_bin2asc);
}

KERNEL_FQ void m04510_m16 (KERN_ATTR_BASIC ())
{
  /**
   * base
   */

  const u64 lid = get_local_id (0);
  const u64 gid = get_global_id (0);
  const u64 lsz = get_local_size (0);

  /**
   * bin2asc table
   */

  LOCAL_VK u32 l_bin2asc[256];

  for (u32 i = lid; i < 256; i += lsz)
  {
    const u32 i0 = (i >> 0) & 15;
    const u32 i1 = (i >> 4) & 15;

    l_bin2asc[i] = ((i0 < 10) ? '0' + i0 : 'a' - 10 + i0) << 0 | ((i1 < 10) ? '0' + i1 : 'a' - 10 + i1) << 8;
  }

  SYNC_THREADS ();

  if (gid >= GID_CNT)
    return;

  /**
   * modifier
   */

  u32 w0[4];

  w0[0] = pws[gid].i[0];
  w0[1] = pws[gid].i[1];
  w0[2] = pws[gid].i[2];
  w0[3] = pws[gid].i[3];

  u32 w1[4];

  w1[0] = pws[gid].i[4];
  w1[1] = pws[gid].i[5];
  w1[2] = pws[gid].i[6];
  w1[3] = pws[gid].i[7];

  u32 w2[4];

  w2[0] = pws[gid].i[8];
  w2[1] = pws[gid].i[9];
  w2[2] = pws[gid].i[10];
  w2[3] = pws[gid].i[11];

  u32 w3[4];

  w3[0] = pws[gid].i[12];
  w3[1] = pws[gid].i[13];
  w3[2] = pws[gid].i[14];
  w3[3] = pws[gid].i[15];

  const u32 pw_len = pws[gid].pw_len & 63;

  /**
   * main
   */

  m04510m (w0, w1, w2, w3, pw_len, pws, rules_buf, combs_buf, bfs_buf, tmps, hooks, bitmaps_buf_s1_a, bitmaps_buf_s1_b, bitmaps_buf_s1_c, bitmaps_buf_s1_d, bitmaps_buf_s2_a, bitmaps_buf_s2_b, bitmaps_buf_s2_c, bitmaps_buf_s2_d, plains_buf, digests_buf, hashes_shown, salt_bufs, esalt_bufs, d_return_buf, d_extra0_buf, d_extra1_buf, d_extra2_buf, d_extra3_buf, kernel_param, gid, lid, lsz, l_bin2asc);
}

KERNEL_FQ void m04510_s04 (KERN_ATTR_BASIC ())
{
  /**
   * base
   */

  const u64 lid = get_local_id (0);
  const u64 gid = get_global_id (0);
  const u64 lsz = get_local_size (0);

  /**
   * bin2asc table
   */

  LOCAL_VK u32 l_bin2asc[256];

  for (u32 i = lid; i < 256; i += lsz)
  {
    const u32 i0 = (i >> 0) & 15;
    const u32 i1 = (i >> 4) & 15;

    l_bin2asc[i] = ((i0 < 10) ? '0' + i0 : 'a' - 10 + i0) << 0 | ((i1 < 10) ? '0' + i1 : 'a' - 10 + i1) << 8;
  }

  SYNC_THREADS ();

  if (gid >= GID_CNT)
    return;

  /**
   * modifier
   */

  u32 w0[4];

  w0[0] = pws[gid].i[0];
  w0[1] = pws[gid].i[1];
  w0[2] = pws[gid].i[2];
  w0[3] = pws[gid].i[3];

  u32 w1[4];

  w1[0] = 0;
  w1[1] = 0;
  w1[2] = 0;
  w1[3] = 0;

  u32 w2[4];

  w2[0] = 0;
  w2[1] = 0;
  w2[2] = 0;
  w2[3] = 0;

  u32 w3[4];

  w3[0] = 0;
  w3[1] = 0;
  w3[2] = 0;
  w3[3] = pws[gid].i[15];

  const u32 pw_len = pws[gid].pw_len & 63;

  /**
   * main
   */

  m04510s (w0, w1, w2, w3, pw_len, pws, rules_buf, combs_buf, bfs_buf, tmps, hooks, bitmaps_buf_s1_a, bitmaps_buf_s1_b, bitmaps_buf_s1_c, bitmaps_buf_s1_d, bitmaps_buf_s2_a, bitmaps_buf_s2_b, bitmaps_buf_s2_c, bitmaps_buf_s2_d, plains_buf, digests_buf, hashes_shown, salt_bufs, esalt_bufs, d_return_buf, d_extra0_buf, d_extra1_buf, d_extra2_buf, d_extra3_buf, kernel_param, gid, lid, lsz, l_bin2asc);
}

KERNEL_FQ void m04510_s08 (KERN_ATTR_BASIC ())
{
  /**
   * base
   */

  const u64 lid = get_local_id (0);
  const u64 gid = get_global_id (0);
  const u64 lsz = get_local_size (0);

  /**
   * bin2asc table
   */

  LOCAL_VK u32 l_bin2asc[256];

  for (u32 i = lid; i < 256; i += lsz)
  {
    const u32 i0 = (i >> 0) & 15;
    const u32 i1 = (i >> 4) & 15;

    l_bin2asc[i] = ((i0 < 10) ? '0' + i0 : 'a' - 10 + i0) << 0 | ((i1 < 10) ? '0' + i1 : 'a' - 10 + i1) << 8;
  }

  SYNC_THREADS ();

  if (gid >= GID_CNT)
    return;

  /**
   * modifier
   */

  u32 w0[4];

  w0[0] = pws[gid].i[0];
  w0[1] = pws[gid].i[1];
  w0[2] = pws[gid].i[2];
  w0[3] = pws[gid].i[3];

  u32 w1[4];

  w1[0] = pws[gid].i[4];
  w1[1] = pws[gid].i[5];
  w1[2] = pws[gid].i[6];
  w1[3] = pws[gid].i[7];

  u32 w2[4];

  w2[0] = 0;
  w2[1] = 0;
  w2[2] = 0;
  w2[3] = 0;

  u32 w3[4];

  w3[0] = 0;
  w3[1] = 0;
  w3[2] = 0;
  w3[3] = pws[gid].i[15];

  const u32 pw_len = pws[gid].pw_len & 63;

  /**
   * main
   */

  m04510s (w0, w1, w2, w3, pw_len, pws, rules_buf, combs_buf, bfs_buf, tmps, hooks, bitmaps_buf_s1_a, bitmaps_buf_s1_b, bitmaps_buf_s1_c, bitmaps_buf_s1_d, bitmaps_buf_s2_a, bitmaps_buf_s2_b, bitmaps_buf_s2_c, bitmaps_buf_s2_d, plains_buf, digests_buf, hashes_shown, salt_bufs, esalt_bufs, d_return_buf, d_extra0_buf, d_extra1_buf, d_extra2_buf, d_extra3_buf, kernel_param, gid, lid, lsz, l_bin2asc);
}

KERNEL_FQ void m04510_s16 (KERN_ATTR_BASIC ())
{
  /**
   * base
   */

  const u64 lid = get_local_id (0);
  const u64 gid = get_global_id (0);
  const u64 lsz = get_local_size (0);

  /**
   * bin2asc table
   */

  LOCAL_VK u32 l_bin2asc[256];

  for (u32 i = lid; i < 256; i += lsz)
  {
    const u32 i0 = (i >> 0) & 15;
    const u32 i1 = (i >> 4) & 15;

    l_bin2asc[i] = ((i0 < 10) ? '0' + i0 : 'a' - 10 + i0) << 0 | ((i1 < 10) ? '0' + i1 : 'a' - 10 + i1) << 8;
  }

  SYNC_THREADS ();

  if (gid >= GID_CNT)
    return;

  /**
   * modifier
   */

  u32 w0[4];

  w0[0] = pws[gid].i[0];
  w0[1] = pws[gid].i[1];
  w0[2] = pws[gid].i[2];
  w0[3] = pws[gid].i[3];

  u32 w1[4];

  w1[0] = pws[gid].i[4];
  w1[1] = pws[gid].i[5];
  w1[2] = pws[gid].i[6];
  w1[3] = pws[gid].i[7];

  u32 w2[4];

  w2[0] = pws[gid].i[8];
  w2[1] = pws[gid].i[9];
  w2[2] = pws[gid].i[10];
  w2[3] = pws[gid].i[11];

  u32 w3[4];

  w3[0] = pws[gid].i[12];
  w3[1] = pws[gid].i[13];
  w3[2] = pws[gid].i[14];
  w3[3] = pws[gid].i[15];

  const u32 pw_len = pws[gid].pw_len & 63;

  /**
   * main
   */

  m04510s (w0, w1, w2, w3, pw_len, pws, rules_buf, combs_buf, bfs_buf, tmps, hooks, bitmaps_buf_s1_a, bitmaps_buf_s1_b, bitmaps_buf_s1_c, bitmaps_buf_s1_d, bitmaps_buf_s2_a, bitmaps_buf_s2_b, bitmaps_buf_s2_c, bitmaps_buf_s2_d, plains_buf, digests_buf, hashes_shown, salt_bufs, esalt_bufs, d_return_buf, d_extra0_buf, d_extra1_buf, d_extra2_buf, d_extra3_buf, kernel_param, gid, lid, lsz, l_bin2asc);
}
