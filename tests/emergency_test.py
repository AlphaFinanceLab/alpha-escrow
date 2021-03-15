from brownie import chain
from brownie import AlphaEscrow
import brownie


def test_request_last_resort_withdraw_by_alpha_gov(escrow, alphaGov):
    tx = escrow.requestLastResort({"from": alphaGov})
    assert tx.timestamp == escrow.lastResortRequestTime(), "incorrect request time"


def test_request_last_resort_withdraw_by_cream_gov(escrow, creamGov):
    with brownie.reverts("only Alpha governor"):
        escrow.requestLastResort({"from": creamGov})


def test_request_last_resort_withdraw_by_other_user(escrow, alice):
    with brownie.reverts("only Alpha governor"):
        escrow.requestLastResort({"from": alice})


def test_cancel_request_last_resort_withdraw_by_alpha_gov(escrow, alphaGov):
    escrow.requestLastResort({"from": alphaGov})
    escrow.cancelLastResort({"from": alphaGov})
    assert escrow.lastResortRequestTime() == 0, "incorrect request time after canceled"


def test_cancel_request_last_resort_withdraw_by_cream_gov(escrow, creamGov, alphaGov):
    escrow.requestLastResort({"from": alphaGov})
    escrow.cancelLastResort({"from": creamGov})
    assert escrow.lastResortRequestTime() == 0, "incorrect request time after canceled"


def test_cancel_request_last_resort_withdraw_by_other_user(escrow, alphaGov, alice):
    escrow.requestLastResort({"from": alphaGov})
    with brownie.reverts("only Cream or Alpha governor"):
        escrow.cancelLastResort({"from": alice})


def test_immediately_claim_last_resort_withdraw_by_alpha_gov(escrow, alpha, alphaGov):
    escrow.requestLastResort({"from": alphaGov})
    with brownie.reverts("invalid time to claim requested ALPHA"):
        escrow.claimLastResort({"from": alphaGov})


def test_immediately_claim_last_resort_withdraw_after_1_month_by_alpha_gov(
    escrow, alpha, alphaGov
):
    escrow.requestLastResort({"from": alphaGov})
    escrow_balance = alpha.balanceOf(escrow)

    # wait 1 month
    chain.sleep(30 * 86400)
    gov_before = alpha.balanceOf(alphaGov)
    escrow.claimLastResort({"from": alphaGov})
    gov_after = alpha.balanceOf(alphaGov)
    assert gov_after - gov_before == escrow_balance, "invalid resort withdraw amount"
    assert (
        escrow.lastResortRequestTime() == 0
    ), "invalid last resort request time after claim"
