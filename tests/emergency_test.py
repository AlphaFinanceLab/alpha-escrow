from brownie import chain
from brownie import AlphaEscrow
import brownie


def test_request_emergency_withdraw_by_alpha_gov(escrow, alphaGov):
    tx = escrow.requestEmergencyWithdraw({"from": alphaGov})
    assert tx.timestamp == escrow.emergencyRequestTime(), "incorrect request time"


def test_request_emergency_withdraw_by_cream_gov(escrow, creamGov):
    with brownie.reverts("only Alpha governor"):
        escrow.requestEmergencyWithdraw({"from": creamGov})


def test_request_emergency_withdraw_by_other_user(escrow, alice):
    with brownie.reverts("only Alpha governor"):
        escrow.requestEmergencyWithdraw({"from": alice})


def test_cancel_request_emergency_withdraw_by_alpha_gov(escrow, alphaGov):
    escrow.requestEmergencyWithdraw({"from": alphaGov})
    escrow.cancelEmergencyWithdraw({"from": alphaGov})
    assert escrow.emergencyRequestTime() == 0, "incorrect request time after canceled"


def test_cancel_request_emergency_withdraw_by_cream_gov(escrow, creamGov, alphaGov):
    escrow.requestEmergencyWithdraw({"from": alphaGov})
    escrow.cancelEmergencyWithdraw({"from": creamGov})
    assert escrow.emergencyRequestTime() == 0, "incorrect request time after canceled"


def test_cancel_request_emergency_withdraw_by_other_user(escrow, alphaGov, alice):
    escrow.requestEmergencyWithdraw({"from": alphaGov})
    with brownie.reverts("only Cream or Alpha governor"):
        escrow.cancelEmergencyWithdraw({"from": alice})


def test_immediately_claim_emergency_withdraw_by_alpha_gov(escrow, alpha, alphaGov):
    escrow.requestEmergencyWithdraw({"from": alphaGov})
    with brownie.reverts("invalid time to claim requested ALPHA"):
        escrow.claimEmergencyWithdraw({"from": alphaGov})


def test_immediately_claim_emergency_withdraw_after_1_month_by_alpha_gov(
    escrow, alpha, alphaGov
):
    escrow.requestEmergencyWithdraw({"from": alphaGov})
    escrow_balance = alpha.balanceOf(escrow)

    # wait 1 month
    chain.sleep(30 * 86400)
    gov_before = alpha.balanceOf(alphaGov)
    escrow.claimEmergencyWithdraw({"from": alphaGov})
    gov_after = alpha.balanceOf(alphaGov)
    assert gov_after - gov_before == escrow_balance, "claim emergency withdraw fail"
    assert escrow.emergencyRequestTime() == 0, "invalid emergencyRequest after claim"
