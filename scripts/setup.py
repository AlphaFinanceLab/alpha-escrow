from brownie import accounts, AlphaEscrow, chain

try:
    from brownie import interface
except:
    pass


def main():
    deployer = accounts[0]
    alphaGov = accounts[1]
    creamGov = accounts[2]
    alice = accounts[3]
    bob = accounts[4]

    alpha = interface.ERC20.deploy("", "ALPHA")
    escrow = AlphaEscrow.deploy(alpha, alphaGov, creamGov, {"from": deployer})

    return deployer, alphaGov, creamGov, alice, bob, alpha, escrow
