from django.contrib import admin
from .models import Farm, Device, Observation, Alert
from django.http import HttpResponse
import csv


admin.site.site_header = "智能农场视觉监测与数据管理平台控制台"
admin.site.site_title = "智能农场视觉监测与数据管理平台控制台"
admin.site.index_title = "业务模型配置中心"


@admin.action(description='一键导出选中的结构化数据 (CSV)')
def export_as_csv(modeladmin, request, queryset):
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("name", "location")
    search_fields = ("name", "location")
    list_filter = ("location",)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "device_type", "farm", "status", "last_online_time")
    list_filter = ("device_type", "status", "farm")
    search_fields = ("name", "location", "farm__name")
    list_select_related = ("farm",)
    actions = [export_as_csv]

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    """边缘视觉采集记录的查询与追溯。"""
    list_display = ("device", "capture_time", "description")
    list_filter = ("device__farm", "device__device_type")
    search_fields = ("device__name", "description")
    date_hierarchy = "capture_time"
    list_select_related = ("device", "device__farm")

    actions = [export_as_csv]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = '视觉采集数据管理与核实' # 将“修改”替换为“核实”
        return super().changelist_view(request, extra_context=extra_context)


    def has_add_permission(self, request):
        return False

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("title", "farm", "device", "severity", "confidence", "created_at", "is_resolved")
    list_filter = ("severity", "is_resolved", "farm", "device")
    search_fields = ("title", "message", "farm__name", "device__name")
    date_hierarchy = "created_at"
    list_select_related = ("farm", "device")
    readonly_fields = ("created_at", "confidence")

    actions = [export_as_csv]

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = '智能警告记录详情与处置'
        return super().changelist_view(request, extra_context=extra_context)
