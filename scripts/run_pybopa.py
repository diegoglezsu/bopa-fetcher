"""Small script to query BOPA data using the pybopa library."""

from pybopa.api import Client


def main() -> int:

    date_from = '12/06/2026'
    date_to = '12/06/2026'

    client = Client()

    print(f"\n=== get_bulletin({date_from}) ===")
    boletin = client.get_bulletin(date_from)
    print(f"  num: {boletin.num}")
    print(f"  fecha: {boletin.date}")
    print(f"  sumario keys: {list(boletin.sumario.keys())}")
    print(f"  articles count: {len(boletin.articles)}")
    if boletin.articles:
        print(f"  primera disposicion: {boletin.articles[0]}")

'''
    print(f"\n=== get_article(cod='2026-04782', num='1', date='12/06/2026') ===")
    article = client.get_article(cod="2026-04782", num="1", date="12/06/2026")

    print(f"\n=== get_bulletins(date_from='{date_from}', date_to='{date_to}') ===")
    bulletins = client.get_bulletins(date_from, date_to)
    print(f"  bulletins count: {len(bulletins)}")
    grouped_by_date = {}
    for b in bulletins:
        grouped_by_date.setdefault(b.date, []).append(b)
    for date, bs in grouped_by_date.items():
        print(f"  {date}: {len(bs)} boletín(es)")
    
    print(f"\n=== get_articles(date_from='{date_from}', date_to='{date_to}') ===")
    articles = client.get_articles(date_from, date_to)
    print(f"  articles count: {len(articles)}")
    grouped_by_date = {}
    for d in articles:
        print(d)
        grouped_by_date.setdefault(d.date, []).append(d)
    for date, ds in grouped_by_date.items():
        print(f"  {date}: {len(ds)} artículo(s)")
'''

if __name__ == "__main__":
    raise SystemExit(main())
