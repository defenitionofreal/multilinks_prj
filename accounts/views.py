from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import LoginForm, CustomUserCreationForm, CustomUserChangeForm

from cardapp.forms import *
from cardapp.models import *

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from dal import autocomplete # for tables

from django.core.signing import BadSignature
from .utilities import signer
from smarturlprj.settings import ALLOWED_HOSTS


# custom error pages
def custom_page_not_found_view(request, exception):
    return render(request, "errors/error404.html", {})
def custom_error_view(request, exception=None):
    return render(request, "errors/error500.html", {})
def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/error403.html", {})
def custom_bad_request_view(request, exception=None):
    return render(request, "errors/error400.html", {})


# mixin для того чтобы во всех шаблонах работало условие под задний фон
class BgMixin(object):
    def get_context_data(self, **kwargs):
        context = super(BgMixin, self).get_context_data(**kwargs)
        context['bg'] = Background.objects.filter(user=self.request.user.pk)
        return context

# mixin для ссылок на модули во всех шаблонах
class ModulesMixin(object):
    def get_context_data(self, **kwargs):
        context = super(ModulesMixin, self).get_context_data(**kwargs)
        context['blocks'] = CreateBlock.objects.filter(user=self.request.user.pk)
        return context



class RegisterUser(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('register_done')
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)

class RegisterDoneView(TemplateView):
    template_name = 'register_done.html'

# активация пользователя
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'bad_signature.html')
    user = get_object_or_404(CustomUser, username=username)
    if user.is_activated:
        template = 'user_is_activated.html'
    else:
        template = 'activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

# класс контроддера для изменения данных пользователя
class ChangeUserInfoView(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    template_name = 'forms/profile_edit.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('dashboard')
    success_message = 'Профиль отредактирован'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def get_context_data(self, **kwargs):
        context = super(ChangeUserInfoView, self).get_context_data(**kwargs)
        context['profile'] = CustomUser.objects.all()
        return context


def user_login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    request.session['user_id'] = user.id
                    login(request, user)
                    messages.success(request, 'Вы авторизовались')
                    return redirect('dashboard')
                    #return HttpResponseRedirect(reverse('dashboard'))
                #return HttpResponseRedirect(reverse('dashboard', kwargs={'username': user.username}))
                else:
                    messages.error(request, 'Аккаунт не активен')
                    return render(request, 'registration/login.html', {'form': form})
            else:
                messages.error(request, 'Неверный логин или пароль')
                return render(request, 'registration/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):

    if not 'user_id' in request.session:
        messages.error(request, 'Авторизуйтесь, чтобы попасть в панель управления.')
        return redirect('login')

    blocks = CreateBlock.objects.filter(user=request.user.pk)
    bg = Background.objects.filter(user=request.user.pk)

    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'

    context = {'blocks': blocks, 'bg': bg, 'host': host}
    return render(request, 'dashboard.html', context)

@login_required
def del_block(request, pk):
    delblock = get_object_or_404(CreateBlock, pk=pk, user=request.user)
    delblock.delete()
    messages.success(request, 'Блок успешно был удален')
    return redirect('dashboard')

class AddBlock(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CreateBlock
    form_class = CreateBlockForm
    template_name = 'forms/block_create.html'
    #pk_url_kwarg = 'pk'
    success_url = reverse_lazy('dashboard')
    success_message = "Блок успешно создан"

    def get_initial(self):
        initial = super(AddBlock, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class UpdateBlock(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'forms/block_edit.html'
    form_class = CreateBlockForm
    pk_url_kwarg = "pk"
    #slug_url_kwarg = 'slug'
    #query_pk_and_slug = True
    success_url = reverse_lazy('dashboard')
    success_message = 'Блок был обнавлен'

    def get(self, request, *args, **kwargs):
        query = CreateBlock.objects.get(pk=self.kwargs['pk'])
        #if query.user.id != request.session['user_id']:  dont work with social_auth. Dont know why yet.
        if query.user.id != request.user.id: # solution :)
            messages.error(request, 'Отказано')
            return HttpResponseRedirect(reverse('dashboard'))
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(UpdateBlock, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = CreateBlock.objects.get(pk=pk)
        return obj

# FAQ * FAQ * FAQ * FAQ * FAQ * FAQ * FAQ * FAQ * FAQ * FAQ * FAQ * FAQ * FAQ *

class AddFaq(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CreateFaq
    form_class = CreateFaqForm
    template_name = 'forms/faq_add.html'
    #pk_url_kwarg = 'pk'
    success_url = '.'
    success_message = "Вопрос успешно был создан"

    def get(self, request, *args, **kwargs):
        #pk = self.kwargs.get(self.pk_url_kwarg)
        query = CreateBlock.objects.get(pk=self.kwargs['pk'])
        #if query.user.id != request.session['user_id']:
        if query.user.id != request.user.id:
            messages.error(request, 'Отказано')
            return HttpResponseRedirect(reverse('dashboard'))
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(AddFaq, self).get_initial()
        initial['user'] = self.request.user
        initial['block'] = CreateBlock.objects.get(pk=self.kwargs['pk'])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AddFaq, self).get_context_data(**kwargs)
        context['owner'] = self.request.user
        context['faqs'] = CreateFaq.objects.filter(block=self.kwargs['pk']).filter(user=self.request.user)
        return context

class UpdateFaq(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'forms/faq_change.html'
    form_class = CreateFaqForm
    pk_url_kwarg = "pk"
    #slug_url_kwarg = 'slug'
    #query_pk_and_slug = True
    success_url = reverse_lazy('dashboard')
    success_message = 'Модуль был обнавлен'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return success_url

    def get(self, request, *args, **kwargs):
        next = request.GET.get('next', '/')
        query = CreateFaq.objects.get(pk=self.kwargs['pk'])
        #if query.user.id != request.session['user_id']: # dont work with social_django :(
        if query.user.id != request.user.id: # solution :)
            messages.error(request, 'Отказано')
            return HttpResponseRedirect(next)
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(UpdateFaq, self).get_initial()
        initial['user'] = self.request.user
        initial['block'] = CreateBlock.objects.get(blockfaq=self.kwargs['pk'])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = CreateFaq.objects.get(pk=pk)
        return obj

@login_required
def del_faq(request, pk):
    next = request.GET.get('next', '/')
    delfaq = get_object_or_404(CreateFaq, pk=pk, user=request.user)
    delfaq.delete()
    messages.success(request, 'Модуль успешно был удален')
    return redirect(next)




# TABLE * TABLE * TABLE * TABLE * TABLE * TABLE * TABLE * TABLE * TABLE * TABLE * TABLE *

@login_required
def add_table(request, pk):

    query = CreateBlock.objects.get(pk=pk)
    #if query.user.id != request.session['user_id']:
    if query.user.id != request.user.id:
        messages.error(request, 'Отказано')
        return HttpResponseRedirect(reverse('dashboard'))

    initial = {'block': CreateBlock.objects.get(pk=pk),
               'user': CustomUser.objects.get(username=request.user)}

    if request.method == "POST":
        formcat = TableCategoryForm(request.POST, initial=initial, user=request.user)
        if formcat.is_valid():
            cat = formcat.save(commit=False)
            #cat.category = formcat.cleaned_data['category']
            cat.save()
            messages.success(request, 'Категория успешно добавлена')
            return HttpResponseRedirect(reverse('add_table',
                                                kwargs={
                                                    'pk': pk,
                                                },
                                                ))
    else:
        formcat = TableCategoryForm(initial=initial, user=request.user)

    if request.method == "POST":
        formitem = TableItemsForm(request.POST, initial=initial)
        if formitem.is_valid():
            item = formitem.save(commit=False)
            #item.category = formitem.cleaned_data['category']
            item.save()
            messages.success(request, 'Объект успешно добавлен в таблицу')
            return HttpResponseRedirect(reverse('add_table',
                                                kwargs={
                                                    'pk': pk,
                                                },
                                                ))
    else:
        formitem = TableItemsForm(initial=initial)

    tablecat = TableCategory.objects.filter(block=pk)
    tableitem = TableItems.objects.all()
    bg = Background.objects.filter(user=request.user.pk)
    context = {'formcat': formcat, 'formitem': formitem, 'tablecat': tablecat, 'tableitem': tableitem, 'bg': bg,}

    return render(request, 'forms/table_add.html', context)



class CategoryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return TableCategory.objects.none()
        qs = TableCategory.objects.all()
        block = self.forwarded.get('block', None)
        if block:
            qs = qs.filter(block=block)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

@login_required
def del_item(request, pk):
    next = request.GET.get('next', '/')
    delitem = get_object_or_404(TableItems, pk=pk, user=request.user)
    delitem.delete()
    messages.success(request, 'Объект таблицы успешно был удален')
    return redirect(next)

@login_required
def del_cat(request, pk):
    next = request.GET.get('next', '/')
    delcat = get_object_or_404(TableCategory, pk=pk, user=request.user)
    delcat.delete()
    messages.success(request, 'Категория успешно была удалена')
    return redirect(next)

@login_required
def change_item(request, pk):

    query = TableItems.objects.get(pk=pk)
    #if query.user.id != request.session['user_id']:
    if query.user.id != request.user.id:
        messages.error(request, 'Отказано')
        return HttpResponseRedirect(reverse('dashboard'))

    next = request.POST.get('next', '/')
    changeitem = get_object_or_404(TableItems, pk=pk, user=request.user)
    if request.method == 'POST':
        changeitemform = TableItemsForm(request.POST, instance=changeitem)
        if changeitemform.is_valid():
            changeitem = changeitemform.save()
            messages.success(request, 'Объект таблицы обнавлен')
            return HttpResponseRedirect(next)
    else:
        changeitemform = TableItemsForm(instance=changeitem)

    bg = Background.objects.filter(user=request.user.pk)
    context = {'changeitemform': changeitemform, 'bg':bg,}
    return render(request, 'forms/item_change.html', context)


class UpdateTableCat(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'forms/cat_change.html'
    form_class = TableCategoryForm
    pk_url_kwarg = "pk"
    success_url = reverse_lazy('dashboard')
    success_message = 'Категория таблицы обнавленна'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return success_url

    def get(self, request, *args, **kwargs):
        next = request.GET.get('next', '/')
        query = TableCategory.objects.get(pk=self.kwargs['pk'])
        #if query.user.id != request.session['user_id']:
        if query.user.id != request.user.id:
            messages.error(request, 'Отказано')
            return HttpResponseRedirect(next)
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(UpdateTableCat, self).get_initial()
        initial['user'] = self.request.user
        initial['block'] = CreateBlock.objects.get(blocktablecat=self.kwargs['pk'])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = TableCategory.objects.get(pk=pk)
        return obj



# IMAGE * IMAGE IMAGE * IMAGE IMAGE * IMAGE IMAGE * IMAGE IMAGE * IMAGE IMAGE * IMAGE IMAGE * IMAGE

class AddImageView(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AddImage
    form_class = AddImageForm
    template_name = 'forms/image_add.html'
    success_url = '.'
    success_message = "Изображение добавленно"

    def get(self, request, *args, **kwargs):
        #pk = self.kwargs.get(self.pk_url_kwarg)
        query = CreateBlock.objects.get(pk=self.kwargs['pk'])
        #if query.user.id != request.session['user_id']:
        if query.user.id != request.user.id:
            messages.error(request, 'Отказано')
            return HttpResponseRedirect(reverse('dashboard'))
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(AddImageView, self).get_initial()
        initial['user'] = self.request.user
        initial['block'] = CreateBlock.objects.get(pk=self.kwargs['pk'])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AddImageView, self).get_context_data(**kwargs)
        context['image'] = AddImage.objects.filter(block=self.kwargs['pk'])
        return context

@login_required
def del_image(request, pk):
    next = request.GET.get('next', '/')
    delimg = get_object_or_404(AddImage, pk=pk, user=request.user)
    delimg.delete()
    messages.success(request, 'Изображение удаленно')
    return redirect(next)



# VIDEO VIDEO VIDEO VIDEO VIDEO VIDEO VIDEO VIDEO VIDEO VIDEO VIDEO VIDEO VIDEO

class AddVideoView(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = YoutubeVideo
    form_class = AddVideoForm
    template_name = 'forms/video_add.html'
    success_url = '.'
    success_message = "Видео добавленно"

    def get(self, request, *args, **kwargs):
        #pk = self.kwargs.get(self.pk_url_kwarg)
        query = CreateBlock.objects.get(pk=self.kwargs['pk'])
        #if query.user.id != request.session['user_id']:
        if query.user.id != request.user.id:
            messages.error(request, 'Отказано')
            return HttpResponseRedirect(reverse('dashboard'))
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(AddVideoView, self).get_initial()
        initial['user'] = self.request.user
        initial['block'] = CreateBlock.objects.get(pk=self.kwargs['pk'])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AddVideoView, self).get_context_data(**kwargs)
        context['video'] = YoutubeVideo.objects.filter(block=self.kwargs['pk'])
        return context

@login_required
def del_video(request, pk):
    next = request.GET.get('next', '/')
    delvid = get_object_or_404(YoutubeVideo, pk=pk, user=request.user)
    delvid.delete()
    messages.success(request, 'Видео удаленно')
    return redirect(next)




# Links Links Links Links Links Links Links Links Links Links Links Links Links Links

class AddLinkView(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = CreateLink
    form_class = CreateLinkForm
    template_name = 'forms/link_add.html'
    success_url = '.'
    success_message = "Ссылка добавленна"

    def get_initial(self):
        initial = super(AddLinkView, self).get_initial()
        initial['user'] = self.request.user
        initial['block'] = CreateBlock.objects.get(pk=self.kwargs['pk'])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AddLinkView, self).get_context_data(**kwargs)
        context['links'] = CreateLink.objects.filter(block=self.kwargs['pk'])
        return context

    def get(self, request, *args, **kwargs):
        #pk = self.kwargs.get(self.pk_url_kwarg)
        query = CreateBlock.objects.get(pk=self.kwargs['pk'])
        #if query.user.id != request.session['user_id']:
        if query.user.id != request.user.id:
            messages.error(request, 'Отказано')
            return HttpResponseRedirect(reverse('dashboard'))
        return super().get(request, *args, **kwargs)

class UpdateLinkView(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'forms/link_change.html'
    form_class = CreateLinkForm
    pk_url_kwarg = "pk"
    success_url = reverse_lazy('dashboard')
    success_message = 'Модуль был обнавлен'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return success_url

    def get_initial(self):
        initial = super(UpdateLinkView, self).get_initial()
        initial['user'] = self.request.user
        initial['block'] = CreateBlock.objects.get(blocklinks=self.kwargs['pk'])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = CreateLink.objects.get(pk=pk)
        return obj

    def get(self, request, *args, **kwargs):
        next = request.GET.get('next', '/')
        query = CreateLink.objects.get(pk=self.kwargs['pk'])
        #if query.user.id != request.session['user_id']:
        if query.user.id != request.user.id:
            messages.error(request, 'Отказано')
            return HttpResponseRedirect(next)
        return super().get(request, *args, **kwargs)

@login_required
def del_link(request, pk):
    next = request.GET.get('next', '/')
    delink = get_object_or_404(CreateLink, pk=pk, user=request.user)
    delink.delete()
    messages.success(request, 'Ссылка удаленна')
    return redirect(next)



class BackgroundCreateView(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'forms/bg_create.html'
    form_class = BackgroundForm
    success_url = reverse_lazy('dashboard')
    success_message = 'Фон создан'

    def get_initial(self):
        initial = super(BackgroundCreateView, self).get_initial()
        initial['user'] = CustomUser.objects.get(pk=self.kwargs['pk'])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, *args, **kwargs):
        obj = super(BackgroundCreateView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise Http404()
        return obj

class BackgroundUpdateView(BgMixin, ModulesMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'forms/bg_edit.html'
    form_class = BackgroundForm
    model = Background
    pk_url_kwarg = "pk"
    #slug_url_kwarg = 'slug'
    #query_pk_and_slug = True
    success_url = reverse_lazy('dashboard')
    success_message = 'Фон отредактирован'

    def get_initial(self):
        initial = super(BackgroundUpdateView, self).get_initial()
        initial['user'] = self.request.user
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = Background.objects.filter(user=pk)[0]
        return obj







# ELSE TRIES aka TRASH. Could be useful somehow somewhere.

#@login_required
#def change_link(request, pk):
#    next = request.POST.get('next', '/')
#    changelink = get_object_or_404(CreateLink, pk=pk)
#    if request.method == 'POST':
#        changelinkform = CreateLinkForm(request.POST, instance=changelink)
#        if changelinkform.is_valid():
#            changelink = changelinkform.save()
#            messages.success(request, 'Ссылка обнавленна')
#            return HttpResponseRedirect(next)
#    else:
#        changelinkform = CreateLinkForm(instance=changelink)
#    context = {'changelinkform': changelinkform,}
#    return render(request, 'forms/link_change.html', context)

#class AddTable(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#    #model = TableCategory
#    form_class = TableCategoryForm
#    second_form_class = TableItemsForm
#    template_name = 'forms/table_add.html'
#    success_url = '.'
#    success_message = "Категория таблицы успешно добавленна"
#
#   def get_initial(self):
#        initial = super(AddTable, self).get_initial()
#        initial['user'] = self.request.user
#        initial['block'] = CreateBlock.objects.get(pk=self.kwargs['pk'])
#        return initial
#
#    def get_context_data(self, **kwargs):
#        context = super(AddTable, self).get_context_data(**kwargs)
#        context['tablecat'] = TableCategory.objects.filter(block=self.kwargs['pk']).filter(user=self.request.user)
#        context['tableitem'] = TableItems.objects.all()
#
#
#       #if 'formcat' not in context:
#        #    context['formcat'] = self.form_class()
#        if 'formitem' not in context:
#            context['formitem'] = self.second_form_class()
#        return context


#def load_categories(request):
#    block_id = request.GET.get('pk')
#    categories = TableCategory.objects.filter(block_id=block_id)
#    return render(request, 'partials/cat_dropdown.html', {'categories': categories})



#class AddCat(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#    #model = TableCategory
#    form_class = TableCategoryForm
#    template_name = 'forms/cat_add.html'
#    success_url = 'add_table'
#    success_message = "Категория таблицы успешно добавленна"
#
#    def get_initial(self):
#        initial = super(AddCat, self).get_initial()
#        initial['user'] = self.request.user
#        initial['block'] = CreateBlock.objects.get(pk=self.kwargs['pk'])
#        return initial
#
#    def get_form_kwargs(self):
#        kwargs = super().get_form_kwargs()
#        kwargs['user'] = self.request.user
#        return kwargs


#@login_required
#def change_faq(request, pk):
#    next = request.POST.get('next', '/') # back to prev page
#    faq = get_object_or_404(CreateFaq, pk=pk, user=request.user)
#    if request.method == 'POST':
#        form = CreateFaqForm(request.POST, instance=faq)
#        if form.is_valid():
#            faq = form.save()
#            messages.success(request, 'Модуль был обнавлен')
#            return HttpResponseRedirect(next)
#    else:
#        form = CreateFaqForm(instance=faq)
#    context = {'form': form,}
#    return render(request, 'forms/faq_change.html', context)


#def add_faq(request, pk):
#    if request.method == "POST":
#        form = CreateFaqForm(request.POST)
#        if form.is_valid():
#            faq = form.save(user=request.user)
#            faq.block = CreateBlock.objects.get(pk=pk)
#            #faq = form.save(commit=False)
#            faq.save()
#            messages.success(request, 'Модуль успешно был создан')
#            return HttpResponseRedirect(reverse('dashboard'))
#    else:
#        form = CreateFaqForm()
#
#    return render(request, 'forms/faq_add.html', {'form': form, 'faq': faq})

#def register(request):
#    if request.method == 'POST':
#        user_form = CustomUserCreationForm(request.POST)
#        if user_form.is_valid():
#            new_user = user_form.save(commit=False)
#            new_user.set_password(user_form.cleaned_data['password1'])
#            new_user.save()
#            CustomUser.objects.create(user=new_user)
#            return render(request, 'register_done.html', {'new_user': new_user})
#    else:
#        user_form = CustomUserCreationForm()
#    return render(request, 'register.html', {'user_form': user_form})

#@login_required
#def profile_edit(request):
#    if request.method == 'POST':
#        userform = CustomUserChangeForm(instance=request.user, data=request.POST, files=request.FILES)
#        if userform.is_valid():
#            userform.save()
#    else:
#        userform = CustomUserChangeForm(instance=request.user)
#
#    context = {'userform': userform,}
#    return render(request, 'profile.html', context)


#@login_required
#def change_cat(request, pk):
#
#    query = TableCategory.objects.get(pk=pk)
#    if query.user.id != request.session['user_id']:
#        messages.error(request, 'Отказано')
#        return HttpResponseRedirect(reverse('dashboard'))
#
#    next = request.POST.get('next', '/')
#    changecat = get_object_or_404(TableCategory, pk=pk, user=request.user)
#
#    if request.method == 'POST':
#        changecatform = TableCategoryForm(request.POST, instance=changecat)
#        if changecatform.is_valid():
#            changecat = changecatform.save()
#            messages.success(request, 'Категория таблицы обнавленна')
#            return HttpResponseRedirect(next)
#    else:
#        changecatform = TableCategoryForm(instance=changecat)
#    context = {'changecatform': changecatform,}
#    return render(request, 'forms/cat_change.html', context)



#@login_required
#def change_block(request, pk):
#    changeblock = get_object_or_404(CreateBlock, pk=pk, user=request.user) # проверка пользователя
#    if request.method == 'POST':
#        changeblockform = CreateBlockForm(request.POST, instance=changeblock)
#        if changeblockform.is_valid():
#            changeblock = changeblockform.save()
#            messages.success(request, 'Блок был обнавлен')
#            return HttpResponseRedirect(reverse('dashboard'))
#    else:
#        changeblockform = CreateBlockForm(instance=changeblock)
#    context = {'changeblockform': changeblockform,}
#    return render(request, 'forms/block_change.html', context)


#@login_required
#def dashboard(request):
#    if not 'user_id' in request.session:
#        messages.error(
#            request, 'Your need to login to be able to view this page.')
#        return redirect('/')
#
#    blocks = CreateBlock.objects.filter(user=request.user.pk)
#    bg = Background.objects.filter(user=request.user.pk)
#    # часть кода для создания нового блока
#    if request.method == "POST":
#        formblock = CreateBlockForm(request.POST)
#        if formblock.is_valid():
#            block = formblock.save(commit=False)
#            block.save()
#            messages.success(request, 'Блок успешно был создан')
#    else:
#        formblock = CreateBlockForm(initial={'user': request.user.pk})
#
#    context = {'formblock': formblock,
#               'blocks': blocks,
#               'bg': bg,}
#    return render(request, 'dashboard.html', context)

#def logout(request):
#    #request.session.clear()
#    request.session.flush()
#    return redirect('/')




