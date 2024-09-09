window.addEventListener('load', function () {
    // Set a flag in session storage when the page loads
    sessionStorage.setItem('navigationFlag', 'false');
});

// Listen for internal link clicks to update the session storage
document.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        sessionStorage.setItem('navigationFlag', 'true');
        setTimeout(function() {
            // Code to run after the link is clicked
            sessionStorage.setItem('navigationFlag', 'false');
    }, 0);
    });
});


window.addEventListener('unload', function (event) {
    // Check the navigation flag in session storage
    const navigationFlag = sessionStorage.getItem('navigationFlag');
    if (navigationFlag === 'false') {
        // Only send the beacon if there's no internal navigation
        navigator.sendBeacon('close');
    }
});
