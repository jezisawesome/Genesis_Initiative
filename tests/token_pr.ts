import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { TokenPr } from "../target/types/token_pr";
import assert from "assert";

describe("TokenPr", () => {
  anchor.setProvider(anchor.AnchorProvider.env());
  const program = anchor.workspace.TokenPr as Program<TokenPr>;

  it("Initializes an account!", async () => {
    // Generate a new keypair for `new_account`
    const newAccount = anchor.web3.Keypair.generate();

    // Get the provider's wallet (payer)
    const provider = anchor.AnchorProvider.env();
    const signer = provider.publicKey;

    // Airdrop SOL to the provider to ensure sufficient balance
    const airdropSig = await provider.connection.requestAirdrop(
      signer,
      anchor.web3.LAMPORTS_PER_SOL
    );
    await provider.connection.confirmTransaction(airdropSig);

    // Call the `initialize` instruction
    const dataValue = 42; // Example value for `data`
    await program.methods
    .initialize(new anchor.BN(dataValue)) // Pass `data` as a BN
    .accounts({
      newAccount: newAccount.publicKey,
      signer: signer,
      systemProgram: anchor.web3.SystemProgram.programId,
    })
    .signers([newAccount]) // Include the `newAccount` keypair
    .rpc();

    // Fetch the account and verify the data
    const account = await program.account.newAccount.fetch(newAccount.publicKey);
    assert.strictEqual(account.data.toNumber(), dataValue);
    console.log("Account initialized with data:", account.data.toNumber());
  });
});
