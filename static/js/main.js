// Set current year in footer
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("current-year").textContent = new Date().getFullYear()
  
    // Mobile menu toggle
    const mobileMenuBtn = document.querySelector(".mobile-menu-btn")
    const navLinks = document.querySelector(".nav-links")
  
    if (mobileMenuBtn && navLinks) {
      mobileMenuBtn.addEventListener("click", () => {
        navLinks.classList.toggle("show")
      })
  
      // Add show class for mobile menu
      navLinks.style.display = "none"
      navLinks.style.transition = "all 0.3s ease"
  
      // Add style for mobile menu
      const style = document.createElement("style")
      style.textContent = `
        .nav-links.show {
          display: flex;
          flex-direction: column;
          position: absolute;
          top: 70px;
          left: 0;
          width: 100%;
          background: var(--light);
          padding: 20px;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        @media (min-width: 769px) {
          .nav-links {
            display: flex !important;
          }
        }
      `
      document.head.appendChild(style)
    }
  
    // Scroll animation
    const fadeElements = document.querySelectorAll(".fade-in")
  
    function checkScroll() {
      fadeElements.forEach((element) => {
        const elementTop = element.getBoundingClientRect().top
        const windowHeight = window.innerHeight
  
        if (elementTop < windowHeight - 100) {
          element.style.opacity = "1"
          element.style.transform = "translateY(0)"
        }
      })
    }
  
    checkScroll()
    window.addEventListener("scroll", checkScroll)
  })
  