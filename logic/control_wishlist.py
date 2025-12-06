import json
import os
from app_store.models import DATABASE

PATH_WISHLIST = 'wishlist.json'  # Путь до файла избранного


def view_in_wishlist(username: str = '') -> dict:
    """
    Просматривает содержимое wishlist.json.
    Если пользователя с именем username нет в избранном, создаёт его запись с пустым списком продуктов.

    :param username: Имя пользователя
    :return: Содержимое 'wishlist.json'
    """
    empty_user_wishlist = {'products': []}

    if os.path.exists(PATH_WISHLIST):
        with open(PATH_WISHLIST, encoding='utf-8') as f:
            wishlist = json.load(f)
            if username not in wishlist:
                wishlist[username] = empty_user_wishlist
    else:
        wishlist = {username: empty_user_wishlist}

    # Сохраняем актуальное состояние wishlist
    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f, ensure_ascii=False, indent=4)

    return wishlist


def add_to_wishlist(id_product: str, username: str = '') -> bool:
    """
    Добавляет продукт в избранное. Если продукт уже есть, не дублирует его.

    :param id_product: Идентификатор продукта
    :param username: Имя пользователя
    :return: True, если продукт добавлен успешно; False, если продукта нет в DATABASE
    """
    wishlist = view_in_wishlist(username)

    if id_product not in DATABASE:
        return False

    user_wishlist = wishlist[username]["products"]
    if id_product not in user_wishlist:
        user_wishlist.append(id_product)

    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f, ensure_ascii=False, indent=4)

    return True


def remove_from_wishlist(id_product: str, username: str = '') -> bool:
    """
    Удаляет продукт из избранного.
    Если продукта нет в списке, возвращает False.

    :param id_product: Идентификатор продукта
    :param username: Имя пользователя
    :return: True, если продукт удалён; False, если продукта нет
    """
    wishlist = view_in_wishlist(username)

    user_wishlist = wishlist[username]["products"]

    if id_product not in user_wishlist:
        return False

    user_wishlist.remove(id_product)

    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f, ensure_ascii=False, indent=4)

    return True
