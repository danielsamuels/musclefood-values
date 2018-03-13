# musclefood-values

A simple tool to determine how much of each type of meat you're getting in each MuscleFood hamper.  Might eventually turn into a website.

### Usage

`python script.py`

Enter a URL when prompted.  Example: http://www.musclefood.com/less-than-5-fat

#### Example output:

```
Please enter a URL: http://www.musclefood.com/less-than-5-fat
Skipping 1 x £5 Premium Chicken Breast Voucher - no grams!
Skipping 1 x £4.95 Reduced Carb Protein Pizza Voucher - no grams!
Skipping 1 x £7.50 Super Fresh Salmon Fillets Voucher - no grams!
Skipping 1 x £4.95 Live Clean™ Ready Meal Voucher - no grams!
Meats: {'chicken': Decimal('2852'), 'beef': Decimal('1646'), 'pork': Decimal('350'), 'flavouring': Decimal('808')}
```


### TODO

* Figure out how to get the price, then use that to calculate a price per gram of meat. (Perhaps just ask if we can't get it automatically?)
* Allow entering 2 URLs to perform a direct comparison.
* Handle the "Get all this extra stuff for £1 more!" thing they do.
* Fail more gracely if we're unable to get the product name(s).
* Handle products that allow you to select the quantity: http://www.musclefood.com/seafood-all/seafood/fresh-salmon-fillets.html
