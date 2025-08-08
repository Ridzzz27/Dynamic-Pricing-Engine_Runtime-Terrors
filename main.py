from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from typing import Optional
import random
from contextlib import contextmanager
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Dynamic Pricing Engine", version="2.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
engine = create_engine("sqlite:///pricing.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PricingRequest(BaseModel):
    product_id: str
    cost_price: float
    demand_score: int
    inventory: int
    competitor_price: float
    customer_segment: Optional[str] = "standard"
    seasonality_factor: Optional[float] = 1.0

class PricingHistory(Base):
    __tablename__ = "pricing_history"
    id = Column(Integer, primary_key=True)
    product_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    original_price = Column(Float)
    dynamic_price = Column(Float)
    demand_score = Column(Integer)
    inventory = Column(Integer)
    competitor_price = Column(Float)
    strategy_used = Column(String)
    conversion_rate = Column(Float, default=0.0)
    revenue_generated = Column(Float, default=0.0)

class CompetitorPrice(Base):
    __tablename__ = "competitor_prices"
    id = Column(Integer, primary_key=True)
    product_id = Column(String, index=True)
    competitor_name = Column(String)
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)

class DynamicPricingEngine:
    def __init__(self):
        self.price_adjustment_strategies = {
            "default": self._calculate_default_price,
            "aggressive": self._calculate_aggressive_price,
            "conservative": self._calculate_conservative_price
        }

    def _get_base_markup(self, ds: int) -> float:
        markups = {
            1: 0.15, 2: 0.18, 3: 0.20, 4: 0.25, 5: 0.30,
            6: 0.35, 7: 0.42, 8: 0.50, 9: 0.60, 10: 0.75
        }
        return markups.get(ds, 0.30)

    def _factor(self, value, thresholds, factors):
        for th, f in zip(thresholds, factors):
            if value <= th:
                return f
        return factors[-1]

    async def calculate(self, req: PricingRequest, strategy: str = "default"):
        calculation_method = self.price_adjustment_strategies.get(strategy, self._calculate_default_price)
        price_data = calculation_method(req)
        
        with get_db() as db:
            db.add(PricingHistory(
                product_id=req.product_id,
                original_price=price_data["base_price"],
                dynamic_price=price_data["dynamic_price"],
                demand_score=req.demand_score,
                inventory=req.inventory,
                competitor_price=req.competitor_price,
                strategy_used=strategy
            ))
            db.commit()
        
        return price_data

    def _calculate_default_price(self, req: PricingRequest):
        base = req.cost_price * (1 + self._get_base_markup(req.demand_score))
        demand_factor = self._factor(req.demand_score, [3,7], [0.85,1.0,1.25])
        inv_factor = self._factor(req.inventory, [10,100], [1.15,1.0,0.90])
        comp_ratio = base / req.competitor_price
        comp_factor = 0.95 if comp_ratio > 1.1 else 1.05 if comp_ratio < 0.9 else 1.0
        seg_factor = {
            "premium": 1.2, "standard": 1.0,
            "budget": 0.85, "loyalty": 0.90
        }.get(req.customer_segment, 1.0)
        
        price = base * demand_factor * inv_factor * comp_factor * req.seasonality_factor * seg_factor
        price = max(req.cost_price*1.1, min(price, req.competitor_price*1.2))
        
        return {
            "product_id": req.product_id,
            "dynamic_price": round(price, 2),
            "base_price": round(base, 2),
            "strategy": "default"
        }

    def _calculate_aggressive_price(self, req: PricingRequest):
        base = req.cost_price * (1 + self._get_base_markup(req.demand_score) + 0.1)
        demand_factor = self._factor(req.demand_score, [3,7], [0.9,1.1,1.4])
        price = base * demand_factor
        price = max(req.cost_price*1.05, min(price, req.competitor_price*1.1))
        
        return {
            "product_id": req.product_id,
            "dynamic_price": round(price, 2),
            "base_price": round(base, 2),
            "strategy": "aggressive"
        }

    def _calculate_conservative_price(self, req: PricingRequest):
        base = req.cost_price * (1 + self._get_base_markup(req.demand_score) - 0.05)
        demand_factor = self._factor(req.demand_score, [3,7], [0.8,0.95,1.15])
        price = base * demand_factor
        price = max(req.cost_price*1.15, min(price, req.competitor_price*0.95))
        
        return {
            "product_id": req.product_id,
            "dynamic_price": round(price, 2),
            "base_price": round(base, 2),
            "strategy": "conservative"
        }

pricing_engine = DynamicPricingEngine()

@app.post("/calculate-price")
async def calculate_price(request: PricingRequest):
    return await pricing_engine.calculate(request)

@app.get("/analytics/pricing-performance")
async def analytics(product_id: Optional[str] = None, days: int = 7):
    with get_db() as db:
        query = db.query(
            func.avg(PricingHistory.dynamic_price).label("average_price"),
            func.count(PricingHistory.id).label("price_changes"),
            func.avg(PricingHistory.conversion_rate).label("conversion_rate"),
            func.sum(PricingHistory.revenue_generated).label("revenue_impact")
        )
        
        if product_id:
            query = query.filter(PricingHistory.product_id == product_id)
        
        metrics = query.filter(
            PricingHistory.timestamp >= datetime.utcnow() - timedelta(days=days)
        ).first()
        
        comp_avg = db.query(
            func.avg(CompetitorPrice.price).label("competitor_avg")
        ).filter(
            CompetitorPrice.timestamp >= datetime.utcnow() - timedelta(days=days)
        ).first()
        
        trend_query = db.query(
            func.date(PricingHistory.timestamp).label("date"),
            func.avg(PricingHistory.dynamic_price).label("price"),
            func.count(PricingHistory.id).label("sales")
        ).group_by("date").order_by("date")
        
        if product_id:
            trend_query = trend_query.filter(PricingHistory.product_id == product_id)
            
        price_trend = trend_query.filter(
            PricingHistory.timestamp >= datetime.utcnow() - timedelta(days=days)
        ).all()
    
    return {
        "metrics": {
            "average_price": float(metrics.average_price) if metrics.average_price else 0,
            "price_changes": metrics.price_changes or 0,
            "conversion_rate": metrics.conversion_rate or 0,
            "revenue_impact": metrics.revenue_impact or 0,
            "competitor_price_avg": float(comp_avg.competitor_avg) if comp_avg.competitor_avg else 0
        },
        "price_trend": [
            {"date": str(t.date), "price": float(t.price), "sales": t.sales}
            for t in price_trend
        ]
    }

@app.post("/competitor-prices/update")
async def update_competitors(tasks: BackgroundTasks):
    async def monitor_competitors():
        competitors = ["Amazon", "Walmart", "Target", "BestBuy", "eBay"]
        with get_db() as db:
            for competitor in competitors:
                mock_price = round(random.uniform(40, 60), 2)
                db.add(CompetitorPrice(
                    product_id="PROD-001",
                    competitor_name=competitor,
                    price=mock_price
                ))
            db.commit()
    
    tasks.add_task(monitor_competitors)
    return {"message": "Competitor price monitoring initiated"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "2.1",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if engine.connect() else "disconnected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)