/* Read-only Hybrid CCK profile schedule chooser. Templates are not issued CCK certificates. */
document.addEventListener('DOMContentLoaded', () => {
  const selector = document.getElementById('hcck-profile-select');
  const detail = document.getElementById('hcck-profile-detail');
  const load = document.getElementById('hcck-load-example');
  const target = document.getElementById('universal-input');
  const seatWrapper = document.getElementById('hcck-seat-wrapper');
  const seatSelector = document.getElementById('hcck-seat-select');
  if (!selector || !detail || !load || !target) return;

  let profiles = [];
  let seats = [];
  function node(tag, value, className) {
    const item = document.createElement(tag);
    item.textContent = String(value ?? '');
    if (className) item.className = className;
    return item;
  }
  function current() {
    return profiles.find(profile => profile.id === selector.value);
  }
  function render() {
    const profile = current();
    detail.replaceChildren();
    load.disabled = !profile;
    if (!profile) return;
    if (seatWrapper) seatWrapper.hidden = profile.id !== 'participant-v1';
    detail.appendChild(node('h3', profile.title));
    detail.appendChild(node('p', 'Domain: ' + profile.domain +
      ' · Subject: ' + (profile.subject_kind || 'any') +
      ' · Source: ' + profile.source_owner));
    detail.appendChild(node('p', 'Required source fields: ' + profile.fields.join(', ')));
    detail.appendChild(node('p', 'Schedule: ' + profile.schedule.cadence +
      ' · ' + profile.schedule.clock + ' clock · ' + profile.schedule.timezone +
      ' · evidence reference: ' + (profile.schedule.evidence_required ? 'required' : 'optional')));
    detail.appendChild(node('p', 'Example metric ideas: ' + profile.example_metrics.join(', ')));
    detail.appendChild(node('p', profile.notes, 'trust-note'));
    if (profile.id === 'participant-v1') {
      const seat = seats.find(item => item.id === seatSelector?.value);
      if (seat) detail.appendChild(node('p',
        'Named section: ' + seat.name + ' · ' +
        (seat.card?.title || 'no King card assigned') +
        ' · no participant evidence imported'));
    }
    detail.appendChild(node('small',
      'Draft profile template. CCK certification, owner authority, and automatic scheduling are not active.'));
  }
  function example(profile) {
    const source_fields = {};
    for (const field of profile.fields) source_fields[field] = 'fixture-' + field;
    if (profile.id === 'athlete-performance-v1') Object.assign(source_fields, {
      player_ref: 'fixture-player', sport: 'basketball', season: 'demo',
      source_scope: 'synthetic-only', consent_ref: 'fixture-not-verified'
    });
    if (profile.id === 'equity-v1') Object.assign(source_fields, {
      symbol: 'DEMO', exchange: 'fictional', quote_currency: 'USD', source_id: 'fixture'
    });
    if (profile.id === 'option-v1') Object.assign(source_fields, {
      underlying: 'DEMO', expiry: '2099-12-31', right: 'call',
      strike: '50', quote_currency: 'USD', source_id: 'fixture'
    });
    if (profile.id === 'device-v1') Object.assign(source_fields, {
      device_category: 'laptop', model: 'fictional computer', inventory_ref: 'fixture-001'
    });
    if (profile.id === 'batch-v1') Object.assign(source_fields, {
      batch_ref: 'fixture-eggs', category: 'eggs', quantity_unit: 'cartons'
    });
    if (profile.id === 'participant-v1') {
      const seat = seats.find(item => item.id === seatSelector?.value);
      Object.assign(source_fields, {
        participant_id: seat?.participant_id || 'fixture-participant',
        role_ref: 'observer', source_scope: 'synthetic-only'
      });
    }
    return {
      profile_id: profile.id,
      cck_profile_ref: 'draft:synthetic-only',
      source_fields,
      simulation: {
        subject: {
          id: 'synthetic-' + profile.id, name: 'Illustrative ' + profile.title,
          kind: profile.subject_kind || 'other', source_owner: 'fixture-only',
          authorized_use: true
        },
        method: {
          id: 'fixture-condition', version: 'demo-1',
          author: 'illustrative author',
          provenance: 'synthetic fixture only; not an ELSE-issued method',
          metrics: [
            {id: 'quality', label: 'Illustrative quality', unit: 'points',
             lower: 0, upper: 100, weight: 3, favorable: 'higher'},
            {id: 'wear', label: 'Illustrative wear', unit: 'points',
             lower: 0, upper: 10, weight: 1, favorable: 'lower'}
          ]
        },
        observations: [
          {at: '2026-01-01T12:00:00Z', values: {quality: 80, wear: 2}, evidence_ref: 'fixture:1'},
          {at: '2026-02-01T12:00:00Z', values: {quality: 70, wear: 4}, evidence_ref: 'fixture:2'},
          {at: '2026-03-01T12:00:00Z', values: {quality: 65, wear: 5}, evidence_ref: 'fixture:3'}
        ],
        purpose: 'simulation'
      }
    };
  }

  selector.addEventListener('change', render);
  seatSelector?.addEventListener('change', render);
  load.addEventListener('click', () => {
    const profile = current();
    if (!profile) return;
    target.value = JSON.stringify(example(profile), null, 2);
    target.dispatchEvent(new Event('input', {bubbles: true}));
    const output = document.getElementById('universal-output');
    if (output) output.replaceChildren(node('p', 'Synthetic ' + profile.title +
      ' profile loaded. Select Simulate to run its schedule checks.'));
    document.getElementById('universal-simulator')?.scrollIntoView({
      behavior: 'smooth', block: 'start'
    });
  });
  async function init() {
    try {
      const response = await fetch('/api/hcck/profiles', {
        headers: {Accept: 'application/json'}, credentials: 'same-origin'
      });
      if (!response.ok) throw new Error('profile directory did not respond');
      const directory = await response.json();
      if (directory.schema !== 'market-compass.hybrid-cck-profile-schedule/v1' ||
          !Array.isArray(directory.profiles)) throw new Error('unexpected profile directory');
      profiles = directory.profiles;
      seats = Array.isArray(directory.participant_instances) ? directory.participant_instances : [];
      if (seatSelector) {
        seatSelector.replaceChildren();
        for (const seat of seats) {
          const choice = document.createElement('option');
          choice.value = seat.id;
          choice.textContent = seat.name + ' · ' + (seat.card?.title || 'Unassigned');
          seatSelector.appendChild(choice);
        }
        seatSelector.disabled = seats.length === 0;
      }
      selector.replaceChildren();
      for (const profile of profiles) {
        const option = document.createElement('option');
        option.value = profile.id;
        option.textContent = profile.title;
        selector.appendChild(option);
      }
      selector.disabled = profiles.length === 0;
      render();
    } catch (error) {
      selector.replaceChildren(node('option', 'Profiles unavailable'));
      selector.disabled = true;
      load.disabled = true;
      detail.replaceChildren(node('p', 'Profile directory unavailable: ' + error.message));
    }
  }
  void init();
});
