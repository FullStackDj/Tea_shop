from django.http import JsonResponse
from django.views import View

from carts.mixins import CartMixin
from carts.models import Cart
from goods.models import Products


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get('product_id')

        try:
            product = Products.objects.get(id=product_id)
        except Products.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'}, status=404)

        cart = self.get_cart(request, product=product)

        if cart:
            cart.quantity += 1
            cart.save()
            message = 'Product quantity has been updated.'
        else:
            Cart.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else None,
                product=product,
                quantity=1
            )
            message = 'Product has been added.'

        response_data = {
            'message': message,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        cart = self.get_cart(request, cart_id=cart_id)

        if cart is None:
            return JsonResponse({'error': 'Cart item not found.'}, status=404)

        cart.quantity = int(request.POST.get('quantity', 1))
        cart.save()

        response_data = {
            'message': 'Amount of product has been changed.',
            'quantity': cart.quantity,
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        cart = self.get_cart(request, cart_id=cart_id)

        if not cart:
            return JsonResponse({'error': 'Cart item not found.'}, status=404)

        cart.delete()

        response_data = {
            'message': 'Product has been removed.',
            'cart_items_html': self.render_cart(request)
        }

        return JsonResponse(response_data)
