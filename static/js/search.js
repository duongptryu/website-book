document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#search').onclick = () => {
        window.location.href = "{{ url_for('search') }}";
    };
});