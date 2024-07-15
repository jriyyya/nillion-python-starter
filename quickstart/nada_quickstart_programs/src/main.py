from nada_dsl import *


def nada_main():
    # Define parties
    alice = Party(name="Alice")
    bob = Party(name="Bob")
    charlie = Party(name="Charlie")

    # Define secret bids from each party
    alice_bid = SecretInteger(Input(name="alice_bid", party=alice))
    bob_bid = SecretInteger(Input(name="bob_bid", party=bob))
    charlie_bid = SecretInteger(Input(name="charlie_bid", party=charlie))

    # Determine the maximum bid
    alice_has_max_bid = (alice_bid > bob_bid) and (alice_bid > charlie_bid)
    bob_has_max_bid = (bob_bid > alice_bid) and (bob_bid > charlie_bid)
    charlie_has_max_bid = (charlie_bid > alice_bid) and (charlie_bid > bob_bid)

    # Combine conditions using logical OR
    max_bid = alice_has_max_bid or bob_has_max_bid or charlie_has_max_bid

    # Output the result
    max_bid_output = Output(max_bid, "max_bid", alice)

    return [max_bid_output]
