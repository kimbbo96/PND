import sys
from socket import *
import binascii


def sendeth (src, dst , type, payload, interface = "eth0"):
        """send raw ethernet frame on interface"""
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
    print(sys.argv[1])
    source = "ba:9d:d3:ec:ea:07"
    dest = "e6:80:50:76:15:46"
    #source = source.replace(':', '').decode('hex')
    #dest = dest.replace(':', '').decode('hex')
    source = binascii.unhexlify(source.replace(':',''))
    dest = binascii.unhexlify(dest.replace(':','')) 
    print(dest, "  ",source)

    ethernet_packet = source.split('\\');
    print(ethernet_packet)



    print("Sent %d-byte Ethernet packet on eth0" %
    sendeth(source,dest,
                                        "\x7A\x05",
                                                  "hello spognardi"))

    
    
