from brownie import AlphaEscrow
import brownie


def test_unlock_alpha_by_cream_gov(escrow, alpha, creamGov, alphaGov):
    unlock_amount = 10 * 10 ** 18
    balance_before = alpha.balanceOf(alphaGov)
    escrow.unlock(unlock_amount, {"from": creamGov})
    balance_after = alpha.balanceOf(alphaGov)

    assert (
        balance_after - balance_before == unlock_amount
    ), "incorrect balance after unlock ALPHA"


def test_unlock_alpha_by_other_user(escrow, alpha, creamGov, alice):
    unlock_amount = 10 * 10 ** 18
    with brownie.reverts("only Cream governor"):
        escrow.unlock(unlock_amount, {"from": alice})