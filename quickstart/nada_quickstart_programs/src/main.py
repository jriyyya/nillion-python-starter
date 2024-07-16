from nada_dsl import *

def initialize_parties(nr_borrowers, nr_lenders):
    borrowers = [Party(name=f"Borrower{i}") for i in range(nr_borrowers)]
    lenders = [Party(name=f"Lender{i}") for i in range(nr_lenders)]
    return borrowers, lenders

def inputs_initialization(borrowers, lenders):
    loan_requests = []
    for b in borrowers:
        loan_amount = SecretUnsignedInteger(Input(name=f"loan_amount_{b.name}", party=b))
        max_interest_rate = SecretUnsignedInteger(Input(name=f"max_interest_rate_{b.name}", party=b))
        loan_requests.append((loan_amount, max_interest_rate))
    
    loan_offers = []
    for l in lenders:
        offer_amount = SecretUnsignedInteger(Input(name=f"offer_amount_{l.name}", party=l))
        interest_rate = SecretUnsignedInteger(Input(name=f"interest_rate_{l.name}", party=l))
        loan_offers.append((offer_amount, interest_rate))
    
    return loan_requests, loan_offers

def match_loans(loan_requests, loan_offers):
    matches = []
    for loan_amount, max_interest_rate in loan_requests:
        best_offer = None
        for offer_amount, interest_rate in loan_offers:
            if interest_rate <= max_interest_rate and (best_offer is None or interest_rate < best_offer[1]):
                best_offer = (offer_amount, interest_rate)
        if best_offer:
            matches.append((loan_amount, best_offer[0], best_offer[1]))
    return matches

def calculate_final_payments(matches):
    final_payments = []
    for loan_amount, offer_amount, interest_rate in matches:
        interest_factor = interest_rate + UnsignedInteger(100)  # interest_rate is out of 100
        final_amount = (loan_amount * interest_factor) / UnsignedInteger(100)
        final_payments.append(final_amount)
    return final_payments

def nada_main():
    nr_borrowers = 3
    nr_lenders = 3
    outparty = Party(name="OutParty")

    borrowers = [Party(name=f"Borrower{i}") for i in range(nr_borrowers)]
    lenders = [Party(name=f"Lender{i}") for i in range(nr_lenders)]
    loan_requests, loan_offers = inputs_initialization(borrowers, lenders)

    matches = match_loans(loan_requests, loan_offers)
    final_payments = calculate_final_payments(matches)

    # Create Output objects for each final payment
    output_payments = [Output(final_amount, name=f"final_payment_{i}", party=outparty) for i, final_amount in enumerate(final_payments)]

    return output_payments
