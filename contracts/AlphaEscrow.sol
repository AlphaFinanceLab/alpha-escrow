pragma solidity 0.6.12;

import 'OpenZeppelin/openzeppelin-contracts@3.2.0/contracts/token/ERC20/IERC20.sol';
import 'OpenZeppelin/openzeppelin-contracts@3.2.0/contracts/token/ERC20/SafeERC20.sol';
import 'OpenZeppelin/openzeppelin-contracts@3.2.0/contracts/utils/ReentrancyGuard.sol';
import 'OpenZeppelin/openzeppelin-contracts@3.2.0/contracts/math/SafeMath.sol';

contract AlphaEscrow is ReentrancyGuard {
  using SafeERC20 for IERC20;
  using SafeMath for uint;

  event Withdraw(uint indexed receiptId, uint amount, uint withdrawTime, address gov);
  event Claim(uint indexed receiptId, uint amount, address gov);
  event Cancel(uint indexed receiptId, address gov);
  event Unlock(address gov, uint amount);
  event RequestEmergency(address gov, uint requestTime);
  event CancelEmergency(address gov, uint cancelTime);
  event ClaimEmergenty(address gov, uint amount, uint claimTime);

  uint public constant STATUS_PENDING = 1;
  uint public constant STATUS_CANCELLED = 2;
  uint public constant STATUS_CLAIMED = 3;
  uint public constant TIMELOCK_DURATION = 7 days;
  uint public constant EMERGENCY_WITHDRAW_TIMELOCK_DURATION = 30 days;

  struct WithdrawReceipt {
    uint amount;
    uint withdrawTime;
    uint status;
  }

  IERC20 public alpha;
  address public alphaGovernor;
  address public creamGovernor;
  uint public withdrawReceiptId;
  mapping(uint => WithdrawReceipt) public receipts;
  uint public emergencyRequestTime;

  modifier onlyAlphaGov() {
    require(msg.sender == alphaGovernor, 'only Alpha governor');
    _;
  }

  modifier onlyCreamGov() {
    require(msg.sender == creamGovernor, 'only Cream governor');
    _;
  }

  constructor(
    address _alpha,
    address _alphaGovernor,
    address _creamGovernor
  ) public {
    alpha = IERC20(_alpha);
    alphaGovernor = _alphaGovernor;
    creamGovernor = _creamGovernor;
    withdrawReceiptId = 0;
  }

  /// @dev Create withdraw receipt by CREAM governor
  /// @param _amount Amount of ALPHA to withdraw
  function withdraw(uint _amount) external nonReentrant onlyCreamGov {
    require(_amount > 0, 'cannot withdraw 0 alpha');
    WithdrawReceipt storage receipt = receipts[withdrawReceiptId];
    receipt.amount = _amount;
    receipt.withdrawTime = block.timestamp;
    receipt.status = STATUS_PENDING;
    withdrawReceiptId++;
    emit Withdraw(withdrawReceiptId, _amount, block.timestamp, msg.sender);
  }

  /// @dev Claim ALPHA using withdrawal receipt by CREAM governor
  /// note: CREAM governor can withdraw receipt afters timelock duration.
  /// @param _receiptId The ID of withdrawal receipt to claim ALPHA
  function claim(uint _receiptId) external nonReentrant onlyCreamGov {
    WithdrawReceipt storage receipt = receipts[withdrawReceiptId];
    require(receipt.status == STATUS_PENDING, 'claim/receipt has cancelled or claimed');
    require(
      block.timestamp >= receipt.withdrawTime.add(TIMELOCK_DURATION),
      'invalid time to claim'
    );
    receipt.status = STATUS_CLAIMED;
    alpha.safeTransfer(msg.sender, receipt.amount);
    emit Claim(_receiptId, receipt.amount, msg.sender);
  }

  /// @dev Cancel withdrawal receipt by ALPHA governor.
  /// note: ALPHA governor can cancel withdrawal receipt that still in timelock duration.
  /// @param _receiptId The ID of withdrawal receipt to cancel
  function cancelWithdrawReceipt(uint _receiptId) external nonReentrant onlyAlphaGov {
    WithdrawReceipt storage receipt = receipts[withdrawReceiptId];
    require(receipt.status == STATUS_PENDING, 'only pending receipt can be cancel');
    require(
      block.timestamp < receipt.withdrawTime.add(TIMELOCK_DURATION),
      'cannot cancel receipt that exceed timelock'
    );
    receipt.status = STATUS_CANCELLED;
    emit Cancel(_receiptId, msg.sender);
  }

  /// @dev Unlock ALPHA token to ALPHA governor
  /// @param _amount Amount of ALPHA to unlock
  function unlock(uint _amount) external nonReentrant onlyCreamGov {
    alpha.safeTransfer(alphaGovernor, _amount);
    emit Unlock(alphaGovernor, _amount);
  }

  /// @dev Emergency withdraw ALPHA from this contract by ALPHA governor
  function requestEmergencyWithdraw() external nonReentrant onlyAlphaGov {
    emergencyRequestTime = block.timestamp;
    emit RequestEmergency(msg.sender, block.timestamp);
  }

  /// @dev Cancel emergency withdraw ALPHA by CREAM governor only
  function cancelEmergencyWithdraw() external nonReentrant onlyCreamGov {
    emergencyRequestTime = 0;
    emit CancelEmergency(msg.sender, block.timestamp);
  }

  /// @dev Claim emergency withdraw ALPHA by ALPHA governor
  function claimEmergencyWithdraw() external nonReentrant onlyAlphaGov {
    require(
      emergencyRequestTime > 0 &&
        block.timestamp >= emergencyRequestTime.add(EMERGENCY_WITHDRAW_TIMELOCK_DURATION),
      'invalid time to claim emergency withdrawn ALPHA'
    );
    emergencyRequestTime = 0;
    uint amount = alpha.balanceOf(address(this));
    alpha.safeTransfer(msg.sender, amount);
    emit ClaimEmergenty(msg.sender, amount, block.timestamp);
  }

  /// @dev Recover any ERC20 token except ALPHA from this contract
  /// @param _token ERC20 Token address to recover from this contract
  function recover(address _token) external nonReentrant onlyAlphaGov {
    require(_token != address(alpha), 'cannot recover ALPHA');
    IERC20 token = IERC20(_token);
    uint amount = token.balanceOf(address(this));
    token.safeTransfer(msg.sender, amount);
  }
}
