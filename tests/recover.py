from brownie import AlphaEscrow
import brownie


def test_recover_erc20_from_escrow(escrow, mock_token, alphaGov, bob):
    amount = 100 * 10 ** 18
    mock_token.mint(escrow, amount, {"from": bob})
    gov_before = mock_token.balanceOf(alphaGov)
    escrow.recover(mock_token, {"from": alphaGov})
    gov_after = mock_token.balanceOf(alphaGov)
    assert gov_after - gov_before == amount, "incorrect erc20 recovery amount"


def test_recover_alpha_from_escrow(escrow, alpha, alphaGov, bob):
    amount = 100 * 10 ** 18
    alpha.mint(escrow, amount, {"from": bob})
    gov_before = alpha.balanceOf(alphaGov)
    with brownie.reverts("cannot recover ALPHA"):
        escrow.recover(alpha, {"from": alphaGov})
    gov_after = alpha.balanceOf(alphaGov)
    assert gov_after == gov_before, "alpha gov can't recover ALPHA"
