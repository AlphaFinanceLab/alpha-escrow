from brownie import chain
from brownie import AlphaEscrow
import brownie


def test_claim_withdraw_receipt_after_7_days_by_cream_gov(escrow, alpha, creamGov):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    escrow.withdraw(withdraw_amount, {"from": creamGov})

    # wait 7 days
    chain.sleep(7 * 86400)

    alphaBefore = alpha.balanceOf(creamGov)
    escrow.claim(id, {"from": creamGov})
    alphaAfter = alpha.balanceOf(creamGov)

    assert (
        alphaAfter - alphaBefore == withdraw_amount
    ), "incorrect alpha balance after claim ALPHA"


def test_claim_withdraw_receipt_before_7_days_by_cream_gov(escrow, alpha, creamGov):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    alphaBefore = alpha.balanceOf(creamGov)
    escrow.withdraw(withdraw_amount, {"from": creamGov})

    # 3 days pass
    chain.sleep(3 * 86400)

    with brownie.reverts("invalid time to claim"):
        escrow.claim(id, {"from": creamGov})
    alphaAfter = alpha.balanceOf(creamGov)
    assert alphaAfter == alphaBefore, "incorrect alpha balance after withdraw ALPHA"


def test_claim_withdraw_receipt_after_7_days_by_alpha_governor(
    escrow, alpha, creamGov, alphaGov
):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    alphaBefore = alpha.balanceOf(alphaGov)
    escrow.withdraw(withdraw_amount, {"from": creamGov})

    # wait 7 days
    chain.sleep(7 * 86400)

    with brownie.reverts("only Cream governor"):
        escrow.claim(id, {"from": alphaGov})
    alphaAfter = alpha.balanceOf(alphaGov)
    assert alphaAfter == alphaBefore, "incorrect alpha balance after withdraw ALPHA"


def test_claim_canceled_withdraw_receipt(escrow, creamGov, alphaGov):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    escrow.withdraw(withdraw_amount, {"from": creamGov})

    # wait 7 days
    chain.sleep(7 * 86400)

    escrow.cancelWithdrawReceipt(id, {"from": alphaGov})
    with brownie.reverts("receipt has been canceled, claimed, or not yet initialized"):
        escrow.claim(id, {"from": creamGov})


def test_claim_claimed_withdraw_receipt(escrow, creamGov):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    escrow.withdraw(withdraw_amount, {"from": creamGov})

    # wait 7 days
    chain.sleep(7 * 86400)

    escrow.claim(id, {"from": creamGov})
    with brownie.reverts("receipt has been canceled, claimed, or not yet initialized"):
        escrow.claim(id, {"from": creamGov})


def test_claim_uninitialized_withdraw_receipt(escrow, creamGov):
    withdraw_amount = 10 ** 18
    id = 1000
    escrow.withdraw(withdraw_amount, {"from": creamGov})

    # wait 7 days
    chain.sleep(7 * 86400)

    with brownie.reverts("receipt has been canceled, claimed, or not yet initialized"):
        escrow.claim(id, {"from": creamGov})


def test_claim_withdraw_receipt_after_7_days_by_other_user(
    escrow, alpha, creamGov, alice
):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    escrow.withdraw(withdraw_amount, {"from": creamGov})

    # wait 7 days
    chain.sleep(7 * 86400)

    with brownie.reverts("only Cream governor"):
        escrow.claim(id, {"from": alice})