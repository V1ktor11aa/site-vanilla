from decimal import Decimal 
from django.conf import settings 
from coffee.models import Coffee 
 
 
class Cart(object): 
 
    def __init__(self, request): 
        """ 
        Инициализация корзины 
        """ 
        self.session = request.session 
        cart = self.session.get(settings.CART_SESSION_ID) 
        if not cart: 
            # сохраняем ПУСТУЮ корзину в сессии 
            cart = self.session[settings.CART_SESSION_ID] = {} 
        self.cart = cart 
 
    def __iter__(self): 
        """ 
        Перебираем товары в корзине и получаем товары из базы данных. 
        """ 
        Coffee_ids = self.cart.keys() 
        # получаем товары и добавляем их в корзину 
        products = Coffee.objects.filter(id__in=Coffee_ids) 
 
        cart = self.cart.copy() 
        for Coffee in products: 
            cart[str(Coffee_ids)]['coffee'] = Coffee 
 
        for item in cart.values(): 
            item['prise'] = Decimal(item['prise']) 
            item['total_price'] = item['prise'] * item['quantity'] 
            yield item 
     
    def __len__(self): 
        """ 
        Считаем сколько товаров в корзине 
        """ 
        return sum(item['quantity'] for item in self.cart.values()) 
 
    def add(self, Coffee, quantity=1, update_quantity=False): 
        """ 
        Добавляем товар в корзину или обновляем его количество. 
        """ 
        Coffee_id = str(Coffee.id) 
        if Coffee_id not in self.cart: 
            self.cart[Coffee_id] = {'quantity': 0, 
                                      'prise': str(Coffee.prise)} 
        if update_quantity: 
            self.cart[Coffee_id]['quantity'] = quantity 
        else: 
            self.cart[Coffee_id]['quantity'] += quantity 
        self.save() 
 
    def save(self): 
        # сохраняем товар 
        self.session.modified = True 
 
    def remove(self, Coffee): 
        """ 
        Удаляем товар 
        """ 
        Coffee_id = str(Coffee_id) 
        if Coffee_id in self.cart: 
            del self.cart[Coffee_id] 
            self.save() 
 
    def get_total_price(self): 
        # получаем общую стоимость 
        return sum(Decimal(item['prise']) * item['quantity'] for item in self.cart.values()) 
 
    def clear(self): 
        # очищаем корзину в сессии 
        del self.session[settings.CART_SESSION_ID] 
        self.save()