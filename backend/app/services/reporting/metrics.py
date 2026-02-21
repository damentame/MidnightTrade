def overview_stats(trades, equity):
    trade_count = len(trades)
    wins = [t for t in trades if (t.pnl_usd or 0) > 0]
    losses = [t for t in trades if (t.pnl_usd or 0) < 0]
    total_pnl = float(sum(float(t.pnl_usd or 0) for t in trades))
    avg_r = float(sum(float(t.pnl_r or 0) for t in trades) / trade_count) if trade_count else 0.0
    expectancy = avg_r
    gross_profit = abs(sum(float(t.pnl_usd or 0) for t in wins))
    gross_loss = abs(sum(float(t.pnl_usd or 0) for t in losses))
    pf = (gross_profit / gross_loss) if gross_loss else (gross_profit if gross_profit else 0.0)
    max_dd = max([e.drawdown for e in equity], default=0.0)
    bos_count = sum(1 for t in trades if t.execution_meta_json.get("bos_occurred"))
    return {
        "total_pnl": total_pnl,
        "win_rate": (len(wins) / trade_count) if trade_count else 0.0,
        "trade_count": trade_count,
        "avg_r": avg_r,
        "expectancy": expectancy,
        "profit_factor": pf,
        "max_drawdown": max_dd,
        "equity_curve": [{"ts": e.ts.isoformat(), "equity": e.equity} for e in equity[-300:]],
        "bos_occurrence_rate": (bos_count / trade_count) if trade_count else 0.0,
    }
