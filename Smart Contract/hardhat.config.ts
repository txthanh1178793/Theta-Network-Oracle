import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
require('dotenv').config();
const { PRIVATE_KEY } = process.env;

const config: HardhatUserConfig = {
  solidity: "0.8.17",
  networks: {
    theta_testnet: {
      url: "https://eth-rpc-api-testnet.thetatoken.org/rpc",
      accounts: [PRIVATE_KEY],
      allowUnlimitedContractSize: true
    }
  },
};

export default config;
