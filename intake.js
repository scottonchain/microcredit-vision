const intake = document.querySelector('#opportunity-intake');
const draftButton = document.querySelector('#prepare-draft');
if (intake && draftButton) {
  const fallback = document.querySelector('#email-draft-link');
  const plainPanel = document.querySelector('#plain-draft-panel');
  const plainDraft = document.querySelector('#plain-draft');
  const status = document.querySelector('#draft-status');
  const clearDraft = message => {
    fallback.hidden = true;
    fallback.removeAttribute('href');
    plainPanel.hidden = true;
    plainDraft.value = '';
    status.textContent = message;
  };
  intake.addEventListener('input', () => clearDraft('Answers changed. Prepare a new draft before copying or opening it.'));
  draftButton.disabled = false;
  draftButton.addEventListener('click', () => {
  clearDraft('Check the required answers before preparing a brief. Nothing has been sent.');
  for (const field of intake.querySelectorAll('input[required],textarea[required]')) {
    if (!field.reportValidity()) return;
  }
  const labels = [['employer','Employer / payer'],['source','Original source'],['task','Useful task and current availability'],['eligibility','Eligibility and location'],['pay','Pay and acceptance terms'],['payout','Payment timing, method, costs and cashout'],['barrier','Access barrier and proposed next step']];
  const body = labels.map(([key,label]) => `${label}:\n${intake.querySelector(`[name="${key}"]`).value || 'Unknown'}\n`).join('\n') + '\nPlease review and remove private worker records before sending.\n';
  const uri = 'mailto:codex-microcredit@agentmail.to?subject=' + encodeURIComponent('Omnequa employer | source=website-intake') + '&body=' + encodeURIComponent(body.replace(/\r\n|\r|\n/g, '\r\n'));
  plainDraft.value = body;
  plainPanel.hidden = false;
  fallback.href = uri;
  fallback.hidden = false;
  status.textContent = 'Your brief is ready, but has not been sent. Copy it into your own email service or open the prepared draft below, then review before sending.';
  });
}
