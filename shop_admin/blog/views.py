from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Count
from .models import Blog, Rates, Comments

# Create your views here.

def blog_list_view(request):
    blog_list=Blog.objects.all().order_by('-created_at')
    paginator=Paginator(blog_list,3)
    page_number=request.GET.get('page')
    blogs=paginator.get_page(page_number)
    return render(request,'blogList.html',{'blogs':blogs,'paginator':paginator,})

def blog_detail_view(request,id):
    blog_item = get_object_or_404(Blog, id=id)
    pre_blog = Blog.objects.filter(id__lt=blog_item.id).order_by('-id').first()
    next_blog = Blog.objects.filter(id__gt=blog_item.id).order_by('id').first()    

    rate_list=Rates.objects.filter(blog=blog_item) 
    total_votes=len(rate_list)

    sum_rate=0;
    for r in rate_list:
        sum_rate+=r.rates

    if total_votes>0:
        avg_rate=sum_rate/total_votes
    else:
        avg_rate=0;
   
    comments = Comments.objects.filter(blog=blog_item,parent_comment=None).order_by('-created_at')

    context={
        'blog':blog_item,
        'prev_blog':pre_blog,
        'next_blog':next_blog,
        'avg_rate':round(avg_rate,1),
        'total_votes':total_votes,
        'stars':range(1,6),
        'comments': comments,
    }    
    return render(request,'blogDetail.html',context)
    
   
@csrf_exempt
def blog_rate(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        rate = request.POST.get('rate')
        author_id = request.POST.get('author_id')
        
        try:
            blog = Blog.objects.get(id=blog_id)
            
            if Rates.objects.filter(blog_id=blog_id, author_id=author_id).exists():
                return JsonResponse({'success': False, 'error': 'Bạn đã đánh giá bài viết này rồi!'})
                
            Rates.objects.create(blog_id=blog_id, rates=int(rate), author_id=author_id)
            return JsonResponse({'success': True})
            
        except Blog.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Blog not found'})
            
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def blog_comment(request):
    if request.method=='POST':
        blog_id=request.POST.get('blog_id')
        comment=request.POST.get('comment')
        parent_id=request.POST.get('parent_id')
        
        if request.user.is_authenticated:
            author=request.user
            author_id=request.user.id
            author_name=request.user.username
            author_image=request.user.avatar
        
            data= {
                'blog_id':blog_id,
                'comment':comment,
                'author_name':author_name,
                'author_image':author_image,
                'author_id':author_id,
            }    
            
            if parent_id:
                data['parent_comment_id']=parent_id
            try:
                new_comment=Comments.objects.create(**data)
                comment_data=Comments.objects.filter(id=new_comment.id).values().first()
                return JsonResponse({'success':True,'comment':comment_data})
            except Exception as e:
                return JsonResponse({'success':False,'error': str(e)})
        
        return JsonResponse({'success':False,'error':'k k user'})
    return JsonResponse({'success':False,'error':'Invalid request'})


