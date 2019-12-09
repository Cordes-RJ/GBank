# GBank
Parser/Scraper for WoW Add-On Data related to inventory management. Side project to help me get used to python again.


## SET UP (including use in google sheets
*Requires Bagnon and Auctioneer to be installed*
*Will only profile inventory and price data that has been seen post-installation*

### Set up GBank Data Directory
1. Set up google drive for your computer:
https://www.dardanellepublicschools.org/apps/pages/index.jsp?uREC_ID=276518&type=d&pREC_ID=921084
2. Create a GuildBank folder
3. Open notepad and copy paste: time,totalVal,totalGold,totalMarketVal on one line. Save as vault.csv
4. Open notepad and copy paste: index,itemID,Name,Link,Rarity,IconName,Type,Subtype,LastPrice,Ct,MrktVal on one line. Save as warehouse.csv
5. Create a blank .csv and name it manualAdd.csv

### Set Parameters/First Update
6. Clone the code to your computer
7. Go to parameters.csv in code directory and add the path of the guildbank folder as the DriveGBankPath
8. Find your World of Warcraft directory, and within it find where "saved variables" are stored. Copy this path and add it to parameters.csv as your SavedVariablesPath.
9. Add your server name under servername.
10. Create your own polite ScrapeHeader. This is what accompanies data requests to wowhead.
11. Go to characterWhiteList.csv, also within code directory, and add in the characters which you would like to scrape inventory data from (Case Sensitive).
12. Run main.py to populate warehouse and vault files.
optional: Any items you'd like to track which are not currently in your possession, add the itemID to ManualAdd (one itemID per line) and run main.py, it will scrape details from wowhead and add it to your warehouse at an inventory ct of 0.

### Connect to google sheet
13. Create a google sheet.
14. Add two new subsheets named warehouse and vault.
15. Copy the refID for the sheet:
https://docs.google.com/spreadsheets/d/REFidWILLBEHERE/
ex: https://docs.google.com/spreadsheets/d/1KGXaZxHPv1alwWrAzRNUlKkRZhF40TBQ99vt0ocw/
16. Go to Tools -> ScriptEditor.
17. Add the following code:

```
function importRawData() {
  importCSVFromGoogleDrive("warehouse.csv","PASTErefIDHERE","warehouse")
  importCSVFromGoogleDrive("vault.csv","PASTErefIDHERE","vault")
}


function importCSVFromGoogleDrive(csvpath, spreadsheetID, sheetName) {
  var file = DriveApp.getFilesByName(csvpath).next(); //open csv file
  var csvData = Utilities.parseCsv(file.getBlob().getDataAsString()); //get csv
  var sheet = SpreadsheetApp.openById(spreadsheetID).getSheetByName(sheetName); //open spreadsheet and then tab (sheet name)
  sheet.clear(); // empty sheet contents completely
  sheet.getRange(1, 1, csvData.length, csvData[0].length).setValues(csvData); //get range and set values
  Utilities.sleep(100) //give chance for update before moving on
}
```
17. Run -> Run Function -> ImportRawData, this will update your google sheet. You can put this on a time-trigger.
18. Done. Run main.py any time to update your GuildBankData.
