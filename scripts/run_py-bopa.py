"""Small script to query BOPA data using the py-bopa library."""

from bopa.api import Client


def main() -> int:

    date_from = '16/06/2026'
    date_to = '23/06/2026'

    client = Client()


    print(f"\n=== get_bulletins(date_from='{date_from}', date_to='{date_to}', text_contains='Junta General') ===")
    bulletins = client.get_bulletins(date_from, date_to, text_contains="Junta General")
    print(f"  bulletins count: {len(bulletins)}")
    print(f"  bulletins: {[b.to_dict() for b in bulletins]}")

    '''

    print(f"\n=== get_bulletin(date='29/12/2023') === (suplements)")
    boletin = client.get_bulletin(date='29/12/2023')
    to_json = boletin.to_dict()
    print(f"  boletin: {to_json}")

    print(f"\n=== get_article(cod='2026-04782', date='12/06/2026') ===")
    article = client.get_article(cod="2026-04782", date="12/06/2026")
    to_json = article.to_dict()
    print(f"  article: {to_json}")
    '''

    '''
    print(f"\n=== get_article(cod='2023-11737', date='29/12/2023') === (suplements)")
    article = client.get_article(cod="2023-11737", date="29/12/2023")
    to_json = article.to_dict()
    print(f"  article: {to_json}")

    print(f"\n=== get_bulletins(date_from='{date_from}', date_to='{date_to}') ===")
    bulletins = client.get_bulletins(date_from, date_to)
    print(f"  bulletins count: {len(bulletins)}")
    grouped_by_date = {}
    for b in bulletins:
        grouped_by_date.setdefault(b.date, []).append(b)
    for date, bs in grouped_by_date.items():
        print(f"  {date}: {len(bs)} boletín(es)")
    '''
    print(f"\n=== get_articles(date_from='{date_from}', date_to='{date_to}', text_contains='Junta General') ===")
    articles = client.get_articles(date_from, date_to, text_contains="Junta General")
    print(f"  articles count: {len(articles)}")
    grouped_by_date = {}
    for d in articles:
        print(d)
        grouped_by_date.setdefault(d.date, []).append(d)
    for date, ds in grouped_by_date.items():
        print(f"  {date}: {len(ds)} artículo(s)")
    

if __name__ == "__main__":
    raise SystemExit(main())
