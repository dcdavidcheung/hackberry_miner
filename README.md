# hackberry_miner
Crypto Miner for Hackberry Pi 

The main communication protocol and mining process was implemented already.
Source: https://github.com/ricmoo/nightminer 

The currency that gets mined is dynamic, where our trained model
tells the Raspberry Pi which to mine. The model is trained from historical
data pulled from Binance's API and is infered from the same API.