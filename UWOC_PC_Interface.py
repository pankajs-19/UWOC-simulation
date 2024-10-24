# Imports
import serial   # To enable communication
import time     # To perform statistical analysis

# Handler class for PC-Hardware interface
class lifi:
    rx_str = ""

    def __init__(self, port):
        self.port = port
        return

    @staticmethod
    def binaryToDecimal(n):
        return int(n,2)

    @staticmethod
    def toString(s):
        string = ""
        for byte in s:
            byte_num = lifi.binaryToDecimal(byte)
            string += chr(byte_num)
        return string

    @staticmethod
    def splitString(s):
        str_lst = [s[i:i + 7] for i in range(0, len(s), 7)]
        return str_lst

    # Performs XOR and adds the resultant to get count of incorrect bits
    @staticmethod
    def bercalculation(b1, b2):
        berrs = 0
        for i in range(len(b1)):
            a = int(b1[i])
            b = int(b2[i])
            berrs += a^b
        return berrs

    @staticmethod
    def toBinary(a):
        bin_str = ""
        for i in a:
            bin_chr = str(bin(ord(i)).replace("0b",""))
            if (len(bin_chr)==6):
                bin_chr = "0"+bin_chr
            bin_str += bin_chr
        return bin_str

    # Primary data transfer function
    def transmit_and_receive_data(self, tx_msg):
        self.port.write("T\n".encode())
        start = time.time()
        for tx in tx_msg:
            tx = int(tx)
            if tx:
                self.port.write("H\n".encode())
            else:
                self.port.write("L\n".encode())
            rx = int(port.readline())
            self.rx_str += str(rx)
        self.port.write("L\n".encode())
        rx = int(port.readline())
        self.rx_str += str(rx)
        elapsed = time.time() - start
        self.port.write("S\n".encode())
        return self.rx_str[1:], elapsed

# Selecting port and message filename
pid = "COM10"
filename = 'message.txt'

# Opening a text file on PC and read the message
with open(filename) as file:
    message = file.read()

port = serial.Serial(pid)

# Convert message its binary form
message_bin = lifi.toBinary(message)
lifi_console = lifi(port)
lifi_rx, elapsed = lifi_console.transmit_and_receive_data(message_bin)

# Statistical analysis
print()
print("-------------- Message signal (Transmitted) ---------------")
print(message)
print("--------------- Binary transmitted signal -----------------")
print(message_bin)
print("------------------- Raw received signal -------------------")
print(lifi_rx)
lifi_rx_str = lifi.splitString(lifi_rx)
print("----------------- Raw split binary signal -----------------")
print(lifi_rx_str)
print("---------------- Message signal (Received) ----------------")
lifi_rx_str = lifi.toString(lifi_rx_str)
print(lifi_rx_str)
error_bits = lifi.bercalculation(lifi_rx, message_bin)
n_bits = len(message)*7
n_bytes = len(message)
print("---------------------- Statistics -------------------------")
print("Time elapsed: %.2f seconds" % (elapsed,))
print("Bits transferred: ", n_bits)
print("Bit error ratio: %.2f percent" % ((error_bits*100)/n_bits),)
print("Bit error rate: %.5f" % (error_bits/elapsed),)
print("Bit rate: %.2f" % (n_bits/elapsed),)
print("BAUD rate: %.2f" % (n_bytes/elapsed),)
print("-----------------------------------------------------------")