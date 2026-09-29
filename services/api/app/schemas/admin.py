from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class KPICards(BaseModel):
    beneficiaries_profiled: int
    recommendation_acceptance_rate: float
    training_enrolment_count: int
    placement_outcome_rate: float

class SectorBreakdown(BaseModel):
    sector: str
    count: int
    percentage: float

class AdminMetricsResponse(BaseModel):
    kpis: KPICards
    profiled_over_time: List[Dict[str, Any]]
    top_sectors_by_block: List[Dict[str, Any]]
    recommendation_categories: List[Dict[str, Any]]
    training_provider_pipeline: List[Dict[str, Any]]

class AdminReportsResponse(BaseModel):
    report_type: str
    generated_at: str
    record_count: int
    data: List[Dict[str, Any]]
