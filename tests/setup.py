import pytest
from brownie import interface, accounts


@pytest.fixture(scope="function")
def status_pending():
    return 1


@pytest.fixture(scope="function")
def status_canceled():
    return 2


@pytest.fixture(scope="function")
def status_claimed():
    return 3


@pytest.fixture(scope="function")
def deployer():
    return accounts[0]


@pytest.fixture(scope="function")
def alphaGov():
    return accounts[1]


@pytest.fixture(scope="function")
def creamGov():
    return accounts[2]


@pytest.fixture(scope="function")
def alice():
    return accounts[3]


@pytest.fixture(scope="function")
def bob():
    return accounts[4]


@pytest.fixture(scope="function")
def alpha(alphaGov, MockERC20):
    return MockERC20.deploy("ALPHA", "ALPHA", 18, {"from": alphaGov})


@pytest.fixture(scope="function")
def mock_token(bob, MockERC20):
    return MockERC20.deploy("MOCK", "MOCK", 18, {"from": bob})


@pytest.fixture()
def escrow(alpha, alphaGov, creamGov, alice, bob, AlphaEscrow):
    contract = AlphaEscrow.deploy(alpha, alphaGov, creamGov, {"from": alphaGov})
    alpha.mint(creamGov, 10 ** 24)
    alpha.approve(contract, 2 ** 256 - 1, {"from": alphaGov})
    alpha.approve(contract, 2 ** 256 - 1, {"from": creamGov})
    alpha.approve(contract, 2 ** 256 - 1, {"from": alice})
    alpha.approve(contract, 2 ** 256 - 1, {"from": bob})

    alpha.transfer(contract, 10 ** 24, {"from": creamGov})
    return contract
