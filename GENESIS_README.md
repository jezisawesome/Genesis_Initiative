# 🧬 NP0:Genesis — Encrypted Genomic Capsule Verification

Welcome to the NP0:Genesis testbed.

This repository demonstrates the encryption and decryption process for permissioned genomic data using real-world canine genome variants. It is part of the NP0 protocol — a decentralized framework for privacy-preserving genomic intelligence.

## 📖 About the Data

The VCF (Variant Call Format) file used in this demo comes from the **Dog10K project**, a large-scale sequencing initiative capturing genome variants from:

- **1,300 domestic dogs** from over 200 breeds
- **77 wild canids**, including wolves and related species

The file represents millions of high-confidence genomic variants and their distribution across the canine lineage.

By extracting and encrypting data at the **gene level**, we demonstrate fine-grained control over access and permissions — a foundational building block for future decentralized bio-intelligence platforms.

## 🚀 What This Repo Proves

- ✅ Gene-level data can be **stored on-chain** in encrypted form.
- ✅ Only holders of the correct keypair + metadata can **decrypt** the binary gene blob.
- ✅ That gene blob can be **converted back into VCF** format for meaningful use.

---

## 📁 Files in this Repository

| File | Description |
|------|-------------|
| `capsule_decoder.py` | Decrypts a specific gene from a capsule using a keypair and its metadata |
| `bin_to_vcf_decoder.py` | Converts decrypted binary data back into a readable VCF file |
| `np0-keypair.json` | Keypair used for sealing/unsealing gene blobs (for test purposes only) |
| `OXTR_encryption_metadata.json` | Metadata to decrypt the gene **OXTR** |
| `TULP1_encryption_metadata.json` | Metadata to decrypt the gene **TULP1** |

---

## 🧪 How to Run

> Make sure you have Python 3.8+ and [pip](https://pip.pypa.io/en/stable/) installed.

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/np0-genesis.git
cd np0-genesis
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Prepare Encrypted Capsule Text

📥 _Insert instructions here for downloading or copying the capsule text from on-chain storage._

Once obtained, save it locally as:

```bash
dog_capsule.txt
```

Or any name of your choice — just reference it correctly in the next step.

---

## 🔓 Decrypt a Gene Capsule

Example: Decrypt the gene **TULP1**

```bash
python3 capsule_decoder.py \
  --capsule dog_capsule.txt \
  --gene TULP1 \
  --meta TULP1_encryption_metadata.json \
  --keypair np0-keypair.json \
  --out TULP1_decrypted.bin
```

---

## 🔁 Reconstruct the VCF

```bash
python3 bin_to_vcf_decoder.py \
  --bin TULP1_decrypted.bin \
  --out TULP1_resurrected.vcf
```

---

## ✅ Output

You should now have a valid `.vcf` file representing the original variant calls for the **TULP1** gene.

Example output:
```
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
12	4971665	.	A	G	.	.	.
...
```

---

## 🛡️ Security Notes

This repo is a demonstration. In real deployments:
- The keypair should be securely stored and never exposed.
- Metadata will only be released with consent of the data owner - typically the holder of the keypair which encrypted and stored the data.

---

## 📫 Contact

Questions or collab requests? DM us via [Twitter](https://twitter.com) or email.

---

🧬 Built with love by the NP0 Genesis crew
