from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class VarianceRequest(BaseModel):
    company_code: str = Field(min_length=1, max_length=20)
    current_month: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    prior_month: str = Field(pattern=r"^\d{4}-(0[1-9]|1[0-2])$")
    currency: str = Field(default="INR", min_length=3, max_length=3)
    metric: Literal["gross_margin", "revenue_amount", "production_yield_pct"] = "gross_margin"
    question: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def periods_must_differ(self):
        if self.current_month == self.prior_month:
            raise ValueError("current_month and prior_month must differ")
        return self
