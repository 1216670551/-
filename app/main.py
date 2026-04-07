"""气象预警信息平台 MVP 示例。

说明：
1. 该文件仅提供最小可用框架，外部 API 需按你们实际接口实现。
2. 推荐将国家预警平台、腾讯文档、钉钉配置放到环境变量或配置中心。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass
class Project:
    project_id: str
    project_name: str
    geo_code: str
    owner: str
    notify_group: str
    severity_threshold: str = "yellow"


@dataclass
class Alert:
    alert_id: str
    title: str
    alert_type: str
    level: str
    geo_code: str
    status: str


LEVEL_RANK: Dict[str, int] = {"blue": 1, "yellow": 2, "orange": 3, "red": 4}


def fetch_projects() -> List[Project]:
    """从腾讯在线文档读取项目数据（示例桩函数）。"""
    return [
        Project(
            project_id="P001",
            project_name="深圳某工地",
            geo_code="440305",
            owner="张三",
            notify_group="ding_group_a",
            severity_threshold="yellow",
        )
    ]


def fetch_alerts() -> List[Alert]:
    """从国家预警平台读取预警数据（示例桩函数）。"""
    return [
        Alert(
            alert_id="A10001",
            title="深圳市南山区暴雨黄色预警",
            alert_type="暴雨",
            level="yellow",
            geo_code="440305",
            status="active",
        )
    ]


def should_notify(alert: Alert, project: Project) -> bool:
    if alert.status != "active":
        return False
    return LEVEL_RANK.get(alert.level, 0) >= LEVEL_RANK.get(project.severity_threshold, 0)


def match_projects_alerts(projects: Iterable[Project], alerts: Iterable[Alert]) -> List[tuple[Project, Alert]]:
    alerts_by_geo: Dict[str, List[Alert]] = {}
    for alert in alerts:
        alerts_by_geo.setdefault(alert.geo_code, []).append(alert)

    matched: List[tuple[Project, Alert]] = []
    for project in projects:
        for alert in alerts_by_geo.get(project.geo_code, []):
            if should_notify(alert, project):
                matched.append((project, alert))
    return matched


def notify_dingtalk(project: Project, alert: Alert) -> None:
    """调用钉钉机器人发送消息（示例：先打印，实际请替换为 HTTP POST）。"""
    content = (
        f"[气象预警] 项目:{project.project_name} 负责人:{project.owner} "
        f"区域:{project.geo_code} 类型:{alert.alert_type} 等级:{alert.level} 标题:{alert.title}"
    )
    print(content)


def run_once() -> None:
    projects = fetch_projects()
    alerts = fetch_alerts()
    for project, alert in match_projects_alerts(projects, alerts):
        notify_dingtalk(project, alert)


if __name__ == "__main__":
    run_once()
