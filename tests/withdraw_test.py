from brownie import chain
from brownie import AlphaEscrow
import brownie


def test_withdraw(escrow, creamGov, status_pending):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    tx = escrow.withdraw(withdraw_amount, {"from": creamGov})
    amount, withdraw_time, status = escrow.receipts(id)

    assert amount == withdraw_amount, "invalid receipt's amount"
    assert withdraw_time == tx.timestamp, "invalid receipt's withdraw time"
    assert status == status_pending, "invalid receipt's status"


def test_withdraw_by_other_user(escrow, alice, status_pending):
    withdraw_amount = 10 ** 18
    with brownie.reverts("only Cream governor"):
        escrow.withdraw(withdraw_amount, {"from": alice})


def test_withdraw_amount_0(escrow, creamGov, status_pending):
    withdraw_amount = 0
    with brownie.reverts("cannot withdraw 0 alpha"):
        escrow.withdraw(withdraw_amount, {"from": creamGov})


def test_withdraw_insufficient_alpha(alpha, escrow, creamGov):
    insufficient_withdraw_amount = alpha.balanceOf(escrow) + 10 * 10 ** 18
    with brownie.reverts("insufficient ALPHA to withdraw"):
        escrow.withdraw(insufficient_withdraw_amount, {"from": creamGov})
