from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from monitoring.models import Alert, Device, Farm, Observation


class Command(BaseCommand):
    help = "初始化智能农场视觉监测与数据管理平台的基础业务数据。"

    def handle(self, *args, **options):
        """创建用户、农场、设备、采集记录与警告，形成完整业务闭环。"""

        User = get_user_model()

        # 所有时间统一控制在 2026 年内，便于追溯。
        base_date = datetime(2026, 3, 1, 9, 0, 0)

        # 管理员账号
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={"is_staff": True, "is_superuser": True},
        )
        if created:
            admin.set_password("admin")
            admin.save()
            self.stdout.write(self.style.SUCCESS("已创建管理员账号 admin / admin"))
        else:
            self.stdout.write("管理员账号已存在，跳过创建")

        # 普通用户
        normal_usernames = ["张依依", "王星", "刘宇", "赵航"]
        for idx, name in enumerate(normal_usernames, start=1):
            user, created = User.objects.get_or_create(
                username=name,
                defaults={"is_staff": False, "is_superuser": False},
            )
            if created:
                user.set_password("12345678")
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f"已创建普通用户 {name} / 123 (序号 {idx})")
                )
            else:
                self.stdout.write(f"普通用户 {name} 已存在，跳过创建")

        # 农场
        farm_main, _ = Farm.objects.get_or_create(
            name="智慧温室园区",
            defaults={
                "location": "某省某市智能农业示范基地 A 区",
                "description": "以温室番茄、黄瓜为主的设施农业种植区域。",
            },
        )

        farm_sub, _ = Farm.objects.get_or_create(
            name="露天果园",
            defaults={
                "location": "某省某市智能农业示范基地 B 区",
                "description": "以苹果、梨树为主的露天果园地块。",
            },
        )

        # 设备
        cam_greenhouse, _ = Device.objects.get_or_create(
            farm=farm_main,
            name="温室一号通道摄像头",
            defaults={
                "device_type": Device.CAMERA,
                "location": "玻璃温室 1 号通道南端",
                "status": "在线",
                "last_online_time": base_date,
            },
        )

        cam_field, _ = Device.objects.get_or_create(
            farm=farm_sub,
            name="果园北侧监控摄像头",
            defaults={
                "device_type": Device.CAMERA,
                "location": "果园北侧主干道",
                "status": "在线",
                "last_online_time": base_date,
            },
        )

        cam_smart, _ = Device.objects.get_or_create(
            farm=farm_main,
            name="多维智能云台",
            defaults={
                "device_type": "INTELLIGENT_PTZ",
                "location": "农场核心监测点",
                "status": "在线",
                "extra_info": "支持室外长焦预置位与室内轨道平移双模式切换",
                "last_online_time": base_date,
            },
        )

        sensor_env, _ = Device.objects.get_or_create(
            farm=farm_main,
            name="温室环境传感器",
            defaults={
                "device_type": Device.SENSOR,
                "location": "玻璃温室中央区域",
                "status": "在线",
                "last_online_time": base_date,
            },
        )

        Observation.objects.get_or_create(
            device=cam_field,
            capture_time=base_date.replace(hour=9, minute=20),
            defaults={
                "image_path": "/static/img/果园.jpg",
                "description": "果园北侧树行监控画面，可用于远程查看树冠长势。",
            },
        )

        Observation.objects.get_or_create(
            device=cam_greenhouse,
            capture_time=base_date.replace(hour=9, minute=25),
            defaults={
                "image_path": "/static/img/苹果近景.jpg",
                "description": "苹果树冠层近景画面，主要用于实时监测绿果期病虫害趋势及叶片水分状态。",
            },
        )

        Observation.objects.get_or_create(
            device=cam_greenhouse,
            capture_time=base_date.replace(hour=10, minute=12),
            defaults={
                "image_path": "/static/img/温室.jpg",
                "description": "温室通道整体视角，用于巡检通行区域与棚内光照。",
            },
        )

        Observation.objects.get_or_create(
            device=cam_greenhouse,
            capture_time=base_date.replace(hour=10, minute=17),
            defaults={
                "image_path": "/static/img/番茄近景.jpg",
                "description": "单株番茄植株近景画面，便于识别叶片病斑与缺素情况。",
            },
        )


        # 警告示例（包含识别可靠性评分等信息）
        first_user = User.objects.filter(is_superuser=False).first()

        Alert.objects.get_or_create(
            farm=farm_main,
            device=sensor_env,
            created_by=first_user,
            title="温室空气湿度偏高预警",
            defaults={
                "message": "环境采集模块检测到温室平均相对湿度持续高于90%，"
                "可能诱发灰霉病和霜霉病风险，建议及时开启通风与除湿设备。",
                "severity": Alert.MEDIUM,
                "created_at": base_date.replace(hour=9, minute=40),
                "is_resolved": False,
                "confidence": 0.88,
            },
        )

        Alert.objects.get_or_create(
            farm=farm_sub,
            device=cam_field,
            created_by=first_user,
            title="果园东侧疑似病斑预警",
            defaults={
                "message": "图像识别结果显示果园东侧存在疑似叶片病斑区域，"
                "本次识别可靠性评分为 0.95，请现场巡查确认并采集样本。",
                "severity": Alert.HIGH,
                "created_at": base_date.replace(hour=9, minute=50),
                "is_resolved": False,
                "confidence": 0.95,
            },
        )

        Alert.objects.get_or_create(
            farm=farm_main,
            device=cam_greenhouse,
            created_by=first_user,
            title="温室一号通道摄像头网络波动",
            defaults={
                "message": "边缘网关在 2 分钟内多次检测到视频码流中断，"
                "平台自动触发网络自愈流程，目前链路已恢复稳定。",
                "severity": Alert.LOW,
                "created_at": base_date.replace(hour=10, minute=0),
                "is_resolved": True,
                "confidence": 0.7,
            },
        )

        self.stdout.write(self.style.SUCCESS("基础业务数据初始化完成。"))
