# rss-filter
Filtre un flux RSS et recrée un flux propre.

#### Exécution planifiée (toutes les 20min)
sudo echo "*/20 * * * * user /usr/bin/python /home/user/scripts/rss-filter.py > /dev/null 2>&1" > /etc/cron.d/fetch_feeds
