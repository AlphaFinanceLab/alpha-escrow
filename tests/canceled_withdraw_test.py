from brownie import accounts, chain
from brownie import AlphaEscrow
from brownie.exceptions import VirtualMachineError
import brownie


def test_cancel_withdraw_receipt_by_alpha_gov(
    escrow, alphaGov, creamGov, status_canceled
):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    expected_withdraw_time = chain.time()
    escrow.withdraw(withdraw_amount, {"from": creamGov})
    escrow.cancelWithdrawReceipt(id, {"from": alphaGov})

    amount, withdraw_time, status = escrow.receipts(id)
    assert amount == withdraw_amount, "invelid receipt's withdraw amount"
    assert withdraw_time == expected_withdraw_time, "invelid receipt's withdraw time"
    assert status == status_canceled, "invalid receipt's status"


def test_cancel_withdraw_receipt_by_cream_gov(escrow, creamGov, status_canceled):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    expected_withdraw_time = chain.time()
    escrow.withdraw(withdraw_amount, {"from": creamGov})
    escrow.cancelWithdrawReceipt(id, {"from": creamGov})

    amount, withdraw_time, status = escrow.receipts(id)
    assert amount == withdraw_amount, "invelid receipt's withdraw amount"
    assert withdraw_time == expected_withdraw_time, "invelid receipt's withdraw time"
    assert status == status_canceled, "invalid receipt's status"


def test_cancel_withdraw_receipt_by_other(escrow, creamGov, alice):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    escrow.withdraw(withdraw_amount, {"from": creamGov})
    with brownie.reverts("only Cream or Alpha governor"):
        escrow.cancelWithdrawReceipt(id, {"from": alice})


def test_cancel_claimed_withdraw_receipt(escrow, creamGov, status_canceled):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    escrow.withdraw(withdraw_amount, {"from": creamGov})

    # wait 7 days
    chain.sleep(7 * 86400)

    escrow.claim(id, {"from": creamGov})

    with brownie.reverts("only pending receipt can be canceled"):
        escrow.cancelWithdrawReceipt(id, {"from": creamGov})


def test_cancel_canceled_withdraw_receipt(escrow, creamGov, status_canceled):
    withdraw_amount = 10 ** 18
    id = escrow.nextReceiptId()
    escrow.withdraw(withdraw_amount, {"from": creamGov})
    escrow.cancelWithdrawReceipt(id, {"from": creamGov})

    with brownie.reverts("only pending receipt can be canceled"):
        escrow.cancelWithdrawReceipt(id, {"from": creamGov})


def test_cancel_uninitialized_withdraw_receipt(escrow, creamGov, status_canceled):
    id = 1000
    withdraw_amount = 10 ** 18
    escrow.withdraw(withdraw_amount, {"from": creamGov})

    with brownie.reverts("only pending receipt can be canceled"):
        escrow.cancelWithdrawReceipt(id, {"from": creamGov})