# StockDetails
This project contains the python script used scraps through the NIFTY 50 - top gainers and top losers and print formatted data on the terminal with Gain/Loss as compared to previous execution of the script.

**stock_details.py** script's can use 2 different approaches for scrapping through the provided urls. First approach use **BeautifulSoup** and second approach uses **lxml**. With lxml package url scrapping is more time efficient as compared to BeautifulSoup package.previous 

On execution of stock_details.py 2 storage files are generated i.e, **gainers.json** and **losers.json**, these json files are used to calculate Gain/Lost percentage as compared to previous script execution. 

**Indication for output generated**
```
Green text: percentage gain or no change
Red text: Percentage loss
```

The project also contains the **requirements.txt** contains the packages required for this project.

**Sample Output**
<img width="1199" alt="Screenshot 2021-11-01 at 4 11 17 PM" src="https://user-images.githubusercontent.com/5197288/139659598-711af57c-1dea-4b35-b783-1e795d84b39d.png">
<img width="1210" alt="Screenshot 2021-11-01 at 4 11 42 PM" src="https://user-images.githubusercontent.com/5197288/139659659-ccd4f6de-5418-4d2f-b657-8d9859536e7a.png">

**NOTE: Sample output is showing all 0.0 in Gain/Lost column since I executed the script on closing the stock market.**

