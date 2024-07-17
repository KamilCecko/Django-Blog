from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm


def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date']

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        cat_menu = Category.objects.all()
        context["cat_menu"] = cat_menu
        category_images_dict = {}
        for category in cat_menu:
            if category.category_image:
                category_images_dict[category.name] = category.category_image.url
        context["category_images"] = category_images_dict
        return context


def category_list_view(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list})


def category_view(request, cats):
    category = get_object_or_404(Category, name=cats)
    category_posts = Post.objects.filter(category=category)
    context = {
        'category': category,
        'category_posts': category_posts
    }
    return render(request, 'categories.html', context)


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        cat_menu = Category.objects.all()
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = post.total_likes()
        liked = post.likes.filter(id=self.request.user.id).exists()
        context["cat_menu"] = cat_menu
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'


class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'


class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
