import base64
from Crypto.Cipher import AES

"""
ECB没有偏移量
"""
def pad(text):
    """
    #填充函数，使被加密数据的字节码长度是block_size的整数倍
    """
    count = len(text.encode('utf-8'))
    add = 16 - (count % 16)
    entext = text + (chr(add) * add)
    return entext.encode('utf-8')


def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')

# 加密函数
def encrypt(text,key):
    key = key.encode('utf-8')
    text = add_to_16(text)
    cryptos = AES.new(key=key, mode=AES.MODE_ECB)
    cipher_text = cryptos.encrypt(text)
    msg = str(base64.b64encode(cipher_text), encoding="utf8")
    return msg


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text,key):
    key = key.encode('utf-8')
    mode = AES.MODE_ECB
    cryptor = AES.new(key, mode)
    res = base64.decodebytes(text.encode("utf-8"))
    plain_text = cryptor.decrypt(res).decode("utf-8").rstrip('\0')
    return plain_text


if __name__ == '__main__':
    text = 'happy_new_years_2022'
    key='9999999999999999'
    #AES key must be either 16, 24, or 32 bytes long
    res = encrypt(text,key)  # 加密
    doc_text = decrypt(res,key)  # 解密
    print("加密前数据:", text)
    print("加密后数据:", res)
    print("数据解密:", doc_text)
