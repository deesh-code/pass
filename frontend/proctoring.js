document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        let events = JSON.parse(localStorage.getItem('proctoring_events') || '[]');
        events.push({type: 'visibilitychange', timestamp: new Date().toISOString()});
        localStorage.setItem('proctoring_events', JSON.stringify(events));
    }
});

document.addEventListener('copy', function(e) {
    let events = JSON.parse(localStorage.getItem('proctoring_events') || '[]');
    events.push({type: 'copy', timestamp: new Date().toISOString()});
    localStorage.setItem('proctoring_events', JSON.stringify(events));
});
