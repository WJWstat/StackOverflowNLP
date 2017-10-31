# Metrics
Total number of tokens = 9,892   

### True Positives
* Count = 8710   

### True Negatives
* Count = 1176  

### False Positives
* Count = 4    
* **;))**   
    * *;*, *)*, *)* --> *;)*, *)*   
* **properties'**   
    * *properties*, *'* --> *properties'*   
* **beginning:)**   
    * *beginning*, *:*, *)*, -->  *beginning*, *:)*   
* **free:)**
    * *free*, *:*, *)*, --> *free*, *:)*   

### False Negatives
* Count = 2   
* **caching/db/etc**   
    * *caching/db/etc* --> *caching*, */*, *db*, */*, *etc*
* **pass/failure/correctness**   
    * *pass/failure/correctness*, --> *pass*, */*, *failure*, */*, *correctness*   
