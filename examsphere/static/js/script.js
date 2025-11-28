document.addEventListener("DOMContentLoaded", () => {

    /* ----------------------------------------------------
       1. PAGE FADE-IN EFFECT
    ---------------------------------------------------- */
    document.body.style.opacity = 0;
    document.body.style.transition = "opacity 0.7s ease";
    setTimeout(() => { document.body.style.opacity = 1; }, 50);


    /* ----------------------------------------------------
       2. SMOOTH PAGE FADE-OUT ON NAVIGATION
    ---------------------------------------------------- */
    document.querySelectorAll('a[href]').forEach(a => {
        a.addEventListener('click', e => {
            const link = a.getAttribute('href');

            if (
                link.startsWith('#') ||
                a.target === "_blank" ||
                a.href.includes("javascript:")
            ) return;

            e.preventDefault();
            document.body.style.opacity = 0;

            setTimeout(() => { window.location.href = link; }, 300);
        });
    });


    /* ----------------------------------------------------
       3. FLASH MESSAGE ANIMATION
    ---------------------------------------------------- */
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(f => {
        f.style.transition = "all .8s ease";
        f.style.opacity = "1";
        f.style.transform = "translateY(0)";
    });

    if (flashes.length) {
        setTimeout(() => {
            flashes.forEach(f => {
                f.style.opacity = "0";
                f.style.transform = "translateY(-10px)";
            });
        }, 3000);

        setTimeout(() => flashes.forEach(f => f.remove()), 4200);
    }


    /* ----------------------------------------------------
       4. RIPPLE EFFECT ON BUTTONS
    ---------------------------------------------------- */
    document.querySelectorAll("button, .btn").forEach(btn => {
        btn.style.position = "relative";
        btn.style.overflow = "hidden";

        btn.addEventListener("click", function (e) {
            let ripple = document.createElement("span");
            ripple.style.position = "absolute";
            ripple.style.background = "rgba(255,255,255,0.5)";
            ripple.style.borderRadius = "50%";
            ripple.style.transform = "scale(0)";
            ripple.style.animation = "rippleEffect .6s linear";
            ripple.style.pointerEvents = "none";

            let rect = this.getBoundingClientRect();
            ripple.style.width = ripple.style.height = Math.max(rect.width, rect.height) + "px";
            ripple.style.left = e.clientX - rect.left - ripple.offsetWidth / 2 + "px";
            ripple.style.top = e.clientY - rect.top - ripple.offsetHeight / 2 + "px";

            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Auto inject ripple animation
    const rippleStyle = document.createElement("style");
    rippleStyle.innerHTML = `
        @keyframes rippleEffect {
            to { transform: scale(4); opacity: 0; }
        }
    `;
    document.head.appendChild(rippleStyle);


    /* ----------------------------------------------------
       5. NAVBAR SCROLL EFFECT
    ---------------------------------------------------- */
    const navbar = document.querySelector("nav, .navbar");
    if (navbar) {
        navbar.style.transition = "all .3s ease";
        window.addEventListener("scroll", () => {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = "0 3px 10px rgba(0,0,0,0.15)";
                navbar.style.transform = "translateY(0)";
            } else {
                navbar.style.boxShadow = "none";
            }
        });
    }


    /* ----------------------------------------------------
       6. CARD HOVER LIFT EFFECT
    ---------------------------------------------------- */
    document.querySelectorAll(".job-card, .card, .box").forEach(card => {
        card.style.transition = "transform .3s ease, box-shadow .3s ease";
        card.addEventListener("mouseover", () => {
            card.style.transform = "translateY(-5px)";
            card.style.boxShadow = "0 6px 18px rgba(0,0,0,0.12)";
        });
        card.addEventListener("mouseout", () => {
            card.style.transform = "translateY(0)";
            card.style.boxShadow = "none";
        });
    });


    /* ----------------------------------------------------
       7. FORM FOCUS GLOW
    ---------------------------------------------------- */
    document.querySelectorAll("input, textarea, select").forEach(input => {
        input.style.transition = "box-shadow .2s ease";

        input.addEventListener("focus", () => {
            input.style.boxShadow = "0 0 10px rgba(100,150,255,0.5)";
        });

        input.addEventListener("blur", () => {
            input.style.boxShadow = "none";
        });
    });

});
