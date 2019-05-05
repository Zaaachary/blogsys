from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


from .models import Post, Category, Tag
from .adminforms import PostAdminForm   # 自定义的form
from blogsys.custom_site import custom_site     # 自定义site


class PostInline(admin.TabularInline):  # StackedInline样式与此不同
    fields = ('title', 'desc')
    extra = 1   # 控制额外多几个
    model = Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav', 'owner')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'
    inlines = [PostInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status', 'owner')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """ 自定义过滤器只显示当前用户分类  此前会显示所有分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'       # 查询时 URL 参数的名字

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
        # return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'owner', 'operator'      # operator 是一个自定义字段
    ]                                   # 配置列表页面显示
    list_display_links = []             # 配置哪些字段可以作为链接

    # list_filter = ['category', ]        # 配置页面过滤器
    list_filter = [CategoryOwnerFilter]        # 配置页面过滤器
    search_fields = ['title', 'category__name']    # 配置搜索字段

    actions_on_top = True               # 动作相关的配置 是否展示在顶部
    # actions_on_bottom = True

    # 编辑页面
    # save_on_top = True                 # 保存、编辑、编辑并新建是否在顶部显示
    exclude = ('owner',)

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),       # 添加自定义的CSS属性
            'fields': ('tag',),
        })
    )
    # filter_horizontal = ('tag', )  # 水平过滤器显示tag

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = "操作"

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    class Media:
        css = {
            'all': ("https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js", ),
        }
        js = ("https://cdn.jsdelivr.net/npm/jquery@1.12.4/dist/jquery.min.js", )

