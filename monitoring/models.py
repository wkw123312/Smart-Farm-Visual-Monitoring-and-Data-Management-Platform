from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Farm(models.Model):
    """农场实体，代表一个物理农业生产单元。

    在农业物联网场景下，一个农场通常对应一个独立的
    采集与控制边缘节点，用于汇聚温湿度、图像、土壤
    传感器等多源数据。"""

    name = models.CharField(
        max_length=100,
        verbose_name="农场名称",
        help_text="农场或示范园区的名称，用于在平台中唯一标识生产单元。",
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="地理位置",
        help_text="农场所在的省市区、地块或温室编号等位置信息。",
    )
    description = models.TextField(
        blank=True,
        verbose_name="备注信息",
        help_text="对农场的作物类型、种植模式等进行补充说明。",
    )

    class Meta:
        verbose_name = "农场配置"
        verbose_name_plural = "农场配置"

    def __str__(self) -> str:
        return self.name


class Device(models.Model):
    """边缘侧接入的物联网设备。

    包含固定摄像头、环境传感器等类型，是视觉采集与
    实时监测数据的来源。"""

    CAMERA = "camera"
    SENSOR = "sensor"
    DEVICE_TYPES = [
        (CAMERA, "固定摄像头"),
        (SENSOR, "环境传感器"),
    ]

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="devices",
        verbose_name="所属农场",
        help_text="设备安装所在的农场或温室。",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="设备名称",
        help_text="边缘侧摄像头或传感器的业务名称。",
    )
    device_type = models.CharField(
        max_length=20,
        choices=DEVICE_TYPES,
        verbose_name="设备类型",
        help_text="区分固定摄像头、环境传感器等不同类型。",
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="安装位置",
        help_text="设备在农场中的具体安装位置信息。",
    )
    status = models.CharField(
        max_length=20,
        default="在线",
        verbose_name="运行状态",
        help_text="设备当前的连通状态，如在线、离线、维护中等。",
    )
    extra_info = models.TextField(
        null=True,
        blank=True,
        verbose_name="设备备注/扩展信息",
        help_text="用于记录设备的特殊功能描述，如变焦倍率、轨道参数等"
    )
    last_online_time = models.DateTimeField(
        verbose_name="最近在线时间",
        help_text="设备最近一次成功与平台通讯的时间，用于判断在线状态。",
    )

    class Meta:
        verbose_name = "物联网设备"
        verbose_name_plural = "物联网设备"

    def __str__(self) -> str:
        return self.name


class Observation(models.Model):
    """单次视觉采集记录。

    记录某个边缘摄像头在特定时间采集到的原始图像信息，
    为后续的视觉识别与历史追溯提供基础数据。"""

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="observations",
        verbose_name="采集设备",
        help_text="产生该次图像采集的摄像头设备。",
    )
    capture_time = models.DateTimeField(
        verbose_name="采集时间",
        help_text="图像在边缘侧实际采集的时间，用于时序分析。",
    )
    image_path = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="图像路径",
        help_text="存储于静态目录或对象存储中的图像访问路径。",
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="业务描述",
        help_text="对该次采集场景的补充说明，例如作物品种、拍摄角度等。",
    )

    class Meta:
        verbose_name = "视觉采集记录"
        verbose_name_plural = "视觉采集记录"

    def __str__(self) -> str:
        return f"{self.device.name} @ {self.capture_time:%Y-%m-%d %H:%M}"


class Alert(models.Model):
    """由设备采集规则或图像识别结果触发的警告信息。

    该模型聚合了现场监测结果与业务侧处理状态，是
    农业物联网警告闭环中的核心实体。"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    SEVERITIES = [
        (LOW, "低"),
        (MEDIUM, "中"),
        (HIGH, "高"),
    ]

    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name="alerts",
        verbose_name="所属农场",
        help_text="产生该警告的农场或温室。",
    )
    device = models.ForeignKey(
        Device,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="alerts",
        verbose_name="关联设备",
        help_text="触发该警告的具体设备，部分规则可能只关联农场不关联设备。",
    )
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="触发用户",
        help_text="发起该警告的操作账号，算法自动触发时可为空。",
    )
    title = models.CharField(
        max_length=100,
        verbose_name="警告标题",
        help_text="用于在列表中快速识别问题类型的简短标题。",
    )
    message = models.TextField(
        blank=True,
        verbose_name="警告详情",
        help_text="对警告产生原因、建议处置措施等进行详细说明。",
    )
    severity = models.CharField(
        max_length=10,
        choices=SEVERITIES,
        verbose_name="警告级别",
        help_text="区分低、中、高不同严重程度，便于分级响应。",
    )
    created_at = models.DateTimeField(
        verbose_name="产生时间",
        help_text="警告在平台侧被记录的时间。",
    )
    is_resolved = models.BooleanField(
        default=False,
        verbose_name="是否已处置",
        help_text="指示该警告是否已经由值班人员完成闭环处理。",
    )
    confidence = models.FloatField(
        null=True,
        blank=True,
        verbose_name="识别可靠性评分",
        help_text="对本次警告依据的识别或判断结果进行 0~1 量化评分。",
    )

    class Meta:
        verbose_name = "智能警告记录"
        verbose_name_plural = "智能警告记录"

    def __str__(self) -> str:
        return self.title
