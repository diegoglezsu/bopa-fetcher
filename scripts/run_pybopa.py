"""Small script to query BOPA data using the pybopa library."""

from pybopa.api import Client


def main() -> int:

    date_from = '12/06/2026'
    date_to = '13/06/2026'

    client = Client()

    print(f"\n=== get_bulletin({date_from}) ===")
    boletin = client.get_bulletin(date_from)
    to_json = boletin.to_dict()
    print(f"  boletin: {to_json}")
    '''
    print(f"\n=== get_bulletin({date_to}) ===")
    boletin = client.get_bulletin(date_to)
    to_json = boletin.to_dict()
    print(f"  boletin: {to_json}")
    '''

    print(f"\n=== get_article(cod='2026-04782', num='1', date='12/06/2026') ===")
    article = client.get_article(cod="2026-04782", num="1", date="12/06/2026")
    to_json = article.to_dict()
    print(f"  article: {to_json}")

    '''
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
