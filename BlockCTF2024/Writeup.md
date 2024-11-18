# BlockCTF 2024 writeup
## Topic: Reversing
### 1. Nothin but Stringz
We are given a file nothin_but_stringz.c.o. Running the "file" command on it says: `nothin_but_stringz.c.o: LLVM bitcode, wrapper`.
To make it into readable format, I ran the command `llvm-dis nothin_but_stringz.c.o -o myfile.ll`. Opening `myfile.ll` gives us the flag.

## Topic: Cryptography
### 1. Sizer Cipher
We are given an output 052c01be88c7f52cbdc3c084c7b1313828034370034dd13778342dff, and a blackbox cipher to decrypt.
After trying blind inputs, we find out the cipher maps as follows:
| Character    | Output (in hexadecimal) |
| -------- | ------- |
| a-z  | 00-19    |
| A-Z | 20- 33    |
| 0-9    | 34-3d    |
| { }   | 3e, 3f   |

Then, the cipher continues to roll over, i.e. aa is 40, which comes after the last single character }, which is 3f.

This process works on every 2 characters, such that 2 charcters in the input maps to 3 characters in the output.

Hence, to solve, we just need a function that maps 3 characters of output to 2 characters of input.
Notice that `output_3 = 0x40 * input[0] + input[1]`
That is the main function used in `sizer_cipher.py`.

To make things easier, I padded an extra `0` in front of the output given, so the length of the output string is divisble by 3. We just need to remove the extra `a` at the front.
Running the code yields the flag: `flag{ImF1ll3dWithSte4kandCann0tD4nc3}`.

### 2. Where's my key?
We are given the code in `server.py`. When we send a `client_pub` to the server, the server creates `secret` by multiplying `client_pub` with `server_priv`.

It then creates a AES cipher using `secret` and random `iv`.

The response of the server is the random `iv` and ciphertext `ct`.

Since we have control over `client_pub`, the only way we can control `secret` is by setting `client_pub` to be all zeros. No matter what random value of `sever_priv` is generated, `secret` will always be 0.

In this way, we can just use `iv` to create our own AES cipher with all zero `secret`, and decrypt the ciphertext, yielding the flag: `flag{0000_wh0_knew_pub_keys_c0uld_be_bad_0000}.`

### 3. Glitch in the Crypt: Exploiting Faulty RSA Decryption
We are provided with `server.py`, which shows RSA decryption using CRT. The part which generates `m1` is faulty 10% of the time, returning some random number.

We are also given the oracle, where we can decrypt whatever ciphertext we want, and are provided with either the correct/faulty decryption.

Notice that if we take the absolute difference between the correct and faulty decryption, the difference is divisible by p.

However, using only one difference is quite tough, as it has other factors as well, and takes a long time to find p, `O(sqrt(n))` time.

If we use multiple differences, we can find their gcd in `O(log(max(a, b)))` time. In this case, we just use random 5 hex ciphertexts.

After getting gcd (which is probably p), we return p and q. This allows us to decrypt and get the flag `flag{cr4ck1ng_RS4_w1th_f4ul7s}`.