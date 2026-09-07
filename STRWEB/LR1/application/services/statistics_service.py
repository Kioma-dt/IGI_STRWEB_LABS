from __future__ import annotations

import logging

from application.dto.statistics import ShopStatisticsDTO
from application.repositories.statistics_repository import StatisticsRepository

logger = logging.getLogger(__name__)


class StatisticsService:
    """Aggregated shop metrics for reporting (no HTTP)."""

    def __init__(
        self,
        *,
        statistics: StatisticsRepository | None = None,
    ) -> None:
        self._statistics = statistics or StatisticsRepository()

    def get_shop_statistics(self) -> ShopStatisticsDTO:
        dto = self._statistics.fetch_shop_statistics()
        logger.debug("Statistics snapshot generated.")
        return dto
