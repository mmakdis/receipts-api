# Receipts API

This is a combination of different APIs and algorithms to:

* Detect, analyze and extract data from receipts.
* Detect & read barcodes on receipts.  
* Receipts image enhancement (super resolution) using different approaches.


# Yada yada

TL:DR we want to turn an image of a receipt:

<img width="400" src="https://user-images.githubusercontent.com/14551392/154231211-a582e790-de20-4d8f-acf8-718007c2d0ff.jpg">

Into:

<img width="400" alt="Screenshot 2022-02-16 at 10 01 17" src="https://user-images.githubusercontent.com/14551392/154231279-4b564095-0b7a-4a48-ae33-050503ce546a.png">

# Image enhancement?

This is what super resolution does:

<img width="362" alt="Screenshot 2022-02-16 at 10 37 58" src="https://user-images.githubusercontent.com/14551392/154237096-ca6686ac-2e85-492a-aa76-631b463e3f03.png">

It helps with reaeding the barcode and makes Textract produce more accurate results.

# Start

Navigate to `api/` to start.