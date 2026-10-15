const intake = document.querySelector('#opportunity-intake');
const draftButton = document.querySelector('#prepare-draft');
if (intake && draftButton) {
  draftButton.disabled = false;
  draftButton.addEventListener('click', () => {
  for (const field of intake.querySelectorAll('input,textarea')) {
    if (!field.reportValidity()) return;
  }
  const labels = [['employer','Employer / payer'],['source','Original source'],['task','Useful task and current availability'],['eligibility','Eligibility and location'],['pay','Pay and acceptance terms'],['payout','Payment timing, method, costs and cashout'],['barrier','Access barrier and proposed next step']];
  const body = labels.map(([key,label]) => `${label}:\n${intake.querySelector(`[name="${key}"]`).value || 'Unknown'}\n`).join('\n') + '\nPlease review and remove private worker records before sending.\n';
  const uri = 'mailto:codex-microcredit@agentmail.to?subject=' + encodeURIComponent('Omnequa employer | source=website-intake') + '&body=' + encodeURIComponent(body);
  const fallback = document.querySelector('#email-draft-link');
  fallback.href = uri;
  fallback.hidden = false;
  document.querySelector('#draft-status').textContent = 'Your email draft is ready. Review it in your email app before sending. If the app did not open, use the draft link below.';
  window.location.href = uri;
  });
}
