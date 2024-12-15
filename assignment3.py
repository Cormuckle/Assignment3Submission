import matplotlib
import polars as pl
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

df = pl.read_csv("./shopping_trends.csv")

fig = make_subplots(
    rows=2,
    cols=6,
    specs=[
        [
            {"colspan": 2, "type": "domain"},
            None,
            {"colspan": 2},
            None,
            {"colspan": 2},
            None,
        ],
        [{"colspan": 3}, None, None, {"colspan": 3}, None, None],
    ],
    subplot_titles=(
        "Proportion of purchases",
        "Purchases and coupon usage by season",
        "Number of purchases by age range",
        "Payment usage",
        "Product ranking and cost by product type",
    ),
)
sunburst = px.sunburst(
    df, path=["Category", "Item Purchased"], values="Purchase Amount (USD)"
)

fig.add_sunburst(
    labels=sunburst["data"][0]["labels"].tolist(),
    parents=sunburst["data"][0]["parents"].tolist(),
    values=sunburst["data"][0]["values"].tolist(),
    col=1,
    row=1,
)
fig.data[-1].name = "Total"

q = df["Season"].value_counts()
q = q.with_columns(
    pl.col("Season").replace_strict(
        ["Spring", "Summer", "Fall", "Winter"], [1, 2, 3, 4]
    )
).sort(pl.col("Season"))

fig.add_trace(
    go.Bar(x=["Spring", "Summer", "Fall", "Winter"], y=q["count"]),
    col=3,
    row=1,
)
fig.data[-1].name = "Purchases"

p = df.filter(pl.col("Discount Applied") == "Yes")

q = p["Season"].value_counts()
q = q.with_columns(
    pl.col("Season").replace_strict(
        ["Spring", "Summer", "Fall", "Winter"], [1, 2, 3, 4]
    )
).sort(pl.col("Season"))

fig.add_trace(
    go.Scatter(x=["Spring", "Summer", "Fall", "Winter"], y=q["count"]),
    col=3,
    row=1,
)
fig.data[-1].name = "Coupons Used"

p = df.filter(pl.col("Age") < 28)
q = p["Season"].value_counts()
q = q.with_columns(
    pl.col("Season").replace_strict(
        ["Spring", "Summer", "Fall", "Winter"], [1, 2, 3, 4]
    )
).sort(pl.col("Season"))

fig.add_trace(
    go.Scatter(x=["Spring", "Summer", "Fall", "Winter"], y=q["count"]),
    col=5,
    row=1,
)
fig.data[-1].name = "Purchases (<28)"

p = df.filter(pl.col("Age").is_between(27, 39))
q = p["Season"].value_counts()
q = q.with_columns(
    pl.col("Season").replace_strict(
        ["Spring", "Summer", "Fall", "Winter"], [1, 2, 3, 4]
    )
).sort(pl.col("Season"))

fig.add_trace(
    go.Scatter(x=["Spring", "Summer", "Fall", "Winter"], y=q["count"]),
    col=5,
    row=1,
)
fig.data[-1].name = "Purchases (24-36)"

p = df.filter(pl.col("Age").is_between(38, 50))
q = p["Season"].value_counts()
q = q.with_columns(
    pl.col("Season").replace_strict(
        ["Spring", "Summer", "Fall", "Winter"], [1, 2, 3, 4]
    )
).sort(pl.col("Season"))

fig.add_trace(
    go.Scatter(x=["Spring", "Summer", "Fall", "Winter"], y=q["count"]),
    col=5,
    row=1,
)
fig.data[-1].name = "Purchases (37-50)"

p = df.filter(49 < pl.col("Age"))
q = p["Season"].value_counts()
q = q.with_columns(
    pl.col("Season").replace_strict(
        ["Spring", "Summer", "Fall", "Winter"], [1, 2, 3, 4]
    )
).sort(pl.col("Season"))

fig.add_trace(
    go.Scatter(x=["Spring", "Summer", "Fall", "Winter"], y=q["count"]),
    col=5,
    row=1,
)
fig.data[-1].name = "Purchases (50+)"


q = df["Payment Method"].value_counts()
fig.add_trace(
    go.Bar(x=q["Payment Method"], y=q["count"]),
    col=1,
    row=2,
)
fig.data[-1].name = "Payment Method"

q = df["Season"].value_counts()
q = q.with_columns(
    pl.col("Season").replace_strict(
        ["Spring", "Summer", "Fall", "Winter"], [1, 2, 3, 4]
    )
).sort(pl.col("Season"))

for x in ["Outerwear", "Accessories", "Footwear", "Clothing"]:
    fig.add_trace(
        go.Scatter(
            x=df.filter(pl.col("Category") == x)["Purchase Amount (USD)"],
            y=df.filter(pl.col("Category") == x)["Review Rating"],
            mode="markers",
        ),
        col=4,
        row=2,
    )
    fig.data[-1].name = x

fig.update_yaxes(
    title_text="Amount purchased / Coupons used", range=[300, 1000], row=1, col=3
)
fig.update_yaxes(title_text="Number of Purchases", row=1, col=5)
fig.update_yaxes(title_text="Total times used", range=[600, 700], row=2, col=1)
fig.update_yaxes(title_text="Rating", row=2, col=4)


fig.update_xaxes(title_text="Season", row=1, col=3)
fig.update_xaxes(title_text="Season", row=1, col=5)
fig.update_xaxes(title_text="Payment Type", row=2, col=1)
fig.update_xaxes(title_text="Price", row=2, col=4)

fig.update_layout(title_text="Analyzing Customer Purchasing Trends")

fig.show()
fig.write_image("./fig.svg", width=2100, height=1200)
