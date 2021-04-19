# ALPHA Escrow 💰

The escrow contract that hold ALPHA tokens to guarantee that Alpha Finance Lab governor will follows Cream Finance agreement until pay off the debt.

- In case of Alpha governor is not follow the agreement to pay the debt, Cream governor can withdraw ALPHA tokens from this contract as a penalty fee. Alpha governor have to check the withdraw request within 7 days to make sure that Cream governor follows the agreement to withdraw ALPHA. If not Alpha governor can cancel the withdraw request. After 7 days of the requesting has passed, Cream governor can claim ALPHA tokens which will send to Cream governor address.
**Note that** only Cream governor can withdraw and claim ALPHA.
- Cream governor can unlock ALPHA tokens of escrow contract to Alpha governor
- In case of emergency, Alpha governor can call `requestLastResort()` function to withdraw all ALPHA tokens from escrow contract with 30 days timelock. Cream governor can cancel the requesting.
**Note that** only Alpha governor can call last resort function.