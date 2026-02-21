async function load() {
  const settings = await (await fetch('/api/settings')).json();
  document.getElementById('risk').value = settings.risk_pct;
  document.getElementById('enabled').checked = settings.trading_enabled;
  document.getElementById('overview').textContent = JSON.stringify(await (await fetch('/api/stats/overview')).json(), null, 2);
  document.getElementById('trades').textContent = JSON.stringify(await (await fetch('/api/trades')).json(), null, 2);
}
document.getElementById('save').onclick = async () => {
  await fetch('/api/settings', {method: 'PUT', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({risk_pct: parseFloat(document.getElementById('risk').value), trading_enabled: document.getElementById('enabled').checked})});
  await load();
};
load();
