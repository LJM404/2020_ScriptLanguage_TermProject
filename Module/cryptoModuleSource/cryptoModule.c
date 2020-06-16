#include <memory.h>
#include <malloc.h>
#include <string.h>
#include "aes.h"

#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define MAX(a, b) (((a) > (b)) ? (a) : (b))

size_t aesBufSize = 0;
uint8_t* aesBuf = NULL;
uint8_t* aesKey = NULL;
uint8_t* aesIv  = NULL;

// 모듈 테스트용 함수
const char* helloworld()
{
    return "Hello World";
}


// AES CBC모드를 사용하기 위한 Context를 설정하는 함수
void setupAESCBCMode(const char* buf, const char* key, const char* iv)
{
    aesBufSize = (strlen(buf) % AES_BLOCKLEN == 0) ? strlen(buf) : AES_BLOCKLEN * ((int)(strlen(buf) / AES_BLOCKLEN) + 1);
    aesBuf = malloc(aesBufSize);
    memset(aesBuf, 0, sizeof(uint8_t) * aesBufSize);
    memcpy(aesBuf, buf,  sizeof(uint8_t) * strlen(buf));

    aesKey = malloc(AES_KEYLEN);
    memset(aesKey, 0, sizeof(uint8_t) * AES_KEYLEN);
    memcpy(aesKey, key, sizeof(uint8_t) * MIN(strlen(key), AES_KEYLEN));

    aesIv = malloc(AES_BLOCKLEN);
    memset(aesIv, 0, sizeof(uint8_t) * AES_BLOCKLEN);
    memcpy(aesIv, iv, sizeof(uint8_t) * MIN(strlen(iv), AES_BLOCKLEN));
}


// AES CBC모드를 사용하기 위해 설정된 Context를 제거하는 함수
void clearAESCBCMode()
{
    if (aesBuf)
    {
        free((void*)aesBuf);
        aesBuf = NULL;
        aesBufSize = 0;
    }

    if (aesKey)
    {
        free((void*)aesKey);
        aesKey = NULL;
    }

    if (aesIv)
    {
        free((void*)aesIv);
        aesIv = NULL;
    }
}


// 버퍼를 AES CBC모드로 암호화 하는 함수
// Tiny AES libaray를 이용함.
const char* encryptBufAESCBCMode()
{
    if (aesBuf && aesKey && aesIv)
    {
        struct AES_ctx ctx;
        AES_init_ctx_iv(&ctx, aesKey, aesIv);
        AES_CBC_encrypt_buffer(&ctx, aesBuf, aesBufSize);
        return aesBuf;
    }
    else
        return NULL;
}


// 버퍼를 AES CBC모드로 복호화 하는 함수
// Tiny AES libaray를 이용함.
const char* decryptBufAESCBCMode()
{
    if (aesBuf && aesKey && aesIv)
    {
        struct AES_ctx ctx;
        AES_init_ctx_iv(&ctx, aesKey, aesIv);
        AES_CBC_decrypt_buffer(&ctx, aesBuf, aesBufSize);
        return aesBuf;
    }
    else
        return NULL;
}