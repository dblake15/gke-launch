import docker
import os
import logging
import subprocess
logging.basicConfig(filename="test.log", format='%(levelname)s: %(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def main():
    subprocess.run(['sudo','gcloud', 'auth', 'login'])
#     print("before client")
#     client = docker.from_env()
#     print("after client")

#     tag = "gcr.io/conductive-fold-275020/fail:latest"
#     client.images.build(path="../frontend/", rm=True, tag=tag, platform='amd64')
#     # filename = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
#     #f = open("/Users/dylanblake/key.json", "r")
#     key = {
#   "type": "service_account",
#   "project_id": "conductive-fold-275020",
#   "private_key_id": "8a604843199537386d198b059ffb88f497eff353",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDWameK/PWMnvCc\n7NkHjaeVNaIbEhFgcBq5IQebUFhRXtfKCrvhCDqN1HlfuSTHUJMwJTxy6QXsPCtZ\n3zDuBcgFid3PMqIO1mlN0OHtWlLUzlk67SvCyuBf4S5UscreHwdlALcd82Zc/6bM\npzZ5pB+rhCuTn+WNQRWhWSVwggSjx9c8H/kCzocR8nATqcm1Wk0qUVxK8gJBFI8v\nK/GcPGae7MpY2EO9M0flsDCLm+iUkbz8MQDaoC3Qvt4V3dq184DnX4AfLM74BII7\n+JkTW17wcqi5jdQrj1qeiyoGeapYSPftIh6ZA1iuBFPEkAn+Kig389n2mbXOxEkc\nsanUD/5vAgMBAAECggEACkKlBLClgMW4Fo+ll/Ka081jHexJhweLoZpHlMtqBaEG\nIHzdAdj02Mzap86ND6tML9HzAVp5DxV6dgkQQ5HWlmcKMBwvnG19F90vl9pqUPht\njjxuGYyGqijKhDnqsoW3mFBJ5MB2AIia3VDkcldD6Zg8jENcptuprW2vptpJCXFC\nWPVZzid5D7Fgd3a5WzQgdRNFo66jVUxpakoCjPGeL4oje+YI9NVS4KW5lFKwk/Ac\nE+QX0FbzwfkaCqtB9MQifRslJUUyqpPJJ/75GOS40O0229Ovhcyu0DxZ1nUpDWNB\nEkxsJzB1lshzwpF+b+7oGyztSfAJ9xuI8/xSW4C5cQKBgQD3pGqXFeZV0hwFMv6K\nqkqOIegWBli54X1PB8pyVArktgLz+lP78YtxhzPdimoacBlB6j5CUywaTmZzlPmQ\nDs72xQ5MCfm/2QJeNNGWh7h3j+4E949CUDNXg/LgSj9zkOGaww0KZ0PNAOUTCoXY\n4KaXHKp//Cgrjtkx6yd8xhLBFwKBgQDdpuqR6zTTPBCiOf4bKMM0huVdrmnkDjxf\n7FPsaBjMoi+/Lu33b+9w83TEwaDbZZmz6V1CR891Emf6mUZOHZ3LHB2zpTGKXTf7\n1FmYOqNak4QfQE3EdsiqbKDhX6Z8aONEgy6FAtoQ8JJ17fQpEla/teGrxfcRKaNO\nTjb3np8UaQKBgB8rkcMMnZ5lwOMipQldH98+A1FqYRacfEJLT78ONwTMqBh/hLys\njYmvo+aZunszaupyCn4cq+tvvNOFh9gLFR/Yc9E8XDQ6o2KqMUtKL/zUn/f+FQka\nwSudzx9OGSh5rvvk2ypZDx6poyu/YlOHC1Dv6cIMQh4hb9MpryG0aL3nAoGAXOmr\nSp+d9S4oithkfF4J9erWGv8RxFdzV4Jpa5/3RVB3U10Iw8BYTrC/Mfs4wr9EPvaD\n8VTI0fp1O8ckgXpIuut+R9/ndGi/HwFUzUtHTqCnsbHy53gjhc0jY1YFJAGTwxR6\nW6dmYdN2kZi90LmvQ42qm6bQepFJs3l18Ta82IECgYEA15DzCZcJkoZVq81FpT4v\nU8+GCrBUUyFxrf3pvVyC/cyAR8MEMKHURUpHVA9xSHh6c9L8T8nLJvtNSUxy+OyO\nobbFjyn8c1BSbWCPrJJ7kWWDgPgX/3wBDMxbJFIg90+BB/tku4PYCcdbiT0rUt6m\nCNYEkkcDyZe2n93feDDGw6E=\n-----END PRIVATE KEY-----\n",
#   "client_email": "1011931254470-compute@developer.gserviceaccount.com",
#   "client_id": "100852397771340537271",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/1011931254470-compute%40developer.gserviceaccount.com"
# }

#     logger.info("key value: {}".format(key))
#     key = "$(" + str(key) + ")"
#     logger.info("key value: {}".format(key))
    
#     client.login(username="_json_key", password = key, email= "1011931254470-compute@developer.gserviceaccount.com", registry= "https://gcr.io", reauth= False, dockercfg_path="config.json")
#     client.images.push(tag)

if __name__ == '__main__':
    main()