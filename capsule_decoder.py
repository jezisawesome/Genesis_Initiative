import argparse
import base64
import json
import binascii
from nacl.public import SealedBox, PrivateKey
from nacl.bindings import crypto_sign_ed25519_sk_to_curve25519
from Crypto.Cipher import AES
import zstandard as zstd


def load_solana_keypair(keypair_path):
    with open(keypair_path, 'r') as f:
        keypair_list = json.load(f)
    keypair_bytes = bytes(keypair_list)
    if len(keypair_bytes) != 64:
        raise ValueError("Solana keypair must be 64 bytes")
    return keypair_bytes


def extract_hex_block(capsule_path, gene):
    with open(capsule_path, 'r') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if lines[i].strip() == f"##NP0::GENE::{gene}##":
            hex_line = lines[i + 1].strip()
            if hex_line.startswith("HEX:"):
                return bytes.fromhex(hex_line.split("HEX:")[1].strip())
    raise ValueError(f"Gene {gene} not found in capsule")


def decrypt_blob(encrypted_blob, metadata_path, keypair_path):
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    sealed_key = base64.b64decode(metadata['sealed_key'])
    nonce = base64.b64decode(metadata['nonce'])
    tag = base64.b64decode(metadata['tag'])

    ed25519_sk_bytes = load_solana_keypair(keypair_path)
    curve25519_sk = crypto_sign_ed25519_sk_to_curve25519(ed25519_sk_bytes)
    box = SealedBox(PrivateKey(curve25519_sk))
    aes_key = box.decrypt(sealed_key)

    try:
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(encrypted_blob, tag)
        decompressed = zstd.ZstdDecompressor().decompress(decrypted)
        return decompressed
    except Exception as e:
        raise ValueError(f"AES-GCM decryption failed: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--capsule", required=True)
    parser.add_argument("--gene", required=True)
    parser.add_argument("--meta", required=True)
    parser.add_argument("--keypair", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    hex_blob = extract_hex_block(args.capsule, args.gene)
    decrypted = decrypt_blob(hex_blob, args.meta, args.keypair)
    with open(args.out, 'wb') as f:
        f.write(decrypted)
    print(f"✅ Gene {args.gene} written to {args.out}")


if __name__ == "__main__":
    main()

