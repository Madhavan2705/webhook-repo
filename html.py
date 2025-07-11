<!DOCTYPE html>
<html>
<head>
    <title>Github Webhook Events</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .event { margin-bottom: 10px; }
    </style>
</head>
<body>
    <h2>Latest Github Events</h2>
    <div id="events"></div>

    <script>
        async function fetchEvents() {
            const res = await fetch('/events');
            const data = await res.json();
            const container = document.getElementById('events');
            container.innerHTML = '';

            data.forEach(e => {
                let text = '';
                const time = new Date(e.timestamp).toLocaleString('en-US', { timeZone: 'UTC' });
                if (e.action_type === 'push') {
                    text = `${e.author} pushed to ${e.to_branch} on ${time} UTC`;
                } else if (e.action_type === 'pull_request') {
                    text = `${e.author} submitted a pull request from ${e.from_branch} to ${e.to_branch} on ${time} UTC`;
                } else if (e.action_type === 'merge') {
                    text = `${e.author} merged branch ${e.from_branch} to ${e.to_branch} on ${time} UTC`;
                }
                const div = document.createElement('div');
                div.className = 'event';
                div.textContent = text;
                container.appendChild(div);
            });
        }

        fetchEvents();
        setInterval(fetchEvents, 15000);
    </script>
</body>
</html>
