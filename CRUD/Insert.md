### CRUD

Insert one

    db.grades.insertOne(
    {
           "account_id": 111333,
           "limit": 12000,
           "products": [
           "Commodity",
           "Brokerage"
           ],
           "last_updated": new Date()
         })



Insert Multiple Documents

Use insertMany() to insert multiple documents at once. Within insertMany(), include the documents within an array. Each document should be separated by a comma. Here's an example:

    db.grades.insertMany(
       [
         {
           "account_id": 232323,
           "limit": 22222,
           "products": [
           "Commodity",
           "Brokerage"
           ],
           "last_updated": new Date()
         },
         {
           "account_id": 456789,
           "limit": 800,
           "products": [
           "CurrencyService",
           "Brokerage",
           "InvestmentStock"
           ],
           "last_updated": new Date()
         },
         {
           "account_id": 7954,
           "limit": 1000,
           "products": [
           "Commodity",
           "CurrencyService"
           ],
           "last_updated": new Date()
         }
       ]
     )

