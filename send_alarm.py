import sys
from socket import *
import binascii
import subprocess
from shlex import split


host_MAC = binascii.unhexlify("ba:9d:d3:ec:ea:07".replace(':',''))




def run_arpwatch():
    """run arpwatch"""
    command = "arpwatch -i eth0 -f /var/lib/arp.dat  -d"
    process = subprocess.Popen(split(command),stdout=subprocess.PIPE)
    payload = ""
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break;
        if output:
            payload += output
            if "delta" in output: # the report is complitely captured
                #print payload
                
                dst1 = payload.split("ethernet address:",1)[1][:20].strip()
                dst2 = payload.split("old ethernet address:",1)[1][:20].strip()
                dst1 = binascii.unhexlify(dst1.replace(':',''))
                dst2 = binascii.unhexlify(dst2.replace(':',''))
                sendeth (host_MAC, dst1, payload)
                sendeth (host_MAC, dst2, payload)
                #print(dst1)
                #print( dst2)
                #print(payload)
                

                payload = ""
    rc = process.poll()
    return rc




def sendeth (src, dst , payload, interface = "eth0"):
    """send raw ethernet frame on interface"""
    
    print(src)
    print(dst)
    
    type = binascii.unhexlify("01FF")
    #48 bit addresses
    assert(len(src) == len(dst) == 6)

    #16-bit Ethernet type
    assert(len(type) == 2)

    s = socket(AF_PACKET, SOCK_RAW)
    s.bind((interface,0))
    return s.send(dst + src + type + payload)

def pack(byte_sequence):
    """Convert list of bytes to byte string"""
    return b"".join(map(chr, byte_sequence))


if __name__=="__main__":
    #print(sys.argv[1])
    """
    source = "ba:9d:d3:ec:ea:07"
    dest = "e6:80:50:76:15:46"
    
    source = binascii.unhexlify(source.replace(':',''))
    dest = binascii.unhexlify(dest.replace(':','')) 
    print(dest, "  ",source)

    ethernet_packet = source.split('\\');
    print(ethernet_packet)



    print("Sent %d-byte Ethernet packet on eth0" %
    sendeth(source,dest,
                                        "\x7A\x05",
                                                  "hello spognardi"))

    """
    
    run_arpwatch()

