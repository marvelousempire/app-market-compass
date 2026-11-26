/* Presentation only. Source receipts retain their exact machine values for export. */
window.MarketCompassHuman = Object.freeze({
  label(key) {
    const names = {rss:'News', edgar:'SEC filings', sha256:'Source fingerprint', as_of:'As of', source_owner:'Source owner', receipt_sha256:'Receipt fingerprint'};
    return names[key] || String(key).replaceAll('_',' ').replace(/\b\w/g, letter => letter.toUpperCase());
  },
  date(value) {
    if (!value) return 'Date unavailable';
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? 'Date unavailable' : new Intl.DateTimeFormat(undefined,{dateStyle:'medium',timeStyle:'short'}).format(date);
  },
  value(input) {
    if (input == null || input === '') return 'Not available';
    if (typeof input === 'boolean') return input ? 'Yes' : 'No';
    if (Array.isArray(input)) return input.length ? input.map(item => this.value(item)).join('; ') : 'None';
    if (typeof input === 'object') return Object.entries(input).map(([key,value]) => `${this.label(key)}: ${this.value(value)}`).join('\n');
    return String(input).replaceAll('_',' ');
  },
  state(value) {
    return ({observed:'Observed',missing:'Unavailable',held:'On hold',stale:'Out of date',ready:'Ready',unknown:'Unknown',pass:'Passed',fail:'Needs attention'})[value] || this.label(value || 'unknown');
  }
});
