class PricingDashboard {
  constructor() {
    this.api = "http://localhost:8000";
    this.chart = null; // Chart instance holder
    this.init();
  }

  init() {
    this.setupListeners();
    this.initChart();
    this.loadAnalytics();
    setInterval(() => this.loadAnalytics(), 30000);
  }

  setupListeners() {
    document.getElementById("pricing-form")
      .addEventListener("submit", e => this.calculate(e));
    
    const ds = document.getElementById("demand_score");
    const dv = document.getElementById("demand_value");
    ds.addEventListener("input", e => {
      dv.textContent = e.target.value;
    });
  }

  async calculate(e) {
    e.preventDefault();
    const btn = e.target.querySelector("button");
    btn.disabled = true;
    
    try {
      const data = this.getFormData();
      const res = await fetch(`${this.api}/calculate-price`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
      });
      
      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || "Request failed");
      }
      
      const json = await res.json();
      this.showResult(json);
      this.loadAnalytics(); // Refresh analytics after new calculation
    } catch (err) {
      this.showError(err.message);
    } finally {
      btn.disabled = false;
    }
  }

  getFormData() {
    return {
      product_id: document.getElementById("product_id").value,
      cost_price: parseFloat(document.getElementById("cost_price").value),
      demand_score: parseInt(document.getElementById("demand_score").value),
      inventory: parseInt(document.getElementById("inventory").value),
      competitor_price: parseFloat(document.getElementById("competitor_price").value),
      customer_segment: document.getElementById("customer_segment").value,
      seasonality_factor: parseFloat(document.getElementById("seasonality_factor").value)
    };
  }

  showResult(r) {
    const div = document.getElementById("result");
    div.innerHTML = `
      <h3>🎯 Optimal Price: ₹${r.dynamic_price}</h3>
      <p>Base Price: ₹${r.base_price}</p>
      <p>Strategy: ${r.strategy}</p>`;
  }

  async loadAnalytics() {
    try {
      const res = await fetch(`${this.api}/analytics/pricing-performance`);
      if (!res.ok) throw new Error("Failed to fetch analytics");
      
      const j = await res.json();
      document.getElementById("revenue-impact").textContent = `₹${j.metrics.revenue_impact}`;
      document.getElementById("conversion-rate").textContent = `${(j.metrics.conversion_rate * 100).toFixed(1)}%`;
      document.getElementById("price-change").textContent = j.metrics.price_changes;
      document.getElementById("competitor-gap").textContent = `₹${(j.metrics.competitor_price_avg - j.metrics.average_price).toFixed(2)}`;
      
      // Update chart with both your price and competitor price
      this.updateChart(j.price_trend, j.metrics.competitor_price_avg);
    } catch (err) {
      console.error("Analytics load error:", err);
    }
  }

  initChart() {
    const ctx = document.getElementById("priceChart").getContext("2d");
    this.chart = new Chart(ctx, {
      type: "line",
      data: {
        labels: [],
        datasets: [
          {
            label: "Your Price",
            data: [],
            borderColor: "#667eea",
            backgroundColor: "rgba(102, 126, 234, 0.1)",
            borderWidth: 2,
            fill: true,
            tension: 0.4
          },
          {
            label: "Competitor Avg",
            data: [],
            borderColor: "#e53e3e",
            borderWidth: 2,
            borderDash: [5, 5],
            fill: false,
            tension: 0.1
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          tooltip: {
            mode: "index",
            intersect: false
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            title: {
              display: true,
              text: "Price (₹)"
            }
          }
        },
        interaction: {
          mode: "nearest",
          axis: "x",
          intersect: false
        }
      }
    });
  }

  updateChart(priceTrend, competitorAvg) {
    if (!this.chart) return;
    
    // Extract dates and prices
    const dates = priceTrend.map(t => t.date);
    const prices = priceTrend.map(t => t.price);
    const competitorPrices = Array(prices.length).fill(competitorAvg);
    
    // Update chart data
    this.chart.data.labels = dates;
    this.chart.data.datasets[0].data = prices;
    this.chart.data.datasets[1].data = competitorPrices;
    
    // Add sales data as tooltip
    this.chart.options.plugins.tooltip.callbacks = {
      afterBody: (context) => {
        const index = context[0].dataIndex;
        return `Sales: ${priceTrend[index].sales}`;
      }
    };
    
    this.chart.update();
  }

  showError(msg) {
    document.getElementById("result").innerHTML = `<p style="color:#e53e3e">${msg}</p>`;
  }
}

window.addEventListener("DOMContentLoaded", () => new PricingDashboard());