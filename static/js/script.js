/* =====================================================================
   script.js — Rising Waters Form Validation & UX Enhancements
   ===================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('predictForm');
  if (!form) return;

  const submitBtn = document.getElementById('submitBtn');

  // Input boundaries (must match core/config.py LIMITS exactly)
  const rules = {
    cloudCover:      { min: 0, max: 100, label: 'Cloud cover must be between 0% and 100%.' },
    annualRainfall:  { min: 0, max: 10000, label: 'Annual rainfall must be between 0 and 10,000 mm.' },
    janFeb:          { min: 0, max: 5000, label: 'Jan–Feb rainfall must be between 0 and 5,000 mm.' },
    marMay:          { min: 0, max: 5000, label: 'March–May rainfall must be between 0 and 5,000 mm.' },
    junSep:          { min: 0, max: 8000, label: 'June–September rainfall must be between 0 and 8,000 mm.' },
  };

  const setError = (input, message) => {
    input.classList.toggle('invalid', Boolean(message));
    const errorEl = form.querySelector(`[data-error-for="${input.id}"]`);
    if (errorEl) {
      errorEl.textContent = message || '';
    }
  };

  const validateField = (input) => {
    const rule = rules[input.id];
    if (!rule) return true;

    const raw = input.value.trim();
    if (raw === '') {
      setError(input, 'This field is required.');
      return false;
    }

    const value = Number(raw);
    if (Number.isNaN(value) || value < rule.min || value > rule.max) {
      setError(input, rule.label);
      return false;
    }

    setError(input, '');
    return true;
  };

  // Validate on blur
  Object.keys(rules).forEach((id) => {
    const input = document.getElementById(id);
    if (!input) return;
    
    input.addEventListener('blur', () => validateField(input));
    input.addEventListener('input', () => {
      // Clear error state dynamically if they correct it
      if (input.classList.contains('invalid')) {
        validateField(input);
      }
    });
  });

  // Validate and show loader on submit
  form.addEventListener('submit', (event) => {
    let allValid = true;
    
    Object.keys(rules).forEach((id) => {
      const input = document.getElementById(id);
      if (input && !validateField(input)) {
        allValid = false;
      }
    });

    if (!allValid) {
      event.preventDefault();
      const firstInvalid = form.querySelector('.invalid');
      if (firstInvalid) {
        firstInvalid.focus();
      }
    } else if (submitBtn) {
      // Disable button and add loading indicator
      submitBtn.disabled = true;
      submitBtn.innerHTML = `
        <svg class="btn-spinner" viewBox="0 0 50 50" style="width: 20px; height: 20px; animation: spin 1s linear infinite; margin-right: 8px; display: inline-block; vertical-align: middle;">
          <circle cx="25" cy="25" r="20" fill="none" stroke="currentColor" stroke-width="5" stroke-dasharray="80 150" stroke-linecap="round"></circle>
        </svg>
        Evaluating Model...
      `;
      // Inject CSS style for spinner animation if not present
      if (!document.getElementById('spinner-style')) {
        const style = document.createElement('style');
        style.id = 'spinner-style';
        style.innerHTML = `
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `;
        document.head.appendChild(style);
      }
    }
  });
});
