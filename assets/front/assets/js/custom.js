jQuery(document).ready(function($) {
    // Only run on frontend, not inside Beaver Builder editor
    if (!$('body').hasClass('fl-builder-edit')) {

        // Initial state
        $('#highlightPort').show();
        $('#FulGalleryPort').hide();

        // Button 1
        $('#btnHighlight').click(function(e) {
            e.preventDefault();

            $('#highlightPort').show();
            $('#FulGalleryPort').hide();

            $('.highlightBtn').addClass('active');
            $('.fullGalleryBtn').removeClass('active');

            // Scroll to section
            $('html, body').animate({
                scrollTop: $('#highlightPort').offset().top - 100 // adjust offset if needed
            }, 600);
        });

        // Button 2
        $('#btnGallery').click(function(e) {
            e.preventDefault();

            $('#highlightPort').hide();
            $('#FulGalleryPort').show();

            $('.highlightBtn').removeClass('active');
            $('.fullGalleryBtn').addClass('active');

            // Scroll to section
            $('html, body').animate({
                scrollTop: $('#FulGalleryPort').offset().top - 100
            }, 600);
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
  const observer = new MutationObserver(function (mutationsList, observer) {
    mutationsList.forEach(function (mutation) {
      if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
        const target = mutation.target;
        if (target.classList.contains('fl-success-message')) {
          // PDF download code
          const link = document.createElement('a');
          link.href = 'https://example.com/wp-content/uploads/2025/06/yourfile.pdf';
          link.download = 'yourfile.pdf';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }
      }
    });
  });

  const targetForm = document.querySelector('.fl-form'); // form ki class yahan target karo
  if (targetForm) {
    observer.observe(targetForm, { attributes: true, subtree: true });
  }
});
window.addEventListener("load", function () {
  const loader = document.getElementById("custom-preloader");
  if (loader) {
    loader.style.opacity = "0";
    setTimeout(() => {
      loader.style.display = "none";
    }, 500);
  }
});






 
  const scrollBtn = document.getElementById("scrollTopBtn");

  // Show button on scroll
  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
      scrollBtn.classList.add("show");
    } else {
      scrollBtn.classList.remove("show");
    }
  });

  // Scroll to top on click
  scrollBtn.addEventListener("click", () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  });
 






window.addEventListener("load", () => {
  const loader = document.getElementById("loader");
  const logo = document.getElementById("mainLogo");
  const circle = document.querySelector(".circle-progress circle");
  const mainContent = document.getElementById("mainContent");

  // Step 1: Show logo
  logo.style.opacity = "1";
  logo.style.transform = "translate(-50%, -50%) scale(1.2)";

  // Step 2: Animate circle after 1s
  setTimeout(() => {
    let progress = 0;
    const circumference = 2 * Math.PI * 106;

    function animate() {
      progress += 1;
      if(progress > 100) progress = 100;

      const offset = circumference - (progress / 100) * circumference;
      circle.style.strokeDashoffset = offset;

      if(progress < 100){
        requestAnimationFrame(animate);
      } else {
        // Fully hide loader and show main content
        loader.style.opacity = "0";
        setTimeout(() => {
          loader.style.display = "none";
          mainContent.style.display = "block";
        }, 600); // match transition
      }
    }

    animate();
  }, 1000);
});


