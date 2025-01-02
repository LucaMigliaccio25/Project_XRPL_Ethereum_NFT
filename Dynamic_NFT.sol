// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Import dei contratti di OpenZeppelin direttamente da github
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.9.0/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.9.0/contracts/access/Ownable.sol";

/// @title DynamicNFT
/// @notice Smart Contract per creare un NFT dinamico che rappresenta un avatar (con metadati variabili)
contract DynamicNFT is ERC721URIStorage, Ownable {
    // contatore per assegnare ID unici agli NFT
    uint256 private tokenCounter;
}