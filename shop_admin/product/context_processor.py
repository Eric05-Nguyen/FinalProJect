def caculate_cart_total(request):
    cart = request.session.get('cart', {})
    cart_count = 0
    for item in cart.values():
        cart_count += item.get('quantity', 0)
    return {'cart_count': cart_count}
