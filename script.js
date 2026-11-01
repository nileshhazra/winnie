// Winnie Landing Page Script

// 1. Theme Management (Light / Dark)
const themeToggleBtn = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

function getPreferredTheme() {
  const saved = localStorage.getItem('winnie-theme');
  if (saved) return saved;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('winnie-theme', theme);
  if (themeIcon) {
    if (theme === 'dark') {
      themeIcon.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>
      `;
    } else {
      themeIcon.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
      `;
    }
  }
}

// Initialize theme
setTheme(getPreferredTheme());

if (themeToggleBtn) {
  themeToggleBtn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    setTheme(current === 'dark' ? 'light' : 'dark');
  });
}

// 2. Showcase Window Dark/Light Tabs
const tabDark = document.getElementById('tab-dark');
const tabLight = document.getElementById('tab-light');
const imgDark = document.getElementById('showcase-img-dark');
const imgLight = document.getElementById('showcase-img-light');

if (tabDark && tabLight && imgDark && imgLight) {
  tabDark.addEventListener('click', () => {
    tabDark.classList.add('active');
    tabLight.classList.remove('active');
    imgDark.classList.remove('hidden');
    imgLight.classList.add('hidden');
  });

  tabLight.addEventListener('click', () => {
    tabLight.classList.add('active');
    tabDark.classList.remove('active');
    imgLight.classList.remove('hidden');
    imgDark.classList.add('hidden');
  });
}

// 3. Interactive Code Stepper Simulator
// Simulates step-by-step visual debugging of two_sum
const stepperSteps = [
  {
    line: 1,
    vars: [
      { name: 'nums', type: 'list', val: '[2, 7, 11, 15]' },
      { name: 'target', type: 'int', val: '9' }
    ]
  },
  {
    line: 2,
    vars: [
      { name: 'nums', type: 'list', val: '[2, 7, 11, 15]' },
      { name: 'target', type: 'int', val: '9' },
      { name: 'seen', type: 'dict', val: '{}' }
    ]
  },
  {
    line: 3,
    vars: [
      { name: 'i', type: 'int', val: '0' },
      { name: 'num', type: 'int', val: '2' },
      { name: 'seen', type: 'dict', val: '{}' }
    ]
  },
  {
    line: 4,
    vars: [
      { name: 'i', type: 'int', val: '0' },
      { name: 'num', type: 'int', val: '2' },
      { name: 'diff', type: 'int', val: '7' },
      { name: 'seen', type: 'dict', val: '{}' }
    ]
  },
  {
    line: 5,
    vars: [
      { name: 'diff in seen', type: 'bool', val: 'False' },
      { name: 'diff', type: 'int', val: '7' }
    ]
  },
  {
    line: 7,
    vars: [
      { name: 'seen', type: 'dict', val: '{2: 0}' }
    ]
  },
  {
    line: 3,
    vars: [
      { name: 'i', type: 'int', val: '1' },
      { name: 'num', type: 'int', val: '7' },
      { name: 'seen', type: 'dict', val: '{2: 0}' }
    ]
  },
  {
    line: 4,
    vars: [
      { name: 'i', type: 'int', val: '1' },
      { name: 'num', type: 'int', val: '7' },
      { name: 'diff', type: 'int', val: '2' },
      { name: 'seen', type: 'dict', val: '{2: 0}' }
    ]
  },
  {
    line: 5,
    vars: [
      { name: 'diff in seen', type: 'bool', val: 'True' },
      { name: 'seen', type: 'dict', val: '{2: 0}' }
    ]
  },
  {
    line: 6,
    vars: [
      { name: 'RETURN', type: 'list', val: '[0, 1]' }
    ]
  }
];

let currentStep = 0;
let autoPlayInterval = null;

const stepBtn = document.getElementById('step-btn');
const playBtn = document.getElementById('play-btn');
const resetBtn = document.getElementById('reset-btn');
const inspectorTbody = document.getElementById('inspector-body');

function renderStep(index) {
  const step = stepperSteps[index];
  
  // Update line highlights
  document.querySelectorAll('.stepper-code .code-line').forEach(el => {
    el.classList.remove('active');
  });
  const activeLine = document.querySelector(`.stepper-code .code-line[data-line="${step.line}"]`);
  if (activeLine) {
    activeLine.classList.add('active');
  }

  // Update variables table
  if (inspectorTbody) {
    inspectorTbody.innerHTML = '';
    step.vars.forEach(v => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td><strong style="color: #F8FAFC;">${v.name}</strong></td>
        <td><span class="type-pill ${v.type}">${v.type}</span></td>
        <td><span class="val-highlight">${v.val}</span></td>
      `;
      inspectorTbody.appendChild(row);
    });
  }
}

if (stepBtn) {
  stepBtn.addEventListener('click', () => {
    currentStep = (currentStep + 1) % stepperSteps.length;
    renderStep(currentStep);
  });
}

if (playBtn) {
  playBtn.addEventListener('click', () => {
    if (autoPlayInterval) {
      clearInterval(autoPlayInterval);
      autoPlayInterval = null;
      playBtn.innerHTML = `
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
        Play
      `;
    } else {
      playBtn.innerHTML = `
        <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
        Pause
      `;
      autoPlayInterval = setInterval(() => {
        currentStep = (currentStep + 1) % stepperSteps.length;
        renderStep(currentStep);
      }, 950);
    }
  });
}

if (resetBtn) {
  resetBtn.addEventListener('click', () => {
    if (autoPlayInterval) {
      clearInterval(autoPlayInterval);
      autoPlayInterval = null;
      if (playBtn) playBtn.innerText = 'Play';
    }
    currentStep = 0;
    renderStep(0);
  });
}

// Render initial step
renderStep(0);

// 4. FAQ Accordions
document.querySelectorAll('.faq-item').forEach(item => {
  const question = item.querySelector('.faq-question');
  question.addEventListener('click', () => {
    const isOpen = item.classList.contains('open');
    // Close other items
    document.querySelectorAll('.faq-item').forEach(other => other.classList.remove('open'));
    if (!isOpen) {
      item.classList.add('open');
    }
  });
});

// 5. Gatekeeper Quarantine Copy Command
const copyBtn = document.getElementById('copy-cmd-btn');
const cmdText = 'xattr -cr /Applications/Winnie.app';

if (copyBtn) {
  copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(cmdText).then(() => {
      const origText = copyBtn.innerText;
      copyBtn.innerText = 'Copied!';
      copyBtn.style.background = '#27C93F';
      copyBtn.style.color = '#FFF';
      setTimeout(() => {
        copyBtn.innerText = origText;
        copyBtn.style.background = '';
        copyBtn.style.color = '';
      }, 2000);
    });
  });
}
