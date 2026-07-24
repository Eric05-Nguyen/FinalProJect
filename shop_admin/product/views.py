from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Brand, Product
from django.http import JsonResponse
import os
from django.conf import settings
import time
from django.shortcuts import redirect
from PIL import Image
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.csrf import csrf_exempt 
@login_required(login_url='login')
def add_product(request):
    if request.method=='POST':
        name=request.POST.get('name')
        price=request.POST.get('price')
        category=request.POST.get('id_category')
        brand=request.POST.get('id_brand')
        status=request.POST.get('state')
        sale_percentage=request.POST.get('sale_percentage')
        company_profile=request.POST.get('company_profile')
        images=request.FILES.getlist('image')
        description=request.POST.get('description')
        
        errors={}
        if not name:
            errors['name']='Tên sản phẩm không được để trống'
        if not price:
            errors['price']='Giá sản phẩm không được để trống'
        else :
            try:
                price=float(price)
                if price < 0 :
                    errors['price'] = 'Giá phải là số dương'
            except ValueError:
                errors['price'] = 'Giá không hợp lệ'
        if not category:
            errors['category']='Danh mục sản phẩm không được để trống'
        if not brand:
            errors['brand']='Thương hiệu sản phẩm không được để trống'
        if not status:
            errors['status']='Trạng thái sản phẩm không được để trống'

        if not company_profile:
            errors['company_profile']='Thông tin công ty không được để trống'
        if not images:
            errors['image']='Ảnh sản phẩm không được để trống'
        elif len(images)>3:
            errors['image']='Ảnh sản phẩm không được vượt quá 3 ảnh'
        else:
            for img in images:
                if img.content_type not in ['image/jpeg', 'image/png']:
                    errors['image']='Ảnh sản phẩm không hợp lệ'
                    break
                if img.size > 1024*1024:
                    errors['image']='Ảnh sản phẩm không được vượt quá 1MB'
                    break

        # Xử lý lưu tên ảnh 

        save_imagenames=[]
        for img in images:
            imagename=img.name.replace(' ','_')
            base,ext=os.path.splitext(imagename)    
            ext=ext.lower()
            
            save_folder=os.path.join(settings.MEDIA_ROOT,'product_images')
            os.makedirs(save_folder,exist_ok=True)

            original_save_path=os.path.join(save_folder,f"{base}{ext}")    

            with open(original_save_path,"wb+") as dest:
                for chunk in img.chunks():
                    dest.write(chunk)

            # Chỉ lưu tên ảnh gốc vào CSDL
            save_imagenames.append(f"{base}{ext}")  

            # Resize ảnh
            img_obj=Image.open(original_save_path)
            for size in [100,400]:
                img_copy=img_obj.copy()
                img_copy.thumbnail((size,size))
                resize_name=f"{size}_{size}{ext}"
                resized_save_path=os.path.join(save_folder,resize_name)
                img_copy.save(resized_save_path)

        if not description:
            errors['description']='Mô tả sản phẩm không được để trống'
        
        if errors:
            return JsonResponse({'status':'error','errors': errors})
        else:
            product=Product.objects.create(
                name=name,
                price=price,
                id_category_id=category, 
                id_brand_id=brand,        
                status=status,
                sale_percentage=sale_percentage if sale_percentage else 0,
                CompaniProFile=company_profile, 
                description=description,
                id_user=request.user,
                images=save_imagenames
            )
                
        return JsonResponse({'status': 'success', 'message': 'Thành công!'})

    categories= Category.objects.all()
    brands= Brand.objects.all()
    return render(request,'add_product.html',{'categories':categories,'brands':brands})

@login_required(login_url='login')
def my_products(request):
    products = Product.objects.filter(id_user=request.user).order_by('-id')
    return render(request, 'my-product.html', {'products': products})

@login_required(login_url='login')
def edit_product(request, id):
    product=Product.objects.get(id=id)
    
    if request.method=='POST':
        name= request.POST.get('name')
        price= request.POST.get('price')
        category= request.POST.get('id_category')
        brand= request.POST.get('id_brand')
        status= request.POST.get('state')
        sale_percentage= request.POST.get('sale_percentage')
        company_profile= request.POST.get('company_profile')
        images= request.FILES.getlist('image')
        description= request.POST.get('description')
        errors={}
        if not name:
            errors['name']='Tên sản phẩm không được để trống'
        if not price:
            errors['price']='Giá sản phẩm không được để trống'
        else :
            try:
                price=float(price)
                if price < 0 :
                    errors['price'] = 'Giá phải là số dương'
            except ValueError:
                errors['price'] = 'Giá không hợp lệ'
        if not category:
            errors['category']='Danh mục sản phẩm không được để trống'
        if not brand:
            errors['brand']='Thương hiệu sản phẩm không được để trống'
        if not status:
            errors['status']='Trạng thái sản phẩm không được để trống'
        if not company_profile:
            errors['company_profile']='Thông tin công ty không được để trống'
        
        current_images = product.get_image_list
        count_CurretnImage = len(current_images)
        count_newImage=len(images) if images else 0
        delete_img=request.POST.getlist('delete_image')
        count_deleteImage=len(delete_img) if delete_img else 0
        total_image=count_CurretnImage-count_deleteImage+count_newImage
        if total_image==0:
            errors['image']='Ảnh sản phẩm không được để trống'
        elif total_image>3:
            errors['image']='Tổng ảnh mới + cũ của sản phẩm không được vượt quá 3 ảnh'
        else:
            for img in images:
                if img.content_type not in ['image/jpeg', 'image/png']:
                    errors['image']='Ảnh sản phẩm không hợp lệ'
                    break
                if img.size > 1024*1024:
                    errors['image']='Ảnh sản phẩm không được vượt quá 1MB'
                    break
        if not description:
            errors['description']='Mô tả sản phẩm không được để trống'
        if errors:
            return JsonResponse({'status':'error','errors': errors})
        else:
            product.name=name
            product.price=price
            product.id_category_id=category
            product.id_brand_id=brand
            product.status=status
            product.sale_percentage=sale_percentage if sale_percentage else 0
            product.CompaniProFile=company_profile
            product.description=description
            product.save()

        current_images = product.get_image_list
        
        if delete_img:
            for img_name in delete_img:
                if img_name in current_images:
                    current_images.remove(img_name)
                for size in [100,400]:
                    base ,ext= os.path.splitext(img_name)
                    file_del = f"{size}_{size}{ext}"
                    file_path = os.path.join(settings.MEDIA_ROOT, 'product_images', file_del)
                    if os.path.exists(file_path):
                        os.remove(file_path)
        if images:
            save_folder = os.path.join(settings.MEDIA_ROOT, 'product_images')
            os.makedirs(save_folder, exist_ok=True)
            for img in images:
                imagename = img.name.replace(' ', '_')
                base, ext = os.path.splitext(imagename)
                ext = ext.lower()
                original_save_path = os.path.join(save_folder, f"{base}{ext}")
                with open(original_save_path, "wb+") as dest:
                    for chunk in img.chunks():
                        dest.write(chunk)
                current_images.append(f"{base}{ext}")
                # Resize
                img_obj = Image.open(original_save_path)
                for size in [100, 400]:
                    img_copy = img_obj.copy()
                    img_copy.thumbnail((size, size))
                    resized_save_path = os.path.join(save_folder, f"{size}_{size}{ext}")
                    img_copy.save(resized_save_path)

        product.images = current_images
        product.save()
        return JsonResponse({'status': 'success', 'message': 'Cập nhật thành công!'})
    
    # nếu method = get
    categories=Category.objects.all()
    brands=Brand.objects.all()
    return render(request,'edit-product.html',{'product':product,'categories':categories,'brands':brands})

def delete_product(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return redirect('my_products')     

def product_detail(request,id):
    product=Product.objects.get(id=id)
    recommended_products=Product.objects.all()[:6]
    return render(request,'product-details.html',{'product':product,'recommended_products':recommended_products})


def add_to_cart(request,id):
    if request.method=='POST':
        product=get_object_or_404(Product,id=id)
        quantity=int(request.POST.get('quantity',1))
        cart=request.session.get('cart',{})
        product_id_str=str(product.id)
        if product_id_str in cart:
            cart[product_id_str]['quantity']+=quantity
        else:
            cart[product_id_str]={
                'name':product.name,
                'price':float(product.price),
                'quantity':quantity,
                'id':product.id,
                'image':product.get_image_list[0] if product.get_image_list else '',
            }
        request.session['cart']=cart
        return redirect('cart')
    return redirect('product_detail',id=id)

def cart(request):
    cart=request.session.get('cart',{})
    total_price_all=0;
    total_single_price=0;
    for item in cart.values():
        item['total_single_price']=item['price']*item['quantity']
        total_price_all+=item['total_single_price']    
    return render(request,'cart.html',{'cart':cart,'total_single_price':total_single_price  ,'total_price_all':total_price_all})

@csrf_exempt 
def update_cart_ajax(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            product_id=str(data.get('product_id'))
            action=data.get('action')
            cart=request.session.get('cart',{})

            target_key = None
            if product_id in cart:
                target_key = product_id
            elif int(product_id) in cart:
                target_key = int(product_id)

            if target_key is None:
                return JsonResponse({'status': 'error', 'message': 'Sản phẩm không tồn tại trong giỏ hàng!'})
            
            if action=='up':
                cart[target_key]['quantity']+=1
            elif action == 'down':
                cart[target_key]['quantity']-=1
                if cart[target_key]['quantity'] <= 0:
                    del cart[target_key]
            elif action == 'delete':
                del cart[target_key]

            request.session['cart'] = cart
            request.session.modified = True

            item_total = 0
            quantity = 0
            if target_key in cart:
                item_total = cart[target_key]['price'] * cart[target_key]['quantity']
                quantity = cart[target_key]['quantity']

            cart_total=0
            cart_count=0
            for item in cart.values():
                cart_count+=item['quantity']
                cart_total+=item['price']*item['quantity']

            return JsonResponse({
                'status':'success',
                'quantity': quantity,
                'item_total': item_total,
                'cart_total': cart_total,
                'cart_count': cart_count
            })
        except Exception as e:
            return JsonResponse({'status':'error','message': str(e)})

    return JsonResponse({'status':'error','message':'Cập nhật thất bại!'})    