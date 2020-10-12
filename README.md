## Portfolio Management with Constrained Optimization

### Description:
This is a sample portfolio management system for backtesting and research purpose. It takes data from excel file and output backtesting results into '.png'.

It has implemented methods of "equal weighted","equalvol weighted","mean-variance weighted","mean-variance-blacklitterman weighted".

It allows user defined rebalance period and model hyper-paramaters can also be changed as specified needs.

To run it on different assets space, please follow the same dataset structure detailed in readData.py file and stored them into "Data.xlsx"

### Installation:
Before installation please make sure you have the correction version of python(3.8).

This project does not need database and it is automatically runnable after unzip.

Please refer to main.py as the root for this system.

### How To run:
After get a cleaned dataset stored in the same location as our root funtion with name "Data.xlsx" and some other specifics details in the readData.py,

just choose a method for portfolio construction and run the main.py function.

The result will be auto-populated into outPut folder in a picture format.

### Project Outline:
This project includes 3 main parts: readData, backTest and reportGeneration.
	1. readData: I specified data structure here which need to be followed in order to run this system. Please pay attention to it since it also
		     take some responsibilities of calculation, ex. generate expected returns for black littlerman model.
	2. backTest: Main loop for portfolio rebalancing and value calcualtion also will be populated in this function.
	3. reportGeneration: Generate portfolio backtest report also calcualte some additional risk factors in this function.

### License:
Shaolun Du

Feel free to change anything that comfortable you also if you find these thing interesting please contact me at Shaolun.du@gmail.com.
