from django.db.models import Q, FilteredRelation, Prefetch

from ec.models import Item, Favorite


def create_item(title: str, price: int):
    item = Item(title=title, price=price)
    item.save()


def find_item(user_id, keyword):
    queryset_items = Item.objects
    if keyword:
        queryset_items = queryset_items.filter(Q(title__icontains=keyword))

    # 全ての行を取得する
    queryset_items = queryset_items.all().prefetch_related(
        # ManyToMany の関係のため、先に結果をキャッシュする.
        # キャッシュ時に取得対象のレコードを限定しておくことで必要な行のみキャッシュする
        Prefetch('favorites', queryset=Favorite.objects.select_related('author').filter(author_id=user_id)))

    results = []
    for item in queryset_items:
        print(item.title)
        # キャッシュ済みの結果を利用する.
        # ※ここで filter なので別な条件で取得しようとすると新たなクエリが発行されるため、事前に限定すること
        print(item.favorites.all())
        # 取得結果の存在確認
        print(item.favorites.all().exists())
        results += [{
            'id': item.id,
            'favorite': '★' if item.favorites.all().exists() else '☆',
            'title': item.title,
            'price': item.price,
        }]
    print(results)
    return results


def create_favorite_relation(user_id, item_ids):
    Favorite.objects.bulk_create([Favorite(author_id=user_id, item_id=item_id) for item_id in item_ids])


def remove_favorite_relation(user_id, item_ids):
    Favorite.objects.filter(item_id__in=item_ids, author_id=user_id).delete()
