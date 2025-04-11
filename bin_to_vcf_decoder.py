# bin_to_vcf_decoder.py

import argparse


def decode_variant(blob):
    chrom_code = blob[0]
    chrom = str(chrom_code) if chrom_code <= 22 else {23: "X", 24: "Y", 25: "MT"}.get(chrom_code, "?")
    pos = int.from_bytes(blob[1:5], 'big')
    ref = blob[5:9].decode('utf-8').rstrip()
    alt = blob[9:13].decode('utf-8').rstrip()
    return chrom, pos, ref, alt


def decode_bin_to_vcf(bin_path, out_vcf_path):
    with open(bin_path, 'rb') as f:
        binary = f.read()

    variants = [decode_variant(binary[i:i+13]) for i in range(0, len(binary), 13)]

    with open(out_vcf_path, 'w') as f:
        f.write("##fileformat=VCFv4.2\n")
        f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")
        for chrom, pos, ref, alt in variants:
            f.write(f"{chrom}\t{pos}\t.\t{ref}\t{alt}\t.\t.\t.\n")
    print(f"✅ VCF written to {out_vcf_path} with {len(variants)} variants")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bin', required=True, help='Input .bin file from decryption')
    parser.add_argument('--out', required=True, help='Output .vcf file')
    args = parser.parse_args()

    decode_bin_to_vcf(args.bin, args.out)

