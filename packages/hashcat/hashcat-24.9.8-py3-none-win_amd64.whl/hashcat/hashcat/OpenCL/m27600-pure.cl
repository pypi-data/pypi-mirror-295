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
#include M2S(INCLUDE_PATH/inc_hash_sha256.cl)
#include M2S(INCLUDE_PATH/inc_cipher_aes.cl)
#endif

#define COMPARE_M M2S(INCLUDE_PATH/inc_comp_multi.cl)

typedef struct vbox
{
  u32 salt1_buf[64];
  u32 salt1_len;
  u32 aes_key_len;
  u32 enc_pass_buf[128];
  u32 salt2_buf[64];
  u32 salt2_len;

} vbox_t;

typedef struct pbkdf2_sha256_tmp
{
  u32  ipad[8];
  u32  opad[8];

  u32  dgst[64];
  u32  out[64];

} pbkdf2_sha256_tmp_t;

DECLSPEC void hmac_sha256_run_V (PRIVATE_AS u32x *w0, PRIVATE_AS u32x *w1, PRIVATE_AS u32x *w2, PRIVATE_AS u32x *w3, PRIVATE_AS u32x *ipad, PRIVATE_AS u32x *opad, PRIVATE_AS u32x *digest)
{
  digest[0] = ipad[0];
  digest[1] = ipad[1];
  digest[2] = ipad[2];
  digest[3] = ipad[3];
  digest[4] = ipad[4];
  digest[5] = ipad[5];
  digest[6] = ipad[6];
  digest[7] = ipad[7];

  sha256_transform_vector (w0, w1, w2, w3, digest);

  w0[0] = digest[0];
  w0[1] = digest[1];
  w0[2] = digest[2];
  w0[3] = digest[3];
  w1[0] = digest[4];
  w1[1] = digest[5];
  w1[2] = digest[6];
  w1[3] = digest[7];
  w2[0] = 0x80000000;
  w2[1] = 0;
  w2[2] = 0;
  w2[3] = 0;
  w3[0] = 0;
  w3[1] = 0;
  w3[2] = 0;
  w3[3] = (64 + 32) * 8;

  digest[0] = opad[0];
  digest[1] = opad[1];
  digest[2] = opad[2];
  digest[3] = opad[3];
  digest[4] = opad[4];
  digest[5] = opad[5];
  digest[6] = opad[6];
  digest[7] = opad[7];

  sha256_transform_vector (w0, w1, w2, w3, digest);
}

DECLSPEC void xts_mul2 (PRIVATE_AS u32 *in, PRIVATE_AS u32 *out)
{
  const u32 c = in[3] >> 31;

  out[3] = (in[3] << 1) | (in[2] >> 31);
  out[2] = (in[2] << 1) | (in[1] >> 31);
  out[1] = (in[1] << 1) | (in[0] >> 31);
  out[0] = (in[0] << 1);

  out[0] ^= c * 0x87;
}

KERNEL_FQ void m27600_init (KERN_ATTR_TMPS_ESALT (pbkdf2_sha256_tmp_t, vbox_t))
{
  /**
   * base
   */

  const u64 gid = get_global_id (0);

  if (gid >= GID_CNT) return;

  sha256_hmac_ctx_t sha256_hmac_ctx;

  sha256_hmac_init_global_swap (&sha256_hmac_ctx, pws[gid].i, pws[gid].pw_len);

  tmps[gid].ipad[0] = sha256_hmac_ctx.ipad.h[0];
  tmps[gid].ipad[1] = sha256_hmac_ctx.ipad.h[1];
  tmps[gid].ipad[2] = sha256_hmac_ctx.ipad.h[2];
  tmps[gid].ipad[3] = sha256_hmac_ctx.ipad.h[3];
  tmps[gid].ipad[4] = sha256_hmac_ctx.ipad.h[4];
  tmps[gid].ipad[5] = sha256_hmac_ctx.ipad.h[5];
  tmps[gid].ipad[6] = sha256_hmac_ctx.ipad.h[6];
  tmps[gid].ipad[7] = sha256_hmac_ctx.ipad.h[7];

  tmps[gid].opad[0] = sha256_hmac_ctx.opad.h[0];
  tmps[gid].opad[1] = sha256_hmac_ctx.opad.h[1];
  tmps[gid].opad[2] = sha256_hmac_ctx.opad.h[2];
  tmps[gid].opad[3] = sha256_hmac_ctx.opad.h[3];
  tmps[gid].opad[4] = sha256_hmac_ctx.opad.h[4];
  tmps[gid].opad[5] = sha256_hmac_ctx.opad.h[5];
  tmps[gid].opad[6] = sha256_hmac_ctx.opad.h[6];
  tmps[gid].opad[7] = sha256_hmac_ctx.opad.h[7];

  sha256_hmac_update_global_swap (&sha256_hmac_ctx, esalt_bufs[DIGESTS_OFFSET_HOST].salt1_buf, esalt_bufs[DIGESTS_OFFSET_HOST].salt1_len);

  for (u32 i = 0, j = 1; i < 16; i += 8, j += 1)
  {
    sha256_hmac_ctx_t sha256_hmac_ctx2 = sha256_hmac_ctx;

    u32 w0[4];
    u32 w1[4];
    u32 w2[4];
    u32 w3[4];

    w0[0] = j;
    w0[1] = 0;
    w0[2] = 0;
    w0[3] = 0;
    w1[0] = 0;
    w1[1] = 0;
    w1[2] = 0;
    w1[3] = 0;
    w2[0] = 0;
    w2[1] = 0;
    w2[2] = 0;
    w2[3] = 0;
    w3[0] = 0;
    w3[1] = 0;
    w3[2] = 0;
    w3[3] = 0;

    sha256_hmac_update_64 (&sha256_hmac_ctx2, w0, w1, w2, w3, 4);

    sha256_hmac_final (&sha256_hmac_ctx2);

    tmps[gid].dgst[i + 0] = sha256_hmac_ctx2.opad.h[0];
    tmps[gid].dgst[i + 1] = sha256_hmac_ctx2.opad.h[1];
    tmps[gid].dgst[i + 2] = sha256_hmac_ctx2.opad.h[2];
    tmps[gid].dgst[i + 3] = sha256_hmac_ctx2.opad.h[3];
    tmps[gid].dgst[i + 4] = sha256_hmac_ctx2.opad.h[4];
    tmps[gid].dgst[i + 5] = sha256_hmac_ctx2.opad.h[5];
    tmps[gid].dgst[i + 6] = sha256_hmac_ctx2.opad.h[6];
    tmps[gid].dgst[i + 7] = sha256_hmac_ctx2.opad.h[7];

    tmps[gid].out[i + 0] = tmps[gid].dgst[i + 0];
    tmps[gid].out[i + 1] = tmps[gid].dgst[i + 1];
    tmps[gid].out[i + 2] = tmps[gid].dgst[i + 2];
    tmps[gid].out[i + 3] = tmps[gid].dgst[i + 3];
    tmps[gid].out[i + 4] = tmps[gid].dgst[i + 4];
    tmps[gid].out[i + 5] = tmps[gid].dgst[i + 5];
    tmps[gid].out[i + 6] = tmps[gid].dgst[i + 6];
    tmps[gid].out[i + 7] = tmps[gid].dgst[i + 7];
  }
}

KERNEL_FQ void m27600_loop (KERN_ATTR_TMPS_ESALT (pbkdf2_sha256_tmp_t, vbox_t))
{
  const u64 gid = get_global_id (0);

  if ((gid * VECT_SIZE) >= GID_CNT) return;

  u32x ipad[8];
  u32x opad[8];

  ipad[0] = packv (tmps, ipad, gid, 0);
  ipad[1] = packv (tmps, ipad, gid, 1);
  ipad[2] = packv (tmps, ipad, gid, 2);
  ipad[3] = packv (tmps, ipad, gid, 3);
  ipad[4] = packv (tmps, ipad, gid, 4);
  ipad[5] = packv (tmps, ipad, gid, 5);
  ipad[6] = packv (tmps, ipad, gid, 6);
  ipad[7] = packv (tmps, ipad, gid, 7);

  opad[0] = packv (tmps, opad, gid, 0);
  opad[1] = packv (tmps, opad, gid, 1);
  opad[2] = packv (tmps, opad, gid, 2);
  opad[3] = packv (tmps, opad, gid, 3);
  opad[4] = packv (tmps, opad, gid, 4);
  opad[5] = packv (tmps, opad, gid, 5);
  opad[6] = packv (tmps, opad, gid, 6);
  opad[7] = packv (tmps, opad, gid, 7);

  for (u32 i = 0; i < 16; i += 8)
  {
    u32x dgst[8];
    u32x out[8];

    dgst[0] = packv (tmps, dgst, gid, i + 0);
    dgst[1] = packv (tmps, dgst, gid, i + 1);
    dgst[2] = packv (tmps, dgst, gid, i + 2);
    dgst[3] = packv (tmps, dgst, gid, i + 3);
    dgst[4] = packv (tmps, dgst, gid, i + 4);
    dgst[5] = packv (tmps, dgst, gid, i + 5);
    dgst[6] = packv (tmps, dgst, gid, i + 6);
    dgst[7] = packv (tmps, dgst, gid, i + 7);

    out[0] = packv (tmps, out, gid, i + 0);
    out[1] = packv (tmps, out, gid, i + 1);
    out[2] = packv (tmps, out, gid, i + 2);
    out[3] = packv (tmps, out, gid, i + 3);
    out[4] = packv (tmps, out, gid, i + 4);
    out[5] = packv (tmps, out, gid, i + 5);
    out[6] = packv (tmps, out, gid, i + 6);
    out[7] = packv (tmps, out, gid, i + 7);

    for (u32 j = 0; j < LOOP_CNT; j++)
    {
      u32x w0[4];
      u32x w1[4];
      u32x w2[4];
      u32x w3[4];

      w0[0] = dgst[0];
      w0[1] = dgst[1];
      w0[2] = dgst[2];
      w0[3] = dgst[3];
      w1[0] = dgst[4];
      w1[1] = dgst[5];
      w1[2] = dgst[6];
      w1[3] = dgst[7];
      w2[0] = 0x80000000;
      w2[1] = 0;
      w2[2] = 0;
      w2[3] = 0;
      w3[0] = 0;
      w3[1] = 0;
      w3[2] = 0;
      w3[3] = (64 + 32) * 8;

      hmac_sha256_run_V (w0, w1, w2, w3, ipad, opad, dgst);

      out[0] ^= dgst[0];
      out[1] ^= dgst[1];
      out[2] ^= dgst[2];
      out[3] ^= dgst[3];
      out[4] ^= dgst[4];
      out[5] ^= dgst[5];
      out[6] ^= dgst[6];
      out[7] ^= dgst[7];
    }

    unpackv (tmps, dgst, gid, i + 0, dgst[0]);
    unpackv (tmps, dgst, gid, i + 1, dgst[1]);
    unpackv (tmps, dgst, gid, i + 2, dgst[2]);
    unpackv (tmps, dgst, gid, i + 3, dgst[3]);
    unpackv (tmps, dgst, gid, i + 4, dgst[4]);
    unpackv (tmps, dgst, gid, i + 5, dgst[5]);
    unpackv (tmps, dgst, gid, i + 6, dgst[6]);
    unpackv (tmps, dgst, gid, i + 7, dgst[7]);

    unpackv (tmps, out, gid, i + 0, out[0]);
    unpackv (tmps, out, gid, i + 1, out[1]);
    unpackv (tmps, out, gid, i + 2, out[2]);
    unpackv (tmps, out, gid, i + 3, out[3]);
    unpackv (tmps, out, gid, i + 4, out[4]);
    unpackv (tmps, out, gid, i + 5, out[5]);
    unpackv (tmps, out, gid, i + 6, out[6]);
    unpackv (tmps, out, gid, i + 7, out[7]);
  }
}

KERNEL_FQ void m27600_init2 (KERN_ATTR_TMPS_ESALT (pbkdf2_sha256_tmp_t, vbox_t))
{
  const u64 gid = get_global_id (0);
  const u64 lid = get_local_id (0);
  const u64 lsz = get_local_size (0);

  /**
   * aes shared
   */

  #ifdef REAL_SHM

  LOCAL_VK u32 s_td0[256];
  LOCAL_VK u32 s_td1[256];
  LOCAL_VK u32 s_td2[256];
  LOCAL_VK u32 s_td3[256];
  LOCAL_VK u32 s_td4[256];

  LOCAL_VK u32 s_te0[256];
  LOCAL_VK u32 s_te1[256];
  LOCAL_VK u32 s_te2[256];
  LOCAL_VK u32 s_te3[256];
  LOCAL_VK u32 s_te4[256];

  for (u32 i = lid; i < 256; i += lsz)
  {
    s_td0[i] = td0[i];
    s_td1[i] = td1[i];
    s_td2[i] = td2[i];
    s_td3[i] = td3[i];
    s_td4[i] = td4[i];

    s_te0[i] = te0[i];
    s_te1[i] = te1[i];
    s_te2[i] = te2[i];
    s_te3[i] = te3[i];
    s_te4[i] = te4[i];
  }

  SYNC_THREADS ();

  #else

  CONSTANT_AS u32a *s_td0 = td0;
  CONSTANT_AS u32a *s_td1 = td1;
  CONSTANT_AS u32a *s_td2 = td2;
  CONSTANT_AS u32a *s_td3 = td3;
  CONSTANT_AS u32a *s_td4 = td4;

  CONSTANT_AS u32a *s_te0 = te0;
  CONSTANT_AS u32a *s_te1 = te1;
  CONSTANT_AS u32a *s_te2 = te2;
  CONSTANT_AS u32a *s_te3 = te3;
  CONSTANT_AS u32a *s_te4 = te4;

  #endif

  if (gid >= GID_CNT) return;

  /**
   * aes
   */

  u32 ukey1[8];
  u32 ukey2[8];

  ukey1[0] = tmps[gid].out[ 0];
  ukey1[1] = tmps[gid].out[ 1];
  ukey1[2] = tmps[gid].out[ 2];
  ukey1[3] = tmps[gid].out[ 3];
  ukey1[4] = tmps[gid].out[ 4];
  ukey1[5] = tmps[gid].out[ 5];
  ukey1[6] = tmps[gid].out[ 6];
  ukey1[7] = tmps[gid].out[ 7];

  ukey2[0] = tmps[gid].out[ 8];
  ukey2[1] = tmps[gid].out[ 9];
  ukey2[2] = tmps[gid].out[10];
  ukey2[3] = tmps[gid].out[11];
  ukey2[4] = tmps[gid].out[12];
  ukey2[5] = tmps[gid].out[13];
  ukey2[6] = tmps[gid].out[14];
  ukey2[7] = tmps[gid].out[15];

  ukey1[0] = hc_swap32_S (ukey1[0]);
  ukey1[1] = hc_swap32_S (ukey1[1]);
  ukey1[2] = hc_swap32_S (ukey1[2]);
  ukey1[3] = hc_swap32_S (ukey1[3]);
  ukey1[4] = hc_swap32_S (ukey1[4]);
  ukey1[5] = hc_swap32_S (ukey1[5]);
  ukey1[6] = hc_swap32_S (ukey1[6]);
  ukey1[7] = hc_swap32_S (ukey1[7]);

  ukey2[0] = hc_swap32_S (ukey2[0]);
  ukey2[1] = hc_swap32_S (ukey2[1]);
  ukey2[2] = hc_swap32_S (ukey2[2]);
  ukey2[3] = hc_swap32_S (ukey2[3]);
  ukey2[4] = hc_swap32_S (ukey2[4]);
  ukey2[5] = hc_swap32_S (ukey2[5]);
  ukey2[6] = hc_swap32_S (ukey2[6]);
  ukey2[7] = hc_swap32_S (ukey2[7]);

  u32 ks[60];

  u32 aes_decrypt[16];

  // first block

  u32 in[4];

  in[0] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[0];
  in[1] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[1];
  in[2] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[2];
  in[3] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[3];

  u32 out[4];

  out[0] = in[0];
  out[1] = in[1];
  out[2] = in[2];
  out[3] = in[3];

  u32 S[4] = { 0 }; // tweak, 16 x 0x00
  u32 T[4] = { 0 };

  aes256_set_encrypt_key (ks, ukey2, s_te0, s_te1, s_te2, s_te3);
  aes256_encrypt (ks, S, T, s_te0, s_te1, s_te2, s_te3, s_te4);

  out[0] ^= T[0];
  out[1] ^= T[1];
  out[2] ^= T[2];
  out[3] ^= T[3];

  aes256_set_decrypt_key (ks, ukey1, s_te0, s_te1, s_te2, s_te3, s_td0, s_td1, s_td2, s_td3);
  aes256_decrypt (ks, out, out, s_td0, s_td1, s_td2, s_td3, s_td4);

  out[0] ^= T[0];
  out[1] ^= T[1];
  out[2] ^= T[2];
  out[3] ^= T[3];

  aes_decrypt[0] = out[0];
  aes_decrypt[1] = out[1];
  aes_decrypt[2] = out[2];
  aes_decrypt[3] = out[3];

  // next

  in[0] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[4];
  in[1] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[5];
  in[2] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[6];
  in[3] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[7];

  out[0] = in[0];
  out[1] = in[1];
  out[2] = in[2];
  out[3] = in[3];

  xts_mul2 (T, T);

  out[0] ^= T[0];
  out[1] ^= T[1];
  out[2] ^= T[2];
  out[3] ^= T[3];

  aes256_decrypt (ks, out, out, s_td0, s_td1, s_td2, s_td3, s_td4);

  out[0] ^= T[0];
  out[1] ^= T[1];
  out[2] ^= T[2];
  out[3] ^= T[3];

  aes_decrypt[4] = out[0];
  aes_decrypt[5] = out[1];
  aes_decrypt[6] = out[2];
  aes_decrypt[7] = out[3];

  // next

  in[0] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[8];
  in[1] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[9];
  in[2] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[10];
  in[3] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[11];

  out[0] = in[0];
  out[1] = in[1];
  out[2] = in[2];
  out[3] = in[3];

  xts_mul2 (T, T);

  out[0] ^= T[0];
  out[1] ^= T[1];
  out[2] ^= T[2];
  out[3] ^= T[3];

  aes256_decrypt (ks, out, out, s_td0, s_td1, s_td2, s_td3, s_td4);

  out[0] ^= T[0];
  out[1] ^= T[1];
  out[2] ^= T[2];
  out[3] ^= T[3];

  aes_decrypt[8] = out[0];
  aes_decrypt[9] = out[1];
  aes_decrypt[10] = out[2];
  aes_decrypt[11] = out[3];

  // next

  in[0] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[12];
  in[1] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[13];
  in[2] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[14];
  in[3] = esalt_bufs[DIGESTS_OFFSET_HOST].enc_pass_buf[15];

  out[0] = in[0];
  out[1] = in[1];
  out[2] = in[2];
  out[3] = in[3];

  xts_mul2 (T, T);

  out[0] ^= T[0];
  out[1] ^= T[1];
  out[2] ^= T[2];
  out[3] ^= T[3];

  aes256_decrypt (ks, out, out, s_td0, s_td1, s_td2, s_td3, s_td4);

  out[0] ^= T[0];
  out[1] ^= T[1];
  out[2] ^= T[2];
  out[3] ^= T[3];

  aes_decrypt[12] = out[0];
  aes_decrypt[13] = out[1];
  aes_decrypt[14] = out[2];
  aes_decrypt[15] = out[3];

  // pbkdf2-hmac-sha256

  u32 w0[4];
  u32 w1[4];
  u32 w2[4];
  u32 w3[4];

  w0[0] = hc_swap32_S (aes_decrypt[ 0]);
  w0[1] = hc_swap32_S (aes_decrypt[ 1]);
  w0[2] = hc_swap32_S (aes_decrypt[ 2]);
  w0[3] = hc_swap32_S (aes_decrypt[ 3]);
  w1[0] = hc_swap32_S (aes_decrypt[ 4]);
  w1[1] = hc_swap32_S (aes_decrypt[ 5]);
  w1[2] = hc_swap32_S (aes_decrypt[ 6]);
  w1[3] = hc_swap32_S (aes_decrypt[ 7]);
  w2[0] = hc_swap32_S (aes_decrypt[ 8]);
  w2[1] = hc_swap32_S (aes_decrypt[ 9]);
  w2[2] = hc_swap32_S (aes_decrypt[10]);
  w2[3] = hc_swap32_S (aes_decrypt[11]);
  w3[0] = hc_swap32_S (aes_decrypt[12]);
  w3[1] = hc_swap32_S (aes_decrypt[13]);
  w3[2] = hc_swap32_S (aes_decrypt[14]);
  w3[3] = hc_swap32_S (aes_decrypt[15]);

  // init2

  sha256_hmac_ctx_t sha256_hmac_ctx;

  sha256_hmac_init_64 (&sha256_hmac_ctx, w0, w1, w2, w3);

  tmps[gid].ipad[0] = sha256_hmac_ctx.ipad.h[0];
  tmps[gid].ipad[1] = sha256_hmac_ctx.ipad.h[1];
  tmps[gid].ipad[2] = sha256_hmac_ctx.ipad.h[2];
  tmps[gid].ipad[3] = sha256_hmac_ctx.ipad.h[3];
  tmps[gid].ipad[4] = sha256_hmac_ctx.ipad.h[4];
  tmps[gid].ipad[5] = sha256_hmac_ctx.ipad.h[5];
  tmps[gid].ipad[6] = sha256_hmac_ctx.ipad.h[6];
  tmps[gid].ipad[7] = sha256_hmac_ctx.ipad.h[7];

  tmps[gid].opad[0] = sha256_hmac_ctx.opad.h[0];
  tmps[gid].opad[1] = sha256_hmac_ctx.opad.h[1];
  tmps[gid].opad[2] = sha256_hmac_ctx.opad.h[2];
  tmps[gid].opad[3] = sha256_hmac_ctx.opad.h[3];
  tmps[gid].opad[4] = sha256_hmac_ctx.opad.h[4];
  tmps[gid].opad[5] = sha256_hmac_ctx.opad.h[5];
  tmps[gid].opad[6] = sha256_hmac_ctx.opad.h[6];
  tmps[gid].opad[7] = sha256_hmac_ctx.opad.h[7];

  sha256_hmac_update_global_swap (&sha256_hmac_ctx, esalt_bufs[DIGESTS_OFFSET_HOST].salt2_buf, esalt_bufs[DIGESTS_OFFSET_HOST].salt2_len);

  for (u32 i = 0, j = 1; i < 8; i += 8, j += 1)
  {
    sha256_hmac_ctx_t sha256_hmac_ctx2 = sha256_hmac_ctx;

    w0[0] = j;
    w0[1] = 0;
    w0[2] = 0;
    w0[3] = 0;
    w1[0] = 0;
    w1[1] = 0;
    w1[2] = 0;
    w1[3] = 0;
    w2[0] = 0;
    w2[1] = 0;
    w2[2] = 0;
    w2[3] = 0;
    w3[0] = 0;
    w3[1] = 0;
    w3[2] = 0;
    w3[3] = 0;

    sha256_hmac_update_64 (&sha256_hmac_ctx2, w0, w1, w2, w3, 4);

    sha256_hmac_final (&sha256_hmac_ctx2);

    tmps[gid].dgst[i + 0] = sha256_hmac_ctx2.opad.h[0];
    tmps[gid].dgst[i + 1] = sha256_hmac_ctx2.opad.h[1];
    tmps[gid].dgst[i + 2] = sha256_hmac_ctx2.opad.h[2];
    tmps[gid].dgst[i + 3] = sha256_hmac_ctx2.opad.h[3];
    tmps[gid].dgst[i + 4] = sha256_hmac_ctx2.opad.h[4];
    tmps[gid].dgst[i + 5] = sha256_hmac_ctx2.opad.h[5];
    tmps[gid].dgst[i + 6] = sha256_hmac_ctx2.opad.h[6];
    tmps[gid].dgst[i + 7] = sha256_hmac_ctx2.opad.h[7];

    tmps[gid].out[i + 0] = tmps[gid].dgst[i + 0];
    tmps[gid].out[i + 1] = tmps[gid].dgst[i + 1];
    tmps[gid].out[i + 2] = tmps[gid].dgst[i + 2];
    tmps[gid].out[i + 3] = tmps[gid].dgst[i + 3];
    tmps[gid].out[i + 4] = tmps[gid].dgst[i + 4];
    tmps[gid].out[i + 5] = tmps[gid].dgst[i + 5];
    tmps[gid].out[i + 6] = tmps[gid].dgst[i + 6];
    tmps[gid].out[i + 7] = tmps[gid].dgst[i + 7];
  }
}

KERNEL_FQ void m27600_loop2 (KERN_ATTR_TMPS_ESALT (pbkdf2_sha256_tmp_t, vbox_t))
{
  const u64 gid = get_global_id (0);

  if ((gid * VECT_SIZE) >= GID_CNT) return;

  u32x ipad[8];
  u32x opad[8];

  ipad[0] = packv (tmps, ipad, gid, 0);
  ipad[1] = packv (tmps, ipad, gid, 1);
  ipad[2] = packv (tmps, ipad, gid, 2);
  ipad[3] = packv (tmps, ipad, gid, 3);
  ipad[4] = packv (tmps, ipad, gid, 4);
  ipad[5] = packv (tmps, ipad, gid, 5);
  ipad[6] = packv (tmps, ipad, gid, 6);
  ipad[7] = packv (tmps, ipad, gid, 7);

  opad[0] = packv (tmps, opad, gid, 0);
  opad[1] = packv (tmps, opad, gid, 1);
  opad[2] = packv (tmps, opad, gid, 2);
  opad[3] = packv (tmps, opad, gid, 3);
  opad[4] = packv (tmps, opad, gid, 4);
  opad[5] = packv (tmps, opad, gid, 5);
  opad[6] = packv (tmps, opad, gid, 6);
  opad[7] = packv (tmps, opad, gid, 7);

  for (u32 i = 0; i < 8; i += 8)
  {
    u32x dgst[8];
    u32x out[8];

    dgst[0] = packv (tmps, dgst, gid, i + 0);
    dgst[1] = packv (tmps, dgst, gid, i + 1);
    dgst[2] = packv (tmps, dgst, gid, i + 2);
    dgst[3] = packv (tmps, dgst, gid, i + 3);
    dgst[4] = packv (tmps, dgst, gid, i + 4);
    dgst[5] = packv (tmps, dgst, gid, i + 5);
    dgst[6] = packv (tmps, dgst, gid, i + 6);
    dgst[7] = packv (tmps, dgst, gid, i + 7);

    out[0] = packv (tmps, out, gid, i + 0);
    out[1] = packv (tmps, out, gid, i + 1);
    out[2] = packv (tmps, out, gid, i + 2);
    out[3] = packv (tmps, out, gid, i + 3);
    out[4] = packv (tmps, out, gid, i + 4);
    out[5] = packv (tmps, out, gid, i + 5);
    out[6] = packv (tmps, out, gid, i + 6);
    out[7] = packv (tmps, out, gid, i + 7);

    for (u32 j = 0; j < LOOP_CNT; j++)
    {
      u32x w0[4];
      u32x w1[4];
      u32x w2[4];
      u32x w3[4];

      w0[0] = dgst[0];
      w0[1] = dgst[1];
      w0[2] = dgst[2];
      w0[3] = dgst[3];
      w1[0] = dgst[4];
      w1[1] = dgst[5];
      w1[2] = dgst[6];
      w1[3] = dgst[7];
      w2[0] = 0x80000000;
      w2[1] = 0;
      w2[2] = 0;
      w2[3] = 0;
      w3[0] = 0;
      w3[1] = 0;
      w3[2] = 0;
      w3[3] = (64 + 32) * 8;

      hmac_sha256_run_V (w0, w1, w2, w3, ipad, opad, dgst);

      out[0] ^= dgst[0];
      out[1] ^= dgst[1];
      out[2] ^= dgst[2];
      out[3] ^= dgst[3];
      out[4] ^= dgst[4];
      out[5] ^= dgst[5];
      out[6] ^= dgst[6];
      out[7] ^= dgst[7];
    }

    unpackv (tmps, dgst, gid, i + 0, dgst[0]);
    unpackv (tmps, dgst, gid, i + 1, dgst[1]);
    unpackv (tmps, dgst, gid, i + 2, dgst[2]);
    unpackv (tmps, dgst, gid, i + 3, dgst[3]);
    unpackv (tmps, dgst, gid, i + 4, dgst[4]);
    unpackv (tmps, dgst, gid, i + 5, dgst[5]);
    unpackv (tmps, dgst, gid, i + 6, dgst[6]);
    unpackv (tmps, dgst, gid, i + 7, dgst[7]);

    unpackv (tmps, out, gid, i + 0, out[0]);
    unpackv (tmps, out, gid, i + 1, out[1]);
    unpackv (tmps, out, gid, i + 2, out[2]);
    unpackv (tmps, out, gid, i + 3, out[3]);
    unpackv (tmps, out, gid, i + 4, out[4]);
    unpackv (tmps, out, gid, i + 5, out[5]);
    unpackv (tmps, out, gid, i + 6, out[6]);
    unpackv (tmps, out, gid, i + 7, out[7]);
  }
}

KERNEL_FQ void m27600_comp (KERN_ATTR_TMPS_ESALT (pbkdf2_sha256_tmp_t, vbox_t))
{
  const u64 gid = get_global_id (0);

  if (gid >= GID_CNT) return;

  const u32 r0 = tmps[gid].out[0];
  const u32 r1 = tmps[gid].out[1];
  const u32 r2 = tmps[gid].out[2];
  const u32 r3 = tmps[gid].out[3];

  #define il_pos 0

  #ifdef KERNEL_STATIC
  #include COMPARE_M
  #endif
}
