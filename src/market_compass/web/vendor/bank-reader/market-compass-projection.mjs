/** Read-only projection of independently verified owner history, never a balance. */
export function marketCompassProjection(operation, scopes) {
  if (operation?.schema !== 'bank-reader.domain-operation/v1' || operation.readback !== true
      || !['trading-history', 'crypto-history'].includes(operation.kind)
      || !Array.isArray(operation.records) || !operation.records.length
      || !Array.isArray(operation.rows) || operation.rows.length !== operation.records.length)
    throw Error('Choose a verified financial-history operation.');
  const trading = operation.kind === 'trading-history';
  const groups = new Map();
  for (let index = 0; index < operation.records.length; index++) {
    const record = operation.records[index], source = operation.rows[index].values;
    const id = source[trading ? 'account_id' : 'wallet_id'];
    const scope = scopes.find(value => value.id === id);
    if (!scope || record.member_id !== operation.memberId || record[trading ? 'account_id' : 'wallet_id'] !== id)
      throw Error('The financial source scope needs owner review.');
    if (!groups.has(id)) groups.set(id, {id, name: scope.name || id,
      broker: trading ? scope.institution || null : scope.platform || null,
      kind: trading ? 'broker-account' : 'crypto-wallet', activities: []});
    // Exact decimal strings come from the confirmed source rows, not binary floats.
    groups.get(id).activities.push({id: record.id, ...source});
  }
  const dates = operation.rows.map(row => row.values.date).sort();
  return {schema: 'bank-reader.market-compass-projection/v1', readOnly: true, readback: true,
    operationId: operation.operationId, originalSha256: operation.sourceSha256,
    reviewedSheetSha256: operation.sheetDigest, memberId: operation.memberId,
    currency: operation.currency, sourceKind: operation.kind,
    period: {first: dates[0], last: dates.at(-1)}, accounts: [...groups.values()],
    holdings: null, combinedHoldings: null, openingPositionsKnown: false,
    completeness: 'historical-activity-only',
    warning: 'Imported activity is not a current balance. Opening positions, missing activity and later changes are unknown.',
    effects: {orders: false, transfers: false, positions: false, balances: false, paperTrades: false}};
}
