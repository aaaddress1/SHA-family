import binascii

message = b'The quick brown fox jumps over the lazy dog'
message_length = len(message) * 8
right_rotate = lambda n, b: ((n >> b) | (n << (64 - b))) & 0xffffffffffffffff

# initialization variables
h0 = 0x6a09e667f3bcc908
h1 = 0xbb67ae8584caa73b
h2 = 0x3c6ef372fe94f82b
h3 = 0xa54ff53a5f1d36f1
h4 = 0x510e527fade682d1
h5 = 0x9b05688c2b3e6c1f
h6 = 0x1f83d9abfb41bd6b
h7 = 0x5be0cd19137e2179

# initialize table of round constants
k = [
	0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc, 0x3956c25bf348b538, 
	0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242, 0x12835b0145706fbe, 
	0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2, 0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 
	0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 
	0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5, 0x983e5152ee66dfab, 
	0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725, 
	0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 
	0x53380d139d95b3df, 0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b, 
	0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218, 
	0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8, 0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 
	0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 
	0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec, 
	0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b, 0xca273eceea26619c, 
	0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba, 0x0a637dc5a2c898a6, 
	0x113f9804bef90dae, 0x1b710b35131c471b, 0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 
	0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817
]

# pre-processing
message += b'\x80'
message += b'\x00' * ((112 - len(message) % 128) % 128)
message += binascii.unhexlify(hex(message_length)[2:].zfill(32))

# break the message in 1024bits chunks
chunks = [message[i:i+128] for i in range(0, len(message), 128)]

for chunk in chunks:
	# break chuck into sixteen 64bits big-endian words
	w = [int(binascii.hexlify(chunk[i:i+8]), 16) for i in range(0, len(chunk), 8)]
	# extend 16 words to 80 words
	for i in range(16, 80):
		s0 = right_rotate(w[i-15], 1) ^ right_rotate(w[i-15], 8) ^ (w[i-15] >> 7) #right_rotate(w[i-15], 3)
		s1 = right_rotate(w[i-2], 19) ^ right_rotate(w[i-2], 61) ^ (w[i-2] >> 6) #right_rotate(w[i-2], 10)
		w.append((w[i-16] + s0 + w[i-7] + s1) & 0xffffffffffffffff)

	# initialize hash value for this chunk
	a = h0
	b = h1
	c = h2
	d = h3
	e = h4
	f = h5
	g = h6
	h = h7

	# main loop
	for i in range(80):
		s0 = right_rotate(a, 28) ^ right_rotate(a, 34) ^ right_rotate(a, 39)
		s1 = right_rotate(e, 14) ^ right_rotate(e, 18) ^ right_rotate(e, 41)
		choice = (e & f) ^ (~e & g)
		majority = (a & b) ^ (a & c) ^ (b & c)
		temp1 = (h + s1 + choice + k[i] + w[i]) & 0xffffffffffffffff
		temp2 = (s0 + majority) & 0xffffffffffffffff
		
		a, b, c, d, e, f, g, h = (temp1 + temp2) & 0xffffffffffffffff, a, b, c, (d + temp1) & 0xffffffffffffffff, e, f, g

	# add this chunk's hash to result so far
	h0 = (h0 + a) & 0xffffffffffffffff
	h1 = (h1 + b) & 0xffffffffffffffff
	h2 = (h2 + c) & 0xffffffffffffffff
	h3 = (h3 + d) & 0xffffffffffffffff
	h4 = (h4 + e) & 0xffffffffffffffff
	h5 = (h5 + f) & 0xffffffffffffffff
	h6 = (h6 + g) & 0xffffffffffffffff
	h7 = (h7 + h) & 0xffffffffffffffff

# produce the final hash value
digest = hex(h0)[2:] + hex(h1)[2:] + hex(h2)[2:] + hex(h3)[2:] + hex(h4)[2:] + hex(h5)[2:] + hex(h6)[2:] + hex(h7)[2:]
print(digest)