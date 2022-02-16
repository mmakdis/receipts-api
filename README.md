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

# Bad quality?

Yes! Take this receipt for an example:

<img width="400" src="https://user-images.githubusercontent.com/14551392/154231773-c2d90fb3-f390-48d5-aa23-e09a551c6090.jpg">

You might think this doesn't look so bad and I agree. But let's try scanning for barcodes:

<img width="570" alt="Screenshot 2022-02-16 at 10 32 40" src="https://user-images.githubusercontent.com/14551392/154235964-64d79764-0dcc-40d3-9928-c863a3e13a64.png">

Is my approach wrong? I'm not so sure. I've tried a dozen of different approaches but ZBar has had the best results so far (highest accuracy and performance).

Let's try enhancing the image and scanning again:

<img width="1008" alt="Screenshot 2022-02-16 at 10 35 28" src="https://user-images.githubusercontent.com/14551392/154236483-07dac43e-20f3-4a4b-9ac0-038fb7c0c4d6.png">

Same image, enhanced.
