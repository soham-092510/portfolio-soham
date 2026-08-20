// Portfolio Interactive Script

document.addEventListener('DOMContentLoaded', () => {
  initTypingEffect();
  initNavbarScroll();
  initMobileNav();
  initProjectFilters();
  initScrollReveal();
  initAchievementsCounter();
  initSkillBars();
  initCardGlow();
});

// 1. Typing effect for Hero Section
function initTypingEffect() {
  const targetElement = document.getElementById('typed-designation');
  if (!targetElement) return;

  const designations = [
    "Machine Learning Engineer",
    "Data Scientist",
    "DevOps Learner"
  ];
  
  let dIndex = 0;
  let charIndex = 0;
  let isErasing = false;
  let typingSpeed = 100;
  let erasingSpeed = 50;
  let delayBetweenWords = 2000;

  function type() {
    const currentWord = designations[dIndex];
    
    if (isErasing) {
      targetElement.textContent = currentWord.substring(0, charIndex - 1);
      charIndex--;
      
      if (charIndex === 0) {
        isErasing = false;
        dIndex = (dIndex + 1) % designations.length;
        setTimeout(type, 500);
      } else {
        setTimeout(type, erasingSpeed);
      }
    } else {
      targetElement.textContent = currentWord.substring(0, charIndex + 1);
      charIndex++;
      
      if (charIndex === currentWord.length) {
        isErasing = true;
        setTimeout(type, delayBetweenWords);
      } else {
        setTimeout(type, typingSpeed);
      }
    }
  }

  // Start typing
  setTimeout(type, 1000);
}

// 2. Navigation bar scrolling adjustments and active indicators
function initNavbarScroll() {
  const navbar = document.getElementById('site-header');
  const sections = document.querySelectorAll('section');
  const navLinks = document.querySelectorAll('.nav-link');
  
  window.addEventListener('scroll', () => {
    // Background blur toggling
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
    
    // Active section links tracking
    let currentSection = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (window.scrollY >= (sectionTop - 150)) {
        currentSection = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentSection}`) {
        link.classList.add('active');
      }
    });
  });
}

// 3. Mobile Menu Navigation
function initMobileNav() {
  const toggleBtn = document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileLinks = document.querySelectorAll('.mobile-link');

  if (!toggleBtn || !mobileMenu) return;

  toggleBtn.addEventListener('click', () => {
    toggleBtn.classList.toggle('active');
    mobileMenu.classList.toggle('active');
    document.body.classList.toggle('no-scroll');
  });

  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      toggleBtn.classList.remove('active');
      mobileMenu.classList.remove('active');
      document.body.classList.remove('no-scroll');
    });
  });
}

// 4. Project filters
function initProjectFilters() {
  const filterButtons = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card-wrap');

  filterButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Toggle active states for filter menu
      filterButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');

      const filterValue = button.getAttribute('data-filter');

      projectCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filterValue === 'all' || category === filterValue) {
          card.style.display = 'block';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
          }, 50);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'scale(0.95)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 300);
        }
      });
    });
  });
}

// 5. Scroll Reveal animations
function initScrollReveal() {
  const reveals = document.querySelectorAll('.reveal');

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target); // Reveal only once
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
  });

  reveals.forEach(element => {
    revealObserver.observe(element);
  });
}

// 6. Achievements Stat counters
function initAchievementsCounter() {
  const statNumbers = document.querySelectorAll('.stat-number');
  
  const countObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const numberEl = entry.target;
        const targetVal = parseInt(numberEl.getAttribute('data-target'), 10);
        
        if (targetVal === 0) {
          numberEl.textContent = '0';
          observer.unobserve(numberEl);
          return;
        }

        let currentVal = 0;
        const duration = 1500; // 1.5 seconds
        const stepTime = Math.max(Math.floor(duration / targetVal), 30);
        
        const counterInterval = setInterval(() => {
          currentVal++;
          numberEl.textContent = currentVal + (targetVal > 3 ? '+' : '+');
          if (currentVal >= targetVal) {
            numberEl.textContent = targetVal + (targetVal > 1 ? '+' : '+');
            clearInterval(counterInterval);
          }
        }, stepTime);

        observer.unobserve(numberEl);
      }
    });
  }, {
    threshold: 0.5
  });

  statNumbers.forEach(num => {
    countObserver.observe(num);
  });
}

// 7. Dynamic skill meters animation
function initSkillBars() {
  const skillBars = document.querySelectorAll('.skill-bar-inner');

  const barObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        const width = bar.getAttribute('data-width');
        bar.style.width = width;
        observer.unobserve(bar);
      }
    });
  }, {
    threshold: 0.2
  });

  skillBars.forEach(bar => {
    barObserver.observe(bar);
  });
}

// 8. Contact Form Handling
function handleFormSubmit(event) {
  event.preventDefault();

  const nameInput = document.getElementById('form-name');
  const emailInput = document.getElementById('form-email');
  const subjectInput = document.getElementById('form-subject');
  const messageInput = document.getElementById('form-message');
  const submitBtn = document.getElementById('btn-submit-form');
  const toast = document.getElementById('success-toast');

  // Simulated button loading
  submitBtn.disabled = true;
  submitBtn.textContent = 'Sending Message...';

  // Simulate server response
  setTimeout(() => {
    // Show Toast
    toast.classList.add('active');

    // Reset inputs
    nameInput.value = '';
    emailInput.value = '';
    subjectInput.value = '';
    messageInput.value = '';
    
    // Reset inputs placeholder active states
    document.querySelectorAll('.form-input').forEach(input => {
      input.dispatchEvent(new Event('blur'));
    });

    submitBtn.disabled = false;
    submitBtn.textContent = 'Send Message →';

    // Hide Toast after 4 seconds
    setTimeout(() => {
      toast.classList.remove('active');
    }, 4000);
  }, 1200);
}

// 9. Modals (Certificates and PDF viewer)
const modal = document.getElementById('media-modal');
const modalBody = document.getElementById('modal-body-container');
const modalTitle = document.getElementById('modal-title');
const modalDesc = document.getElementById('modal-desc');

function openCertModal(imageSrc, titleText, descText) {
  if (!modal || !modalBody) return;

  // Render Image inside Modal
  modalBody.innerHTML = `<img src="${imageSrc}" alt="${titleText}" onerror="loadModalImageFallback(this)">`;
  modalTitle.textContent = titleText;
  modalDesc.textContent = descText || "Professional certificate credential.";
  
  modal.classList.add('active');
  document.body.classList.add('no-scroll');
}

function openPdfModal(pdfUrl, titleText, descText) {
  if (!modal || !modalBody) return;

  // Render PDF iframe
  modalBody.innerHTML = `<iframe src="${pdfUrl}" type="application/pdf"></iframe>`;
  modalTitle.textContent = titleText;
  modalDesc.textContent = descText || "Full PDF credential details.";

  modal.classList.add('active');
  document.body.classList.add('no-scroll');
}

function closeModal(event) {
  // Close only if click is outside modal-content (or close btn)
  if (event.target === modal) {
    closeModalDirect();
  }
}

function closeModalDirect() {
  modal.classList.remove('active');
  document.body.classList.remove('no-scroll');
  // Clear modal contents to stop PDF loading
  setTimeout(() => {
    modalBody.innerHTML = '';
  }, 300);
}

// 10. Fail-safe asset loading (CSS and SVGs placeholders for missing user uploads)
function loadProfileFallback() {
  const profileImgWrap = document.querySelector('.profile-img-wrap');
  if (profileImgWrap) {
    profileImgWrap.innerHTML = `
      <div class="profile-avatar-fallback">
        <span class="initials">SG</span>
        <span class="label">Soham Gaikwad</span>
      </div>
    `;
  }
}

function loadCertFallback(imgEl) {
  const targetPreview = imgEl ? imgEl.closest('.cert-image-preview') : document.querySelector('.cert-image-preview');
  if (targetPreview) {
    const titleText = imgEl ? imgEl.alt : "Professional Certificate";
    targetPreview.innerHTML = `
      <div class="cert-placeholder" style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; height: 100%; width: 100%; padding: 1.5rem;">
        <svg viewBox="0 0 24 24" style="width: 40px; height: 40px; fill: var(--color-gold); margin-bottom: 0.5rem;"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
        <h4 style="font-size: 0.95rem; color: var(--color-cream); margin-bottom: 0.25rem; font-family: var(--font-sans); font-weight: 600;">${titleText}</h4>
        <p style="font-size: 0.75rem; color: var(--color-muted);">Certificate Preview Placeholder</p>
      </div>
      <div class="cert-overlay">
        <span>View Details</span>
      </div>
    `;
  }
}

function loadModalImageFallback(imgEl) {
  imgEl.outerHTML = `
    <div class="profile-avatar-fallback" style="padding: 4rem 2rem; max-width: 500px; text-align: center; border-radius: 4px;">
      <svg viewBox="0 0 24 24" width="60" height="60" fill="var(--color-gold)" style="margin-bottom:1rem;"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>
      <h3 style="color:var(--color-cream); font-family:var(--font-serif-header); margin-bottom:0.5rem;">Certificate Graphic</h3>
      <p style="color:var(--color-cream-secondary); font-size:0.9rem; margin-bottom:1.5rem;">"Data Science with Python" external training course completion credential.</p>
      <span style="font-size:0.75rem; color:var(--color-muted);">File Name: datascience_python.jpg</span>
    </div>
  `;
}

// 11. Interactive hover glow spotlight effect for cards
function initCardGlow() {
  const cards = document.querySelectorAll('.glass-card');
  
  cards.forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left; // x position within the element
      const y = e.clientY - rect.top;  // y position within the element
      
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });
}
