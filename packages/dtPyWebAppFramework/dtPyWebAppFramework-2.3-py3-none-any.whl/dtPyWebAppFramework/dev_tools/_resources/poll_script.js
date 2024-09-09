function pollServer() {
    fetch('check-for-update')
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.url; // Redirect to the URL provided by the server
        }
    });
}

// Start polling the server every 10 seconds
setInterval(pollServer, 2000);