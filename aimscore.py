# Python program to test
# internet speed

import speedtest
from cymruwhois import Client
import requests
from requests import get
import json
import pingparsing
import uuid

# Get IP address for ASN lookup
ips = get('https://api.ipify.org').text

# perform a whois to get ASN
c=Client()
r=c.lookup(ips)
print('asn number: ',r.asn)
print('asn owner : ',r.owner)

st = speedtest.Speedtest()
st.get_best_server()

# get download stats - threads=8 is not scientific but anecdata shows good results
print('Download Throughput: ',(st.download(threads=8)/1e6))

# get upload stats
print('Upload Throughput: ',(st.upload(threads=8)/1e6))

# get ping stats
print('RTT: ',st.results.ping)

# perform a ping test to get loss rate and jitter
ping_parser = pingparsing.PingParsing()
transmitter = pingparsing.PingTransmitter()
transmitter.destination = "google.com"
transmitter.count = 10
result = transmitter.ping()

# shove it into a json and then convert it back to a dict because python is stupid
formatted = json.dumps(ping_parser.parse(result).as_dict())
dict = json.loads(formatted)

print('Packet Loss: ',dict['packet_loss_rate'])
print('Jitter: ', dict['rtt_mdev'])

# RPKI support
try:
  rpki = get('https://invalid.rpki.cloudflare.com', timeout=(5, None))
  if rpki.status_code == 200:
      print('RPKI Support: false')
  else: print('RPKI Support: true')
except requests.exceptions.Timeout as e:
  print('RPKI Support: true')


test_uuid = uuid.uuid1()
try:
    uuid_request = get('https://'+str(test_uuid)+'.com')
    print('NXDOMAIN Pollution: true')
except requests.exceptions.RequestException as err:
    print('NXDOMAIN Pollution: false')
