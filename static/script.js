document.addEventListener("DOMContentLoaded", () => {

    console.log("EventPulse loaded successfully.");

    highlightActivePage();

    attachStopConfirmation();

});

function highlightActivePage() {

    const currentPage = window.location.pathname;

    const navLinks = document.querySelectorAll(".nav-links a");

    navLinks.forEach(link => {

        if (link.getAttribute("href") === currentPage) {

            link.style.color = "#2563eb";

            link.style.fontWeight = "700";

        }

    });

}

function attachStopConfirmation() {

    const stopButton = document.querySelector(".stop-btn");

    if (!stopButton) {

        return;

    }

    stopButton.addEventListener("click", function (event) {

        const confirmStop = confirm(

            "Stop monitoring the selected folder?"

        );

        if (!confirmStop) {

            event.preventDefault();

        }

    });

}