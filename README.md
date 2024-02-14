## What does Funtastic Scraper do?
Funtastic Scraper allows you to scrape basic product's info from eshop https://www.funtastic.sk/.
You can choose, if you want to scrape info about all categories of products or just some.

It uses selenium in combination with beautifulsoup. 

You can choose from categories:
1. PREDOBJEDNÁVKY
2. SPOLOČENSKÉ HRY
3. KARTOVÉ ZBERATEĽSKÉ HRY
4. KUSOVÉ KARTY TCG
5. DOPLNKY KU HRÁM
6. KNIHY
7. KOMIKSY
8. MANGA V ČEŠTINE
9. KNIHY V ANGLICKOM JAZYKU
10. ANTIKVARIÁT
11. KNIHY A KOMIKSY - VÝPREDAJ
12. AKČNÉ FIGÚRKY
13. DROBNOSTI / MERCHANDISE

You can define it in `config.json` file:

```json
{
  "wanted_categories": ["KOMIKSY", "KNIHY"]
}
```

or you can choose all products, if you left the `config.json` file empty

```json
{
  "wanted_categories": []
}
```

Products info are saved into csv file `products.csv`:
1. url
2. title
3. isbn
4. normal_price
5. price
6. category0
7. category1
8. category2
9. category3
10. category4
