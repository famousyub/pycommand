import socket
import select
import sys

# All constants must be present in the module, TelnetClient class relies on them
BUFSIZE = 4096

IAC = 255
DONT = 254
DO = 253
WONT = 252
DONT = 254
WILL = 251

COMMANDS = {
    # RFC 854 official codes
    'IAC': IAC,
    'DONT': DONT,
    'DO': DO,
    'WONT': WONT,
    'WILL': WILL,
    'GA': 249,
    'SE': 240,
    'NOP': 241,
    'DM': 242,
    'BRK': 243,
    'IP': 244,
    'AO': 245,
    'AYT': 246,
    'EC': 247,
    'EL': 248,
    'SB': 250,
    # Not in RFC, but still popular in the wild:
    'Transmit Binary': 0,
    'Echo': 1,
    'Suppress Go Ahead': 3,
    'Status': 5,
    'Terminal Type': 24,
    'Window size': 31,
    'Line Mode': 34
}

# Inverted mapping for translations
CODES = {v: k for k, v in COMMANDS.items()}

WELCOME_MESSAGE = """
*** Welcome to Telnet51, Group 51 Telnet client ***
This client supports direct IAC send mode. Any message started with '!'
and followed by decimal opcodes and/or their known character aliases
will be sent directly to server as an IAC-prepended sequence.
E.g.:
> !AYT will send byte sequence FFF6 (255, 246) to server.
> !253 249 will send GA to server, can be also expressed with !DO GA
All IAC-prepended sequences coming from the server will be translated into
respective opcodes and their names will be printed on screen for convenience.
"""

def translate_and_log(sequence):
    """Translates binary sequences to readable codes"""
    translations = [CODES.get(i, str(i)) for i in sequence]
    sys.stdout.write("(Server says) ")
    print(' '.join(translations))

class TelnetClient:
    """Telnet client from scratch"""
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)

    def _connect(self):
        try:
            self.sock.connect((self.host, self.port))
        except socket.error:
            print('Unable to connect')
            sys.exit()

        out = "*** Connected to {} on port {} ***".format(self.host, self.port)
        print(out)
        print(WELCOME_MESSAGE)

    def _send_payload(self, *codes):
        payload = bytearray()
        for code in codes:
            payload.append(code)
        self.sock.send(payload)

    def _negotiate(self, sequence):
        # Negotiate according to minimal best-practice rules:
        # WILL -> DONT, DO -> WONT, WONT -> DONT, DONT -> WONT
        # Don't engage in subnegotiations automatically
        # And ignore non-negotiating sequences
        if len(sequence) < 3:
            return
        opt = sequence[2]
        verb = sequence[1]
        if verb == WILL:
            self._send_payload(IAC, DONT, opt)
        elif verb == DO:
            self._send_payload(IAC, WONT, opt)
        elif verb == WONT:
            self._send_payload(IAC, DONT, opt)
        elif verb == DONT:
            self._send_payload(IAC, WONT, opt)

    # Interactive manual command sending
    # You can send either a decimal byte representation or a code from
    # known list of codes. _Starting IAC is auto-appended_
    def _send_command(self, msg):
        codes = msg[1:].split() # drop the '!'
        pre_processed = [COMMANDS.get(w, w) for w in codes] # support direct codes
        processed = []
        for elt in pre_processed:
            try:
                dec = int(elt)
                if dec < 256:
                    processed.append(int(elt))
            except ValueError:
                continue
        self._send_payload(IAC, *processed)

    def _parse_incoming(self):
        try:
            data = self.sock.recv(BUFSIZE)
            if not data:
                print('Connection closed by remote host')
                sys.exit()
        except ConnectionResetError: # some servers hard-reset the connection
            print('Server was mean to us :(')
            sys.exit()

        starting_iac = False
        # Look at all received bytes and search for IAC
        for idx, byte in enumerate(data):
            if byte == IAC:
                # negotiation sequence is IAC + two more bytes
                sequence = [b for b in data[idx:idx+3]]
                translate_and_log(sequence) # Log to screen
                self._negotiate(sequence) # Answer if 3-bytes sequence
                if idx == 0:
                    starting_iac = True
        # Printing bytes to screen one-by-one affects smoothness,
        # so we print the whole buffer except for starting IAC sequence
        # if it was present.
        if starting_iac:
            data = data[3:]
        sys.stdout.write(data.decode('utf-8', errors='ignore'))
        sys.stdout.flush() # clear the buffer.

    def run(self):
        """Starts the client"""
        self._connect()
        while True:
            # Non-blocking IO with UNIX Select API
            socket_list = [sys.stdin, self.sock]
            readable, _, _ = select.select(socket_list, [], [])
            # Set up and watch wich process becomes available
            for read in readable:
                if read == self.sock:  # Socket is available for reading
                    self._parse_incoming()
                else:  # Stdin is available for reading
                    msg = sys.stdin.readline()
                    if msg.startswith('!'): # Enable interactive mode
                        self._send_command(msg)
                    else:
                        msg += '\r' # force carriage return for servers w/o line mode
                        self.sock.send(msg.encode())

if __name__ == "__main__":
    # Guard
    if len(sys.argv) < 2:
        print('Usage: python telnet.py hostname [port]')
        sys.exit()

    # Set up and go
    HOST = sys.argv[1]
    try:
        PORT = int(sys.argv[2])
    except IndexError:
        PORT = 23 # Default to standard Telnet port

    TC = TelnetClient(HOST, PORT)
    try:
        TC.run()
    except KeyboardInterrupt:
        print("Bye-bye!")
        sys.exit()