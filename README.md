# rss-filter
Filtre un flux RSS et recrée un flux propre.

#### Personnalisation

Le nouveau flux RSS généré sera composé des articles dont le titre **ne contient pas** l'une des expressions de la liste `filters`. Pour personnaliser vos filtres, ajoutez vos expressions comme indiqué ci-dessous :
```python
filters = (
    u'Nintendo', u'T-Shirt enfant', u'XBOX One|360', u'jeux video',
    u'DVD', u'@ DX', u'onsole Xbox', u'@ Priceminister',
    u'Sélection de jeux', u'PS[34P]', u'Blu[\s-]?Ray', u'Steam',
    u'Wii', u'Playstation', u'@ Mcdonalds', u'@ Quick', u'@ action',
    u'@ Meccanodirect', u'sur 3DS??|PC', u'TV \d{2}"|\s?pouces')
```

#### Exécution planifiée (toutes les 20min)
```bash
sudo echo "*/20 * * * * user /usr/bin/python /home/user/rss-filter/rss-filter.py > /dev/null 2>&1" > /etc/cron.d/fetch_feeds
```
