from statistics import mean

def evaluate(events):
    if not events:return {'count':0,'avg_latency_ms':0,'total_tokens':0,'estimated_cost_usd':0,'error_rate':0,'avg_quality':0}
    return {'count':len(events),'avg_latency_ms':round(mean(e['latency_ms'] for e in events),1),'total_tokens':sum(e['tokens'] for e in events),'estimated_cost_usd':round(sum(e['tokens']*e['usd_per_1k_tokens']/1000 for e in events),6),'error_rate':round(sum(e['error'] for e in events)/len(events),3),'avg_quality':round(mean(e['quality'] for e in events),3)}
